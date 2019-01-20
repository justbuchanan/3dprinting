#!/usr/bin/env python2

# Simple script to render cadquery models via the cqgi interface
# Usage: cq_render.py --file mymodel.py --out_dir output/mymodel/

from cadquery import cqgi
import argparse
import sys
import os

parser = argparse.ArgumentParser(
    description=
    "Utility to render cqparts models to gltf. Each model in a given file is rendered to a separate gltf."
)
parser.add_argument(
    '--file', required=True, help="cqparts python file to render models from")
parser.add_argument('--outfile', required=True, help="Output file")
args = parser.parse_args()

fname = args.file

with open(fname, 'r') as f:
    build_result = cqgi.parse(f.read()).build()

print("Build results: %s" % str(build_result.results))

for res in build_result.results:
    asm = res.shape
    clsname = asm.__class__.__name__

    outfile = args.outfile

    outtype = 'gltf'
    f, ext = os.path.splitext(outfile)
    if len(ext) > 0:
        outtype = ext[1:]

    print("Writing '%s' object to '%s'" % (clsname, outfile))
    asm.exporter(outtype)(outfile)
