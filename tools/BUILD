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
    name = "render",
    srcs = ["render.py"],
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
    name = "openscad",
    srcs = ["openscad.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "CuraEngine",
    srcs = ["CuraEngine.sh"],
    visibility = ["//visibility:public"],
)
