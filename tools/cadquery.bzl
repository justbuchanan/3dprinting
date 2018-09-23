load("//tools:cura.bzl", "slice_stl_to_gcode")

def _cq_render(ctx):
    p = ctx.outputs.out.dirname + "/outdir"
    ctx.actions.run(
        inputs = ctx.files.file + ctx.files.deps + [ctx.executable._cadquery_tool],
        outputs = [ctx.outputs.out],
        # command = "python2 {cmd} --file {file} --outfile {out}".format(
        #     cmd=ctx.executable._cadquery_tool.path,
        #     file=ctx.file.file.path,
        #     out=ctx.outputs.out.path),
        executable=ctx.executable._cadquery_tool,
        arguments=["--file", ctx.file.file.path, "--outfile", ctx.outputs.out.path],
        mnemonic = "CadQueryRender",
    )

cq_render = rule(
    implementation = _cq_render,
    attrs = {
        "file": attr.label(allow_files = True, mandatory = True, single_file = True),
        "out": attr.output(mandatory = True),
        "_cadquery_tool": attr.label(cfg = "host", executable = True, allow_files = True, default = Label("//tools:cq_render")),
        "deps": attr.label_list(allow_files = True),
    },
)

def cq_model(name, file, deps = []):
    # TODO: this doesn't work - there are multiple output files
    cq_render(
        name = name + "_gltf",
        file = file,
        out = name + ".gltf",
        deps = deps,
    )
    cq_render(
        name = name + "_stl",
        file = file,
        out = name + ".stl",
        deps = deps,
    )
    slice_stl_to_gcode(
        name = name + "_gcode",
        file = name + "_stl",
        gcode_out = name + ".gcode",
    )
