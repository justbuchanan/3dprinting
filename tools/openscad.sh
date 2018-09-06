#!/usr/bin/env bash

# A stub that allows bazel to use the system-installed openscad.
# TODO: pull the binary into the bazel workspace for hermeticity

set -e

openscad $@
