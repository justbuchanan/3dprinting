from solid import *
import math
from solid.utils import *
from tools.util import *
import jigsaw2


in2mm = 25.4

fn = 100

# outer dimensions
DOWNSPOUT_OUTER_W = 78.7
h = 58.7
r = 15

# shelf dimensions
shelf_width = 33*in2mm
shelf_depth = 13.5*in2mm


# hexagonal hole pattern
def hatch(sz=[100,100], r=2, wall_th=1):
    h = square(sz)
    dx = r*2*.866 + wall_th
    dy = r*1.5 + wall_th

    holes = union()
    for i in range(ceil(sz[0]/r)):
        for j in range(ceil(sz[1]/r)):
            # shirt alternate layers horizontally relative to eachother
            xshift = r if (j % 2 == 0) else 0
            # cut out a hexagon at each location
            holes += translate([i*dx+xshift, j*dy])(
                rotate(30)(circle(r=r, segments=6)))
    return h - holes



def rrect(w, h, r):
    return union()(
        translate([0, r])(square([w, h-2*r])),
        translate([r, 0])(square([w-2*r, h])),
        translate([r,r])(circle(r)), # bottom right
        *[translate([x, y])(circle(r)) for x in [r, w-r] for y in [r, h-r]],
    )

# thickness of vinyl downspout walls
downspout_th = 2
class DownspoutProfile(Part):
    def __init__(self):
        super().__init__()
        th = downspout_th
        p = rrect(DOWNSPOUT_OUTER_W, h, r) \
              - translate([th,th])(rrect(DOWNSPOUT_OUTER_W-2*th, h-2*th, r-th))
        self.add(p)

DEFAULT_ENDCAP_BACK_TH = 2
# DEFAULT_ENDCAP_TOTAL_H = 10
class Endcap(Part):
    def __init__(self,
        w=DOWNSPOUT_OUTER_W,
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


downspout_spacing = (shelf_depth - 3*DOWNSPOUT_OUTER_W - 2*in2mm)/2
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
        dx = DOWNSPOUT_OUTER_W + downspout_spacing - e1.wall_th*2

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
            jigsaw_piece(dx=dx, th=backing_th, opp=True))

        # water channel holes in back of endcaps
        for x in [e1.total_w/2, e1.total_w/2 + dx]:
            conn -= translate([x, e1.h/2, -backing_th+chan_wall_th])(
                        cylinder(r=hole_r, h=100))

        # horizontal channel connecting two water holes
        conn -= translate([e1.total_w/2, (e1.h-chan_h)/2, -chan_wall_th])(
                rotate([0, 90, 0])(
                    linear_extrude(dx)(
                        square([chan_w, chan_h]))))

        # # add cross-hatch filter/screen to entry holes
        # # TODO: make this a dome? this flat bridge currently doesn't print well
        # screen_th=2
        # for x in [0, dx]:
        #     conn += translate([w/2+wall_th - hole_r*1.5 + x, h/2+wall_th-hole_r*1.5, -screen_th])(
        #                 linear_extrude(screen_th)(
        #                     hatch(sz=[hole_r*3, hole_r*3], r=2, th=1.2)))


        conn = render()(conn)

        self.add(color("gray")(conn))
        self.con['left'] = Connector([DOWNSPOUT_OUTER_W/2, h/2, 0.001], [.001,.001,1])
        self.con['right'] = Connector([DOWNSPOUT_OUTER_W/2 + dx, h/2, 0], [0.001,.001,1])

        # export variables
        self.backing_th = backing_th
        self.dx = dx


downspout_chunk_len = shelf_width - 2*in2mm

class Downspout(Part):
    def __init__(self,
        l=downspout_chunk_len,

        has_holes=True,
        hole_spacing=20,
        hole_r=1*in2mm
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
                        translate([DOWNSPOUT_OUTER_W/2, -(sp + hole_r + i*(sp+hole_r*2)), h/2])(
                            cylinder(r=hole_r, h=100))))


        self.add(color("white")(render()(d)))

        self.con['back'] = Connector([DOWNSPOUT_OUTER_W/2, h/2, 0], [0.001,0.001,1])
        self.con['front'] = Connector([DOWNSPOUT_OUTER_W/2, h/2, l], [0.001,0.001,-1]) #/////////////////////////////////

def shelf_plumbing():
    c = Endcap180Connector()
    d1 = Downspout()
    d2 = Downspout()

    asm = c
    asm += attach(c.con['right'], d1.con['back'])(d1)
    asm += attach(c.con['left'], d2.con['back'])(d2)

    c2 = Endcap180Connector()
    asm += attach(d1.con['front'], c2.con['left'])(c2)

    # TODO: attachments aren't smart enough to do this :(
    # d3 = Downspout()
    # asm += attach(c2.con['right'], d3.con['front'])(d3)

    # asm = cube()
    return asm

# class EndcapWithHole(Part):
#     def __init__(self,
#         hole_r = 10,
#         wall_th = 1,
#         ):
#         super().__init__()

#         e = Endcap()

#         z = 10
#         e += translate([-wall_th,-wall_th,-z])(linear_extrude(z)(
#                 rrect(w+wall_th*2, h+wall_th*2, r+wall_th)))

#         e -= translate([w/2, h/2, -5])(
#             cylinder(r=hole_r, h=100))

#         self.add(e)

def jigsaw_piece(dx, th, peg_w=10, opp=False):
    # print("jigsaw({}, {}".format(dx, th))
    e = Endcap(back_th=DEFAULT_ENDCAP_BACK_TH+th)
    jig = jigsaw2.jigsaw(e.h+2*INC, max_peg_cycle_ht=14, peg_w=peg_w, opp=opp)
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
            Endcap(back_th=DEFAULT_ENDCAP_BACK_TH+e180.backing_th),
            jigsaw_piece(dx=e180.dx, th=e180.backing_th),
        ))


def shelf_sxs():
    ec = Endcap180Connector()
    asm = ec
    asm += translate([ec.dx*2+DOWNSPOUT_OUTER_W+20, h, 0])(rotate([0,0,180])(EndcapWithPegs()))
    return asm


def with_conn(x):
    return x + x.draw_connectors()

# A circle with hexagonal holes.
def hatchring(
    r=50,
    hex_th=0.5,
    circ_th=1,
    ):

    # hatch
    h = translate([-r*2, -r*2])(
            hatch(sz=[r*4, r*4], r=1, wall_th=hex_th))
    # boundary circle
    ring = circle(r=r) - circle(r=r-circ_th)
    return render()(
        intersection()(
            h + ring,
            # trim off everything outside the circle
            circle(r)
        )
    )

# def ball():
#     return difference()(
#         sphere(r=10),
#         [rotate([i*360/20,j*360/20,0])(cylinder(r=1,h=100)) for i in range(20) for j in range(20)]
#         )

def jigsaw_test_piece(opp=True):
    return render()(jigsaw_piece(30, 10, opp=opp))

def both_jigsaw_test_pieces():
    return union()(
            render()(
                jigsaw_test_piece(opp=True)),
            translate([130, 60])(
                rotate([0,0,180])(
                    render()(
                        jigsaw_test_piece(opp=False)))))


if __name__ == '__main__':
    model = item_grid([
        ("downspout profile", DownspoutProfile()),
        ("endcap", with_conn(Endcap())),
        # ("endcap2", with_conn(EndcapWithHole())),
        ("with pegs", EndcapWithPegs()),
        ("hatch", hatchring()),
        ("endcap 180", Endcap180Connector()),
        ("shelf sxs", shelf_sxs()),
        ("downspout", rotate([180,0,0])(
                        with_conn(Downspout()))),
        ("jigsaw demo", jigsaw_test_piece()),
        ("jigsaw demo 2", both_jigsaw_test_pieces()),
    ], spacing=400)

    model = shelf_sxs()

    # write scad
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
