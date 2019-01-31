# from solid import circle, translate, cube
import math
from solid.utils import *
from tools.util import item_grid, Part


# Returns a 2d profile that should be *cut out* of the part.
# Place it it a distance W before the end and subtract.
class Jigsaw2(Part):
    def __init__(self,
        h,
        r1 = 4, # big circle of peg
        # center-to-center distance between big circle and small circle
        joint_w = 7,
        opp=True,
        # extra radius is added to negative peg. This allows them to actually fit together.
        gap_extra_r = 0.1,
        ):
        super().__init__()

        # r2 = r1 / 2
        dy = r1 * 3
        n = math.floor(h / dy)

        dy = h / n
        r1 = dy / 3
        r2 = r1 / 2
        dx = r1 * 2
        start_y = -dy/2 if opp else 0
        n += 1

        # export variables
        self.w = r1*2 + joint_w

        self.add(translate([r1,0,0])(union()(*[
                translate([0, start_y + dy * (i+ 1/2)])(
                    hull()(
                        circle(r1+gap_extra_r),
                        translate([joint_w, 0])(
                            circle(r2+gap_extra_r))))
                    for i in range(n)
                ],

                translate([joint_w, 0])(
                    difference()(
                        square([20, h]),
                        *[translate([0, start_y+i*dy])(
                            circle(r1))
                        for i in range(n)],
                    )
                )
            )
        ))


def demo_part():
    return square([20, h]) - Jigsaw2(h)


if __name__ == '__main__':
    h = 63.7
    model = item_grid([
        ("demo part", demo_part()),
        ("jigsaw", Jigsaw2(h)),
    ], spacing=100)

    # write scad
    fn = 100
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
