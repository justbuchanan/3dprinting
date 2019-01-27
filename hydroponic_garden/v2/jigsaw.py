from solid import *
from math import sin, cos, pi
import math
from solid.utils import *
# from downspout_connector import *
# from solid.utils import *
# from tools.util import *

fn = 100

w = 78.7
h = 58.7

r1 = 4
r2 = r1 / 2
n = 6
dy = r1 * 3
dx = r1 * 2
joint_w = 7 # center-to-center distance between big circle and small circle
start_y = 2
h += 5

protrusion_len = r1/2 + r1 + joint_w

# TODO: hole should be bigger than peg

model = intersection()(
    # cut off everything outside this rect:
    square([w + joint_w * 100, h]),

    # Create positive pegs and cut out negatives
    difference()(
        # positive pegs
        union()(
            square([w, h]),
            *[
                translate([w, dy * i + start_y])(
                    hull()(
                        circle(r1),
                        translate([joint_w, 0])(
                            circle(r1))))
                for i in range(n)
            ],
        ),

        # cut out negative "pegs"
        union()(*[
            translate([w, start_y + dy * (i - 1/2)])(
                hull()(
                    circle(r1),
                    translate([joint_w, 0])(
                        circle(r2))))
            for i in range(n)
        ])))

# TODO: middle of joint
# visualize center of connectors
model += color("blue")(
            translate([w+protrusion_len/2, 0, 0])(
                square([1, h])))

if __name__ == '__main__':
    # write scad
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
