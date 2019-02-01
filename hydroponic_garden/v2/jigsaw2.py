import math
from solid.utils import *
from tools.util import item_grid, Part, INC
import numpy as np


# tol: subtracted from the y on each side. Tried 0.05 initially. They were pretty tight
# also tried tol=0.1, seemed slightly loose
def sine_peg(peg_w, peg_cycle_ht, amp=1.5, opp=False, tol=0.05):
    endangle = 2*pi
    t2w = peg_w/endangle

    # return cube(1)
    def wave(theta, peg_cycle_ht):
        return (theta*t2w, -math.sin(theta)*amp+peg_cycle_ht)

    vspace = peg_cycle_ht/2 - tol*2

    npoint = 100

    return translate([0, tol])(polygon([
        *[
            wave(theta,peg_cycle_ht=vspace)
            for theta in np.linspace(0, endangle, num=npoint)
        ],
        *[
            (theta*t2w,wave(-theta,peg_cycle_ht=0)[1])
            for theta in np.linspace(endangle, 0, num=npoint)
        ],
        ]))


def rect_peg(peg_w, peg_cycle_ht, opp=False):
    return square([peg_w, peg_cycle_ht/2])


def jigsaw(h, peg_w=10, max_peg_cycle_ht=12, peg_func=sine_peg, opp=False):
    # Calculate number of pegs so that we're close, but not over our desired peg height
    n = math.floor(h / max_peg_cycle_ht)
    peg_cycle_ht = h / n
    n = round(h / peg_cycle_ht)
    # Add an extra one to ensure we're covered. Any excess will be trimmed off at the end
    n = n + 1

    # print("jigsaw: peg_cycle_ht: {peg_cycle_ht}; n: {n}; peg_w: {peg_w}".format(peg_cycle_ht=peg_cycle_ht, n=n, peg_w=peg_w))

    # Shift so that opposing parts intermesh correctly
    # Opposing pegs are spaced 1/4*peg_cycle_ht offset from one another
    y_shift_mul = 1/4 if opp else -1/4
    return intersection()(
        # all of the pegs
        union()([
            translate([0, peg_cycle_ht * (i+y_shift_mul)])(
                peg_func(peg_w, peg_cycle_ht))
            for i in range(n)]
        ),

        # trim pegs to fit in this rect
        square([peg_w, h]),
    )

def jigsaw_test(**kwargs):
    left = jigsaw(opp=False, **kwargs)
    right = translate([kwargs['peg_w'], kwargs['h']])(
                rotate(180)(
                    jigsaw(opp=True, **kwargs)))

    L = left - right
    R = right - left

    return color("red")(render()(L)) + color("green")(render()(R))

def both(h):
    rr = translate([-3, 0])(square([3+INC, h]))
    return linear_extrude(6)(union()(
            # an interlocking set of demo pieces
            translate([30,h])(rotate(180)(
                rr + jigsaw(h=h, peg_func=sine_peg))),
            rr + jigsaw(h=h,peg_func=sine_peg, opp=True)))

h = 40
model = item_grid([
    ("demo", both(h)),
    ("test", jigsaw_test(h=h, peg_w=10, peg_func=sine_peg)),
    ("peg", sine_peg(peg_w=10, peg_cycle_ht=13)),
    ("rect jig test", jigsaw_test(h=h, peg_w=10, peg_func=rect_peg)),
    ("rect jig", jigsaw(h=h)),
])

if __name__ == '__main__':
    # write scad
    fn = 100
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
