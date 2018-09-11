package(default_visibility = ["//visibility:public"])

load("//tools:openscad.bzl", "scad_model")

filegroup(
    name = "endcap_stl",
    srcs = ["downspout-endcap/2x3_End_Cap.stl"],
)

scad_model(
    name = "net_pot",
    file = "net-pot/net-pot.scad",
)

filegroup(
    name = "threads",
    srcs = glob(["threads/*.scad"]),
)
