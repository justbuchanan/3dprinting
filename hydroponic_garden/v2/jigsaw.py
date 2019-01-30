from solid import *
from math import sin, cos, pi
import math
from solid.utils import *
# from solid.utils import *
from tools.util import item_grid, Part


# extra radius added to negative peg. This allows them to actually fit together.
# gap_extra_r = 0.2
# TODO: hole should be bigger than peg

# def jigsaw(
#     h,
#     w = 78.7,
#     r1 = 4,
#     joint_w = 7, # center-to-center distance between big circle and small circle
#     start_y = 2,
#     ):
#     r2 = r1 / 2
#     dy = r1 * 3
#     dx = r1 * 2
#     n = 6

#     # horizontal distance from end of negative peg to end of positive peg
#     protrusion_len = r1/2 + r1 + joint_w

#     return intersection()(
#         # cut off everything outside this rect:
#         square([w + joint_w * 100, h]),

#         # create positive pegs and cut out negatives
#         difference()(
#             # positive pegs
#             union()(
#                 square([w, h]),
#                 *[
#                     translate([w, dy * i + start_y])(
#                         hull()(
#                             circle(r1),
#                             translate([joint_w, 0])(
#                                 circle(r1))))
#                     for i in range(n)
#                 ],
#             ),

#             # cut out negative "pegs"
#             union()(*[
#                 translate([w, start_y + dy * (i - 1/2)])(
#                     hull()(
#                         circle(r1),
#                         translate([joint_w, 0])(
#                             circle(r2))))
#                 for i in range(n)
#             ])))


# Returns a 2d profile that should be *cut out* of the part.
# Place it it a distance W before the end and subtract.
class Jigsaw2(Part):
    def __init__(self,
        h,
        r1 = 4, # big circle of peg
        # center-to-center distance between big circle and small circle
        joint_w = 7,
        # blue_line=True,
        opp=True,
        ):
        super().__init__()

        # r2 = r1 / 2
        dy = r1 * 3
        n = math.floor(h / dy)

        dy = h / n
        r1 = dy / 3
        r2 = r1 / 2

        dx = r1 * 2

        n += 1

        start_y = -dy/2 if opp else 0


        m = union()(*[
                translate([r1, start_y + dy * (i+ 1/2)])(
                    hull()(
                        circle(r1),
                        translate([joint_w, 0])(
                            circle(r2))))
                for i in range(n)
            ],

            translate([r1+joint_w, 0])(
                difference()(
                    square([20, h]),
                    *[translate([0, start_y+i*dy])(circle(r1)) for i in range(n)],
                )
            )
        )

        # m += color("blue")(square([r1+r1+joint_w, 100]))

        # TODO: height of endcap part is not right. It's also not at (0, 0) dammit

        # # TODO: middle of joint
        # # vertical line visualize center of connectors
        # if blue_line:
        #     protrusion_len = r1/2 + r1 + joint_w
        #     m += color("blue")(
        #             translate([protrusion_len/2, 0, 1])(
        #                 square([0.1, h])))

        self.add(m)

        # export variables
        self.w = r1*2 + joint_w


def part2():
    return square([20, h]) - Jigsaw2(h)


if __name__ == '__main__':
    h = 63.7
    model = item_grid([
        ("part2", part2()),
        # ("part2", part2()),
        # ("jigsaw", jigsaw(h)),
        ("jigsaw2", Jigsaw2(h)),
    ], spacing=100)

    # write scad
    fn = 100
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
