#!/usr/bin/env python3

import os
import sys
from solid import *

import argparse
import subprocess as proc
from subprocess import DEVNULL
import os
import imp


# Imports the python file at the given path and reads the "model" variable from
# it.
def load_model(filepath):
    sys.path.append(os.getcwd())
    module = imp.load_source('module', filepath)
    return module.model


def render_model(scadmodel, outfile, header):
    # save openscad file
    print('writing file: %s' % outfile)
    with open(outfile, 'w') as f:
        f.write(scad_render(scadmodel, file_header=header))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'Render a solidpython model/file to openscad.')
    parser.add_argument('file')
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--header', type=str, default='$fn=30;', help="Scad file header. May include $fn setting.")
    parser.add_argument('--toplevel_expr', type=str, default='model', help="")
    args = parser.parse_args()

    machine = load_model(args.file)

    scad_filename = args.output
    render_model(machine, scad_filename, header=args.header)
