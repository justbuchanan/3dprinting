#!/usr/bin/env bash

# Choose the python interpreter based on the file's shebang. This allows for
# using python2 executables along python3 in the same bazel repo.

# https://groups.google.com/forum/#!topic/bazel-discuss/nVQ48R94S_8
# https://github.com/bazelbuild/bazel/issues/3517#issuecomment-420501895

set -e

echo "base path $BASE_PATH"

if head -n 1 "$1" | grep -q python3; then
  exec "$BASE_PATH"/usr/bin/python3 "$@"
else
  exec "$BASE_PATH"/usr/bin/python2 "$@"
fi
