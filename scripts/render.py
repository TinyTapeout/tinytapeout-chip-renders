# SPDX-License-Identifier: Apache-2.0
# This script creates a full-die render of a given Tiny Tapeout shuttle.
# Copyright (C) 2024 Tiny Tapeout LTD
# Author: Uri Shaked

import argparse
import json
import logging
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List, Optional

from klayout.lay import LayoutView

# In legacy shuttles, we don't have an OAS file of the complete chip, rather a GDS file with just Tiny Tapeout tiles.
LEGACY_SHUTTLES = ["tt01", "tt02", "tt03", "tt03p5"]
SCRIPT_DIR = Path(__file__).parent


TECHNOLOGIES = {
    "sky130A": {
        "boundary": "prBoundary.boundary",
        "hide_layers": ["areaid.standardc", "areaid.lowTapDensity"],
        "logic_density_layers": ["li1.drawing", "li1.pin"],
    },
    "sg13g2": {
        "boundary": "EdgeSeal.boundary",
        "hide_layers": [],
        "logic_density_layers": ["Via1.drawing", "Via3.drawing"],
    },
}


def download_gds(shuttle_id: str) -> Path:
    extension = "oas" if shuttle_id not in LEGACY_SHUTTLES else "gds"
    target_path = SCRIPT_DIR / "gds" / f"{shuttle_id}.{extension}"
    if target_path.exists():
        logging.info(f"Found existing GDS file at {target_path}, skipping download")
        return target_path

    # Download the main index file from the Tiny Tapeout server
    url = "https://index.tinytapeout.com/index.json"
    logging.info(f"Downloading index file from {url}")
    response = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    )
    index = json.load(response)
    shuttles = index.get("shuttles", {})
    shuttle = next(
        (shuttle for shuttle in shuttles if shuttle["id"] == shuttle_id), None
    )
    if shuttle_id == "tt01":
        # Tiny Tapeout 1 was an experimental shuttle and is not in the main index
        shuttle = {
            "gds_url": "https://github.com/TinyTapeout/tinytapeout-02/raw/mpw7/gds/user_project_wrapper.gds.gz"
        }
    if not shuttle:
        logging.error(f"Shuttle {shuttle_id} not found in the index")
        sys.exit(1)

    gds_url = shuttle["gds_url"]
    logging.info(f"Downloading GDS file from {gds_url}")

    response = urllib.request.urlopen(gds_url)
    with open(target_path, "wb") as f:
        if gds_url.endswith(".gz"):
            import gzip

            with gzip.GzipFile(fileobj=response) as gz:
                f.write(gz.read())
        else:
            f.write(response.read())

    return target_path


def render_gds(
    gds_path: str,
    output_path: str,
    scale: float = 1.0,
    tech: str = "sky130A",
    only_layers: Optional[List[str]] = None,
    hide_layers: Optional[List[str]] = None,
):
    BOUNDARY_LAYER = TECHNOLOGIES[tech]["boundary"]

    lv = LayoutView()
    lv.load_layout(gds_path)
    lv.max_hier()
    lv.load_layer_props(SCRIPT_DIR / "lyp" / f"{tech}.lyp")
    lv.set_config("background-color", "#ffffff")
    lv.set_config("grid-visible", "false")
    lv.set_config("text-visible", "false")
    lv.zoom_fit()

    bbox = None
    for layer in lv.each_layer():
        layer_name = layer.name
        if tech == "sky130A":
            layer_name = layer_name.split("-")[0].strip() if "-" in layer_name else ""
        if layer_name == BOUNDARY_LAYER:
            bbox = layer.bbox()
            layer.visible = True
        elif only_layers is not None:
            layer.visible = layer_name in only_layers
        elif hide_layers is not None:
            layer.visible = layer_name not in hide_layers and layer_name != ""
        else:
            layer.visible = layer_name != ""  # Hides the fill layers

    if bbox is None:
        raise ValueError(f"No bounding box found for '{BOUNDARY_LAYER}' layer")
    lv.zoom_box(bbox)

    lv.save_image(output_path, int(bbox.width() * scale), int(bbox.height() * scale))
    lv.destroy()


def main(shuttle_id: str, scale: float = 1.0):
    gds_file = download_gds(shuttle_id)
    png_dir = SCRIPT_DIR / ".." / "shuttles" / shuttle_id
    png_dir.mkdir(parents=True, exist_ok=True)

    tech = "sg13g2" if shuttle_id.startswith("ttihp") else "sky130A"
    tech_info = TECHNOLOGIES[tech]

    logging.info(f"Rendering {png_dir / 'full_gds.png'}")
    render_gds(
        gds_file,
        png_dir / "full_gds.png",
        scale=scale,
        tech=tech,
        hide_layers=tech_info["hide_layers"],
    )

    logging.info(f"Rendering {png_dir / 'logic_density.png'}")
    render_gds(
        gds_file,
        png_dir / "logic_density.png",
        tech=tech,
        scale=scale,
        only_layers=tech_info["logic_density_layers"],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update shuttle index")
    parser.add_argument("shuttle_id", type=str, help="Shuttle ID")
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Scale factor for the output image",
    )

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    main(args.shuttle_id, scale=args.scale)
