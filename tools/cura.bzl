def _slice_stl_to_gcode(ctx):
    # TODO: do better
    PRINTER_DEF = "/usr/share/cura/resources/definitions/prusa_i3.def.json"

    ctx.actions.run(
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
