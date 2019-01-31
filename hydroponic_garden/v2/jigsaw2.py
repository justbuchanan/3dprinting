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


def jigsaw(h, desired_cycle_wid=12, peg_func=rect_peg, opp=False):
    # n = 3
    n = math.floor(h / desired_cycle_wid)
    dy = h / n

    n = 7

    peg_w = 10
    part_w = 3
    total_w = part_w + peg_w

    print("jigsaw: dy: {dy}; n: {n}; peg_w: {peg_w}".format(dy=dy, n=n, peg_w=peg_w))

    part = square([part_w, h])

    # Shift so that opposing parts intermesh correctly
    # Opposing pegs are spaced 1/4*dy offset from one another
    y_shift_mul = 1/4 if opp else -1/4
    pegs = union()([
        translate([part_w-INC,dy*(i+y_shift_mul)])(
            peg_func(peg_w,dy))
        for i in range(n)])

    # TODO: intersect with bounding rect
    return color("red")(intersection()(
        part + pegs,
        square([total_w, h]),
        ))

def jigsaw_test(**kwargs):
    left = jigsaw(opp=False, **kwargs)
    right = jigsaw(opp=True, **kwargs)

    R = translate([16,kwargs['h']])(rotate(180)(right))

    L = render()(left - R)
    R = render()(R - left)
    # R = 

    return color("red")(L) + color("green")(R)

def both(h):
    return linear_extrude(6)(union()(
            # an interlocking set of demo pieces
            translate([20,0])(
                jigsaw(h=h, peg_func=sine_peg)),
            jigsaw(h=h,peg_func=sine_peg, opp=True)))

h = 40
model = item_grid([
    ("demo", both(h)),
    ("test", jigsaw_test(h=h,peg_func=sine_peg)),
    ("peg", sine_peg(peg_w=10, dy=13)),
])

if __name__ == '__main__':
    # write scad
    fn = 100
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
