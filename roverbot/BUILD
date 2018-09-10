load("//tools:solidpy.bzl", "solidpy_model")

solidpy_model(
    name = "robot",
    file = "robot.py",
    py_deps = [
        "//tools:util_py",
    ],
    scad_resolution = 100,
    deps = [
        "@mcad",
        "@scad_utils",
    ],
)
