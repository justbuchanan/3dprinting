# from solid import circle, translate, cube
import math
from solid.utils import *
from tools.util import item_grid, Part
import numpy as np

INC = 0.001


def sine_wave(w=20, amp = 1.5, dy=20):
    endangle = 2*pi
    t2w = w/endangle

    # return cube(1)
    def wave(theta, dy):
        return (theta*t2w, -math.sin(theta)*amp+dy)

    vspace = dy/2

    npoint = 100

    return translate([0, 0])(polygon([
        *[
            wave(theta,dy=vspace)
            for theta in np.linspace(0, endangle, num=npoint)
        ],
        *[
            (theta*t2w,wave(-theta,dy=0)[1])
            for theta in np.linspace(endangle, 0, num=npoint)
        ],
        ]))

def sine_peg(peg_w, dy, opp=False):
    return sine_wave(w=peg_w, dy=dy)

def rect_peg(peg_w, dy, opp=False):
    return square([peg_w, dy/2])


def jigsaw(h=100, peg_func=rect_peg, xgap=0.2):
    n = 5
    dy = h / n

    peg_w = 20
    part_w = 1
    total_w = part_w + peg_w

    part = square([part_w, h])

    pegs = union()([translate([part_w-INC,dy*i])(peg_func(peg_w,dy)) for i in range(n)])
    left = color("red")(
            part,
            pegs,
        )
    right = color("green")(
        translate([total_w+part_w, h])(
            rotate([0,0,180])(
                part,
                pegs
                )))

    L = left - right
    R = right - left

    return L + translate([xgap,0])(R)


model = union()(
    jigsaw(),
    translate([50,0])(jigsaw(peg_func=sine_peg,xgap=0)),
    translate([-30,0])(sine_wave()),
)

if __name__ == '__main__':
    # h = 63.7
    # model = item_grid([
    #     ("demo part", demo_part()),
    #     ("jigsaw", Jigsaw2(h)),
    # ], spacing=100)

    # write scad
    fn = 100
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
