import math
from solid.utils import *
from tools.util import item_grid, Part
import numpy as np

INC = 0.001


# tol: subtracted from the y on each side.
def sine_peg(peg_w, dy, amp=1.5, opp=False, tol=0.05):
    endangle = 2*pi
    t2w = peg_w/endangle

    # return cube(1)
    def wave(theta, dy):
        return (theta*t2w, -math.sin(theta)*amp+dy)

    vspace = dy/2 - tol*2

    npoint = 100

    return translate([0, tol])(polygon([
        *[
            wave(theta,dy=vspace)
            for theta in np.linspace(0, endangle, num=npoint)
        ],
        *[
            (theta*t2w,wave(-theta,dy=0)[1])
            for theta in np.linspace(endangle, 0, num=npoint)
        ],
        ]))

def rect_peg(peg_w, dy, opp=False):
    return square([peg_w, dy/2])


def jigsaw(h=100, peg_func=rect_peg, xgap=0.2, opp=False):
    n = 3
    dy = h / n

    n = 7

    peg_w = 10
    part_w = 3
    total_w = part_w + peg_w

    part = square([part_w, h])

    dddyyy = 1/4 if opp else -1/4

    pegs = union()([
        translate([part_w-INC,dy*(i+dddyyy)])(
            peg_func(peg_w,dy))
        for i in range(n)])
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

    L = left #- right
    R = right #- left

    # TODO: intersect with bounding rect
    return color("red")(intersection()(
        L,
        square([total_w, h]),
        ))

    # return L# + translate([xgap,0])(R)

h = 40
model = linear_extrude(6)(union()(
    # jigsaw(),
    translate([50,0])(jigsaw(h=h,peg_func=sine_peg,xgap=0)),
    jigsaw(h=h,peg_func=sine_peg,xgap=0, opp=True),
    # translate([-30,0])(sine_wave()),
))

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
