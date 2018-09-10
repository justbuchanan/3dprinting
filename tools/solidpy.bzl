load("//tools:openscad.bzl", "scad_model")

def _solidpy_to_scad(ctx):
    args = ["--output", ctx.outputs.out.path, ctx.file.file.path, "--header", "$fn=%d;" % ctx.attr.resolution]
    outs = [ctx.outputs.out]
    if ctx.outputs.bom_out:
        outs.append(ctx.outputs.bom_out)
        args += ["--bom_output", ctx.outputs.bom_out.path]
    ctx.actions.run(
        inputs = ctx.files.file + ctx.files.deps + ctx.files.py_deps,
        outputs = outs,
        progress_message = "toscad;",
        arguments = args,
        executable = ctx.executable._render_tool,
    )

solidpy_to_scad = rule(
    implementation = _solidpy_to_scad,
    attrs = {
        "file": attr.label(allow_files = True, mandatory = True, single_file = True),
        "out": attr.output(mandatory = True),
        "bom_out": attr.output(mandatory = False),
        "_render_tool": attr.label(cfg = "host", executable = True, allow_files = True, default = Label("//tools:render")),
        "deps": attr.label_list(allow_files = True),
        "py_deps": attr.label_list(allow_files = True),
        "resolution": attr.int(default = 200),
    },
)

def solidpy_model(name, file, deps = [], py_deps = [], scad_resolution = 100, three_d = True):
    solidpy_to_scad(
        name = name + "_scad",
        file = file,
        out = name + ".scad",
        bom_out = name + "_bom.txt",
        deps = deps,
        py_deps = py_deps,
        resolution = scad_resolution,
    )
    scad_model(
        name = name,
        file = name + ".scad",
        deps = deps,
        three_d = three_d,
    )
