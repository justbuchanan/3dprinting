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
    default_python_version = "PY3",
    srcs_version = "PY3ONLY",
    visibility = ["//visibility:public"],
    deps = [
        ":util_py",
        requirement("solidpython"),
        requirement("numpy"),
    ],
)

sh_binary(
    name = "CuraEngine",
    srcs = ["CuraEngine.sh"],
    visibility = ["//visibility:public"],
)
