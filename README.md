# Tiny Tapeout Chip Renders

This repo contains the chip renders for all Tiny Tapeouts shuttles. Each shuttle includes up to three renders:

- full_gds.png: A full render of the GDS file.
- logic_density: Shows only the local interconnect layer, which is used to estimate the logic density of the chip.
- top_metal.png: Shows only the top metal 1/2 layers (IHP shuttles only).

For Tiny Tapeout 4 and later, the renders include the complete chip area, including the pads, and the caravel harness. For earlier shuttles, the renders only include the core area.

The renders are generated using the [render.py](scripts/render.py) script, which uses [klayout](https://www.klayout.org/) to render the GDS files. See [below](#regenerating-the-renders) for instructions on how to regenerate the renders.

## Full Renders

### Tiny Tapeout IHP 25a

[![Tiny Tapeout IHP 25a](shuttles/ttihp25a/full_gds.png)](shuttles/ttihp25a/full_gds.png)

### Tiny Tapeout 9

[![Tiny Tapeout 9](shuttles/tt09/full_gds.png)](shuttles/tt09/full_gds.png)

### Tiny Tapeout IHP 0p2

[![Tiny Tapeout IHP 0p2](shuttles/ttihp0p2/full_gds.png)](shuttles/ttihp0p2/full_gds.png)

### Tiny Tapeout 8

[![Tiny Tapeout 8](shuttles/tt08/full_gds.png)](shuttles/tt08/full_gds.png)

### Tiny Tapeout IHP 0p1

[![Tiny Tapeout IHP 0p1](shuttles/ttihp0p1/full_gds.png)](shuttles/ttihp0p1/full_gds.png)

### Tiny Tapeout 7

[![Tiny Tapeout 7](shuttles/tt07/full_gds.png)](shuttles/tt07/full_gds.png)

### Tiny Tapeout 6

[![Tiny Tapeout 6](shuttles/tt06/full_gds.png)](shuttles/tt06/full_gds.png)

### Tiny Tapeout 5 OpenFrame

[![Tiny Tapeout 5 OpenFrame](shuttles/tt05of/full_gds.png)](shuttles/tt05of/full_gds.png)

### Tiny Tapeout 5

[![Tiny Tapeout 5](shuttles/tt05/full_gds.png)](shuttles/tt05/full_gds.png)

### Tiny Tapeout 4

[![Tiny Tapeout 4](shuttles/tt04/full_gds.png)](shuttles/tt04/full_gds.png)

### Tiny Tapeout 03p5

[![Tiny Tapeout 03p5](shuttles/tt03p5/full_gds.png)](shuttles/tt03p5/full_gds.png)

### Tiny Tapeout 3

[![Tiny Tapeout 3](shuttles/tt03/full_gds.png)](shuttles/tt03/full_gds.png)

### Tiny Tapeout 2

[![Tiny Tapeout 2](shuttles/tt02/full_gds.png)](shuttles/tt02/full_gds.png)

### Tiny Tapeout 1

[![Tiny Tapeout 1](shuttles/tt01/full_gds.png)](shuttles/tt01/full_gds.png)

## Top Metal Renders

* [Tiny Tapeout IHP 25a](shuttles/ttihp25a/top_metal.png)
* [Tiny Tapeout IHP 0p2](shuttles/ttihp0p2/top_metal.png)

## Logic Density Renders

* [Tiny Tapeout IHP 25a](shuttles/ttihp25a/logic_density.png)
* [Tiny Tapeout 9](shuttles/tt09/logic_density.png)
* [Tiny Tapeout IHP 0p2](shuttles/ttihp0p2/logic_density.png)
* [Tiny Tapeout 8](shuttles/tt08/logic_density.png)
* [Tiny Tapeout IHP 0p1](shuttles/ttihp0p1/logic_density.png)
* [Tiny Tapeout 7](shuttles/tt07/logic_density.png)
* [Tiny Tapeout 6](shuttles/tt06/logic_density.png)
* [Tiny Tapeout 5 OpenFrame](shuttles/tt05of/logic_density.png)
* [Tiny Tapeout 5](shuttles/tt05/logic_density.png)
* [Tiny Tapeout 4](shuttles/tt04/logic_density.png)
* [Tiny Tapeout 03p5](shuttles/tt03p5/logic_density.png)
* [Tiny Tapeout 3](shuttles/tt03/logic_density.png)
* [Tiny Tapeout 2](shuttles/tt02/logic_density.png)
* [Tiny Tapeout 1](shuttles/tt01/logic_density.png)

## Regenerating the renders

To regenerate the PNG files for a shuttle, run the following commands:

```bash
cd scripts
pip install -r requirements.txt
python render.py <shuttle>
```

Where `<shuttle>` is the identifier of the shuttle (e.g. tt04).

You can also specify the scale of the render by passing the `--scale` argument. For example, to render the full GDS of shuttle tt04 at 2x scale:

```bash
python render.py tt04 --scale 2
```

## License

The chip renders are licensed under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.
