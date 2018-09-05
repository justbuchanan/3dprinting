load("//tools:tools.bzl", "solidpy_model")

filegroup(
    name = "nema17",
    srcs = [
        "utl.NEMA.scad",
    ],
    visibility = ["//visibility:public"],
)

solidpy_model(
    name = "demo",
    file = "demo.py",
    deps = [
        ":nema17",
    ],
)
