A few of my 3d printed designs. These are not particularly well organized, so explore at your own risk.

To build all models files and render stls (this will take a while...):

```{.sh}
bazel build $(bazel query 'kind(scad_render,...)')
```

Browse `bazel-bin` to see the results.

When opening openscad models (source files or those generated in bazel-bin), be sure to add the relevant directories to the `OPENSCADPATH` environment variable. For example:

```{.sh}
OPENSCADPATH="$(pwd):$(pwd)/bazel-bin:$OPENSCADPATH" openscad path/to/file.scad
```
