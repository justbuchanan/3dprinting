# 3d printed models

A few of my 3d printed designs. These are not particularly well organized, so explore at your own risk.

## Dependencies

- [bazel](https://bazel.build/) - this is the build system used to turn source solidpy and scad models into output stls, svgs, and gcode.
- [openscad](http://www.openscad.org/) - programmatic CAD software
- [cura](https://ultimaker.com/en/products/ultimaker-cura-software) (optional) - 3d slicer that turns stls into gcode instructions

## Rendering models

To see a list of everything that can be rendered, do a bazel query:

```{.sh}
bazel query //...
```

Build a model with (for example):

```{.sh}
bazel build //succulent_planter:planter_stl
```

To build and render all stls (this will take a while...):

```{.sh}
bazel build $(bazel query 'kind(scad_render,...)')
```

Browse the `bazel-bin` directory to see the results.

## Tips

When opening openscad models (source files or those generated in `bazel-bin`), be sure to add the relevant directories to the `OPENSCADPATH` environment variable. For example:

```{.sh}
OPENSCADPATH="$(pwd):$(pwd)/bazel-bin:$OPENSCADPATH" openscad path/to/file.scad
```
