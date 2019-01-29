from solid import *
from math import sin, cos, pi
import math
from solid.utils import *
# from solid.utils import *
from tools.util import item_grid


# extra radius added to negative peg. This allows them to actually fit together.
# gap_extra_r = 0.2
# TODO: hole should be bigger than peg

def jigsaw(
    h,
    w = 78.7,
    r1 = 4,
    joint_w = 7, # center-to-center distance between big circle and small circle
    start_y = 2,
    ):
    r2 = r1 / 2
    dy = r1 * 3
    dx = r1 * 2
    n = 6

    # horizontal distance from end of negative peg to end of positive peg
    protrusion_len = r1/2 + r1 + joint_w

    return intersection()(
        # cut off everything outside this rect:
        square([w + joint_w * 100, h]),

        # create positive pegs and cut out negatives
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

# Returns a 2d profile that should be *cut out* of the part.
# Place it it a distance W before the end and subtract.
def jigsaw2(
    #
    #   ***  *
    #  *   *  * **
    #  *   *    **
    #   ***
    #
    #
    #
    #
    h,
    w = 78.7,
    r1 = 4, # big circle of peg
    # center-to-center distance between big circle and small circle
    joint_w = 7,
    blue_line=True,
    ):
    r2 = r1 / 2
    dy = r1 * 3
    dx = r1 * 2
    n = math.ceil(h / dy)
    # w = joint_w + r1*2
    # return square([20, h])
    m = union()(*[
        translate([r1, dy * (i+1 - 1/2)])(
            hull()(
                circle(r1),
                translate([joint_w, 0])(
                    circle(r2))))
        for i in range(n)
    ]) + translate([r1+joint_w, 0])(
            difference()(
                square([20, h]),
                *[translate([0, i*dy])(circle(r1)) for i in range(n)],
                ))
    # TODO: middle of joint
    # vertical line visualize center of connectors
    if blue_line:
        protrusion_len = r1/2 + r1 + joint_w
        m += color("blue")(
                translate([w+protrusion_len/2, 0, 1])(
                    square([0.1, h])))
    return m



def part2():
    return square([20, h]) - jigsaw2(h)

h = 63.7
model = item_grid([
    ("part2", part2()),
    # ("part2", part2()),
    ("jigsaw", jigsaw(h)),
    ("jigsaw2", jigsaw2(h)),
], spacing=100)


if __name__ == '__main__':
    # write scad
    fn = 100
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
