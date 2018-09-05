load("//tools:tools.bzl", "solidpy_model")

solidpy_model(
    name = "planter",
    file = "round_rect_pot.py",
    py_deps = [":util"],
    scad_resolution = 100,
)

solidpy_model(
    name = "planter_old",
    file = "planter_old.py",
    py_deps = [":util"],
    scad_resolution = 100,
)

py_library(
    name = "util",
    srcs = ["util.py"],
)
