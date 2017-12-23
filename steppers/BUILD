load("//tools:tools.bzl", "solidpy_model")

filegroup(
    name = "nema17",
    srcs = [
        "utl.NEMA.scad",
    ],
    visibility = ["//visibility:public"],
)

solidpy_model(
    name = "robot",
    file = "robot.py",
    deps = [
        ":nema17",
    ],
)
