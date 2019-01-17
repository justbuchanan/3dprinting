package(default_visibility = ["//visibility:public"])

load("//tools:openscad.bzl", "scad_part")

filegroup(
    name = "all_stls",
    srcs = [
        ":hose_fitting_drain_1cm_stl",
        ":hose_fitting_main_stl",
        ":hose_fitting_nut_stl",
        ":hose_fitting_source_2cm_stl",
        ":splitter_v2_inlet_stl",
        ":splitter_v2_main_stl",
        "//hydroponic_garden/thingiverse:endcap_stl",
        "//hydroponic_garden/thingiverse:net_pot_stl",
    ],
)

########## Splitter v1

scad_part(
    name = "splitter_v1",
    file = "splitter_v1.scad",
    toplevel = "splitter();",
    deps = [":hose_fitting_scad"],
)

########## Splitter v2

splt2_scaddeps = [
    ":hose_fitting_scad",
    "//hydroponic_garden/thingiverse:threads",
]

scad_part(
    name = "splitter_v2_inlet",
    file = "splitter_v2.scad",
    toplevel = "splitter();",
    deps = splt2_scaddeps,
)

scad_part(
    name = "splitter_v2_main",
    file = "splitter_v2.scad",
    toplevel = "splitter_input_tip();",
    deps = splt2_scaddeps,
)

########## Hose fitting

filegroup(
    name = "hose_fitting_scad",
    srcs = ["hose_fitting.scad"],
    visibility = ["//visibility:public"],
)

hf_scaddeps = [
    "//hydroponic_garden/thingiverse:threads",
]

scad_part(
    name = "hose_fitting_demo",
    file = "hose_fitting.scad",
    toplevel = """
main();
translate([-20,-20,0]) fitting_nut();
translate([20,20,0]) source_plug();""",
    deps = hf_scaddeps,
)

scad_part(
    name = "hose_fitting_drain_1cm",
    file = "hose_fitting.scad",
    toplevel = "plug();",
    deps = hf_scaddeps,
)

scad_part(
    name = "hose_fitting_source_2cm",
    file = "hose_fitting.scad",
    toplevel = """
$fn = 100;
source_plug(water_level=2.0*cm);""",
    deps = hf_scaddeps,
)

scad_part(
    name = "hose_fitting_nut",
    file = "hose_fitting.scad",
    toplevel = "fitting_nut();",
    deps = hf_scaddeps,
)

scad_part(
    name = "hose_fitting_main",
    file = "hose_fitting.scad",
    toplevel = "main();",
    deps = hf_scaddeps,
)
