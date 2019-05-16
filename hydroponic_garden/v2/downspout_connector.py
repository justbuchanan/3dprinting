from solid import *
from solid.utils import *
import math
from tools.util import item_grid, Part, Connector, INC
import jigsaw

# This module provides a design for a 3d-printed endcap for vinyl downspout
# tubes to build a planting tray for hydroponics. The endcap is printed in two
# pieces that have a jigsaw connector to connect them together. The larger of
# the two pieces connects two downspout tubes and has a an embedded channel to
# allow water to flow between them.


# The final output will be in mm, so we define a conversion factor for working
# with inches.
inch = 25.4

# STL render resolution
fn = 100

# outer dimensions
downspout_outer_w = 78.7
h = 58.7
r = 15

# shelf dimensions
shelf_width = 33*inch
shelf_depth = 13.5*inch



def rrect(w, h, r):
    return union()(
        translate([0, r])(square([w, h-2*r])),
        translate([r, 0])(square([w-2*r, h])),
        translate([r,r])(circle(r)), # bottom right
        *[translate([x, y])(circle(r)) for x in [r, w-r] for y in [r, h-r]]
    )

# thickness of vinyl downspout walls
downspout_th = 2
class DownspoutProfile(Part):
    def __init__(self):
        super().__init__()
        th = downspout_th
        p = rrect(downspout_outer_w, h, r) \
              - translate([th,th])(rrect(downspout_outer_w-2*th, h-2*th, r-th))
        self.add(p)

DEFAULT_ENDCAP_BACK_TH = 2
# DEFAULT_ENDCAP_TOTAL_H = 10
class Endcap(Part):
    def __init__(self,
        w=downspout_outer_w,
        h=h,
        wall_th=1,
        wall_h = 8,
        back_th=DEFAULT_ENDCAP_BACK_TH,
        ):
        super().__init__()
        # w, h, r dimensions are for the *outside* of the downspout tube.
        # inner width = w - 2*th.

        total_z_ht = wall_h + back_th

        base = linear_extrude(total_z_ht)(
                    rrect(w+wall_th*2, h+wall_th*2, r+wall_th))

        # hollow out large middle portion
        dth = downspout_th + wall_th
        center_hollow = translate([wall_th+dth, wall_th+dth, back_th])(
                    linear_extrude(total_z_ht)(
                        rrect(w-dth*2, h-dth*2,r-dth)))

        # cut out profile for downspout
        downspout = translate([wall_th, wall_th, back_th])(
                        linear_extrude(total_z_ht)(
                            DownspoutProfile()))

        e = base - center_hollow - downspout
        self.add(e)
        self.con['main'] = Connector(
            [wall_th+w/2, wall_th+h/2, back_th],
            [0.01,0.01,1])

        # export variables for inspection
        self.back_th = back_th
        self.total_z_ht = total_z_ht
        self.h = h + 2*wall_th
        self.total_w = w + 2*wall_th
        self.wall_th = wall_th


downspout_spacing = (shelf_depth - 3*downspout_outer_w - 2*inch)/2
# print("downspout spacing: {}".format(downspout_spacing))

class Endcap180Connector(Part):
    # TODO: share with endcap()
    # thickness of connector wall
    def __init__(self,
        downspout_spacing=downspout_spacing,
        # wall_th = 1,
        endcap_th = 2,
        # water hole cut out of each endcap that connects to channel
        hole_r = 10,
        ):
        """
        Args:
          downspout_spacing: distance between the two downspouts
        """
        super().__init__(collect_subconnectors=False)


        # add two endcaps
        e1, e2 = Endcap(), Endcap()

        # center-to-center distance between the two endcaps.
        dx = downspout_outer_w + downspout_spacing - e1.wall_th*2

        # INC makes a slight overlap to embed endcaps into backing
        conn = translate([0, 0, -endcap_th+INC])(
                e1,
                translate([dx, 0])(
                    e2))


        # distance from back of wall to start of water hole/channel
        chan_wall_th = 3
        chan_w = 4
        chan_h = hole_r*2

        # thickness of main backing body
        backing_th = chan_wall_th*2 + chan_w # TODO calculate from chan_wall_th
        conn += translate([0, 0, -backing_th])(
                    linear_extrude(backing_th)(
                        rrect(e1.total_w+dx, e1.h, r+e1.wall_th)))

        # add jigsaw connector
        conn += translate([dx, 0, -backing_th])(
            jigsaw_piece(dx=dx, th=backing_th, odd=True))

        # water channel holes in back of endcaps
        for x in [e1.total_w/2, e1.total_w/2 + dx]:
            conn -= translate([x, e1.h/2, -backing_th+chan_wall_th])(
                        cylinder(r=hole_r, h=100))

        # horizontal channel connecting two water holes
        conn -= translate([e1.total_w/2, (e1.h-chan_h)/2, -chan_wall_th])(
                rotate([0, 90, 0])(
                    linear_extrude(dx)(
                        square([chan_w, chan_h]))))


        conn = render()(conn)

        self.add(color("gray")(conn))
        self.con['left'] = Connector([downspout_outer_w/2, h/2, 0.001], [.001,.001,1])
        self.con['right'] = Connector([downspout_outer_w/2 + dx, h/2, 0], [0.001,.001,1])

        # export variables
        self.backing_th = backing_th
        self.dx = dx


# Leave some extra space at the ends
downspout_tube_len = shelf_width - 2*inch

class Downspout(Part):
    def __init__(self,
        l=downspout_tube_len,

        has_holes=True,
        hole_spacing=20,
        hole_r=1*inch
        ):
        super().__init__()
        d = color("white")(
                linear_extrude(l)(
                    DownspoutProfile()))

        if has_holes:
            n = math.floor((l - hole_spacing) / (hole_spacing + hole_r*2))
            sp = (l - 2*n*hole_r) / (n + 1)
            # print("n = %d" % n)
            for i in range(n):
                d -= rotate([0,0,0])(rotate([-90, 0, 0])(
                        translate([downspout_outer_w/2, -(sp + hole_r + i*(sp+hole_r*2)), h/2])(
                            cylinder(r=hole_r, h=100))))


        self.add(color("white")(render()(d)))

        self.con['back'] = Connector([downspout_outer_w/2, h/2, 0], [0.001,0.001,1])
        self.con['front'] = Connector([downspout_outer_w/2, h/2, l], [0.001,0.001,-1]) #/////////////////////////////////

def jigsaw_piece(dx, th, peg_w=10, odd=False):
    # print("jigsaw({}, {}".format(dx, th))
    e = Endcap(back_th=DEFAULT_ENDCAP_BACK_TH+th)
    jig = jigsaw.jigsaw(e.h+2*INC, max_peg_cycle_ht=14, peg_w=peg_w, odd=odd)
    # total w is width of piece up until the end of the pegs
    # note that only half of peg length is counted
    rect_w = dx/2 - peg_w / 2
    return translate([e.total_w/2, 0, 0])(
            union()(
                cube([rect_w, e.h, th]),
                translate([rect_w-INC, 0, 0])(
                    linear_extrude(th)(
                        jig))))


class EndcapWithPegs(Part):
    def __init__(self,
        # dimensions are based on the 180 connector that it connects to
        e180 = Endcap180Connector(),
        ):
        super().__init__()
        self.add(render()(
            Endcap(back_th=DEFAULT_ENDCAP_BACK_TH+e180.backing_th-2),
            jigsaw_piece(dx=e180.dx, th=e180.backing_th),
        ))



def jigsaw_test_piece(odd=True):
    return render()(jigsaw_piece(30, 10, odd=odd))

def both_jigsaw_test_pieces():
    return union()(
            render()(
                jigsaw_test_piece(odd=True)),
            translate([130, 60])(
                rotate([0,0,180])(
                    render()(
                        jigsaw_test_piece(odd=False)))))


if __name__ == '__main__':
    model = item_grid([
        ("downspout profile", DownspoutProfile()),
        ("with pegs", EndcapWithPegs()),
        ("endcap 180", Endcap180Connector()),
        ("downspout", rotate([180,0,0])(
                        Downspout())),
        ("jigsaw demo", jigsaw_test_piece()),
        ("jigsaw demo 2", both_jigsaw_test_pieces()),
    ], spacing=220)

    # write scad
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
