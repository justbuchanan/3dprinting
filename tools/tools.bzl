# utilities for working with openscad and solidpython models

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

# instead of using the "model" variable from the python file as solidpy_to_scad
# does, this accepts a "toplevel" argument that lets you define what to render
# as a snippet of python that's evaluated within the context of the file.
# TODO: integrate this with the stl, png, etc outputs
# TODO: evaluate snippet in python, not scad
def scad_part(name, file, toplevel, deps = []):
    tmpfile = name + ".scad"
    part_scad_file(name = name + "_scad", file = file, output = tmpfile, toplevel = toplevel)

    scad_render(
        name = name + "_stl",
        file = tmpfile,
        out = name + ".stl",
        deps = deps + [file],
    )

def _slice_stl_to_gcode(ctx):
    # TODO: do better
    PRINTER_DEF = "/usr/share/cura/resources/definitions/prusa_i3.def.json"

    ctx.action(
        inputs = ctx.files.file,
        outputs = [ctx.outputs.gcode_out],
        executable = ctx.executable._cura_engine_tool,
        arguments = [
            "slice",
            "-v",
            "-j",
            PRINTER_DEF,
            "-e1",
            "-s",
            "infill_line_distance=0",
            "-e0",
            "-l",
            ctx.file.file.path,
            "-o",
            ctx.outputs.gcode_out.path,
        ],
    )

slice_stl_to_gcode = rule(
    implementation = _slice_stl_to_gcode,
    attrs = {
        "file": attr.label(allow_files = True, mandatory = True, single_file = True),
        "gcode_out": attr.output(mandatory = True),
        "_cura_engine_tool": attr.label(cfg = "host", executable = True, allow_files = True, default = Label("//tools:CuraEngine")),
    },
)

def solidpy_model(name, file, deps = [], py_deps = [], scad_resolution = 100):
    solidpy_to_scad(
        name = name + "_scad",
        file = file,
        out = name + ".scad",
        bom_out = name + "_bom.txt",
        deps = deps,
        py_deps = py_deps,
        resolution = scad_resolution,
    )
    scad_render(
        name = name + "_stl",
        file = name + ".scad",
        out = name + ".stl",
        deps = deps,
    )
    scad_render(
        name = name + "_svg",
        file = name + ".scad",
        out = name + ".svg",
        deps = deps,
    )
    slice_stl_to_gcode(
        name = name + "_gcode",
        file = name + "_stl",
        gcode_out = name + ".gcode",
    )
