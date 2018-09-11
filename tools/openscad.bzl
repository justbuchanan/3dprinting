load("//tools:cura.bzl", "slice_stl_to_gcode")

def _part_scad_file(ctx):
    ctx.actions.write(
        output = ctx.outputs.output,
        content = "include <%s>;\n%s;" % (ctx.file.file.path, ctx.attr.toplevel),
        is_executable = False,
    )

part_scad_file = rule(
    implementation = _part_scad_file,
    attrs = {
        "file": attr.label(allow_files = True, mandatory = True, single_file = True),
        "output": attr.output(mandatory = True),
        "toplevel": attr.string(mandatory = True),
    },
)

def _scad_render(ctx):
    ctx.actions.run(
        inputs = ctx.files.file + ctx.files.deps,
        outputs = [ctx.outputs.out],
        arguments = ["-o", ctx.outputs.out.path, ctx.file.file.path],
        executable = ctx.executable._openscad_tool,
        mnemonic = "OpenSCADRender",
    )

scad_render = rule(
    implementation = _scad_render,
    attrs = {
        "file": attr.label(allow_files = True, mandatory = True, single_file = True),
        "out": attr.output(mandatory = True),
        "_openscad_tool": attr.label(cfg = "host", executable = True, allow_files = True, default = Label("//tools:openscad")),
        "deps": attr.label_list(allow_files = True),
    },
)

def scad_model(name, file, deps = [], three_d = True):
    if three_d:
        scad_render(
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
    else:
        scad_render(
            name = name + "_svg",
            file = file,
            out = name + ".svg",
            deps = deps,
        )

# Instead of using the "model" variable from the python file as solidpy_to_scad
# does, this accepts a "toplevel" argument that lets you define what to render
# as a snippet of scad code that's evaluated within the context of the file.
def scad_part(name, file, toplevel, deps = [], three_d = True):
    tmpfile = name + "_part.scad"
    part_scad_file(name = name + "_scad", file = file, output = tmpfile, toplevel = toplevel)
    scad_model(
        name = name,
        three_d = three_d,
        file = tmpfile,
        deps = deps + [file],
    )

# TODO: create a screenshot rule for this
# def scad2png(scadfile, png_filename):
#     imgsize = '800, 800'
#     p = proc.check_call(
#         [
#             'openscad',
#             '--imgsize=%s' % imgsize, '--camera=-5.3,-4.3,5.5,75,0,326,80',
#             '--preview', scadfile, '-o', png_filename
#         ],
#         stdout=DEVNULL,
#         stderr=DEVNULL)
#     print('wrote %s' % png_filename)
