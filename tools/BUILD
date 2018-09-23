package(default_visibility = ["//visibility:public"])

load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "util_py",
    srcs = [
        "util.py",
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "solidpy2scad",
    srcs = ["solidpy2scad.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":util_py",
        requirement("solidpython"),
        requirement("numpy"),
    ],
)

py_binary(
    name = "cq_render",
    srcs = ["cq_render.py"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "openscad",
    srcs = ["openscad.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "CuraEngine",
    srcs = ["CuraEngine.sh"],
    visibility = ["//visibility:public"],
)

py_runtime(
    name = "python-2-or-3",
    files = [],
    interpreter = "python-2-or-3.sh",
)
