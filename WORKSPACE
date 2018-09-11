new_git_repository(
    name = "scad_utils",
    build_file_content = """
filegroup(
    name = "scad_utils",
    srcs = glob(["*.scad"]),
    visibility = ["//visibility:public"],
)""",
    commit = "484d39bc2fd19cf6903c8e92e01af40a77276e66",
    remote = "https://github.com/OskarLinde/scad-utils",
)

new_git_repository(
    name = "mcad",
    build_file_content = """
filegroup(
    name = "mcad",
    srcs = glob(["*.scad"]),
    visibility = ["//visibility:public"],
)""",
    commit = "818265f4a6f78e1e7e258228c0763c345c1fdc04",
    remote = "https://github.com/openscad/MCAD",
)

git_repository(
    name = "io_bazel_rules_python",
    commit = "44711d8ef543f6232aec8445fb5adce9a04767f9",
    remote = "https://github.com/bazelbuild/rules_python.git",
)

load("@io_bazel_rules_python//python:pip.bzl", "pip_import", "pip_repositories")

pip_repositories()

# This rule translates the specified requirements.txt into
# @py_deps//:requirements.bzl, which itself exposes a pip_install method.
pip_import(
    name = "py_deps",
    requirements = "//third_party:requirements.txt",
)

# Load the pip_install symbol for py_deps, and create the dependencies'
# repositories.
load("@py_deps//:requirements.bzl", "pip_install")

pip_install()
