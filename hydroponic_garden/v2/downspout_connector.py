from solid import *
from math import sin, cos, pi
import numpy as np
import math
from solid.utils import *
from functools import reduce
from solid.utils import *
from tools.util import *

INC = 0.001

in2mm = 25.4

fn = 100

w = 78.7
h = 58.7
r = 15

def wavy_piece():
    amp = 1
    wave = [(t, amp*sin(t)) for t in np.linspace(0, 8*pi, num=50)]
    # print(wave[0], wave[-1])
    h = 5
    model = polygon(points = [(wave[0][0],h)] + wave + [(wave[-1][0],h)] )
    return model

# def circ():
#     return [(r*cos(t), r*sin(t)) for t in np.linspace(0, 2*pi, num=fn)]

def hatch(sz=[100,100], r=2, th=1):
    h = square(sz)
    dx = r*2*.866 + th
    dy = r*2*0.75 + th

    for i in range(ceil(sz[0]/r)):
        for j in range(ceil(sz[1]/r)):
            xs = r if (j % 2 == 0) else 0
            h -= translate([i*dx+xs, j*dy])(
                rotate(30)(circle(r=r, segments=6)))
    return h



def rrect(w, h, r):
    return union()(
        translate([0, r])(square([w, h-2*r])),
        translate([r, 0])(square([w-2*r, h])),
        translate([r,r])(circle(r)), # bottom right
        *[translate([x, y])(circle(r)) for x in [r, w-r] for y in [r, h-r]],
    )

# thickness of vinyl downspout walls
downspout_th = 2
def downspout_profile():
    th = downspout_th
    p = rrect(w, h, r) \
          - translate([th,th])(rrect(w-2*th, h-2*th, r-th))
    return p


class Endcap(Part):
    def __init__(self):
        super().__init__()
        # w, h, r dimensions are for the *outside* of the tube.
        # inner width = w - 2*th.
        wall_th = 1

        back_th = 2
        total_h = 10

        base = translate([-wall_th, -wall_th])(
                rrect(w+wall_th*2, h+wall_th*2, r+wall_th))
        base = linear_extrude(total_h)(base)

        # hollow out large middle portion
        dth = downspout_th + wall_th
        base -= translate([dth,dth,back_th])(
                    linear_extrude(total_h)(
                        rrect(w-dth*2, h-dth*2,r-dth)))

        # cut out profile for downspout
        base -= translate([0,0,back_th])(
                    linear_extrude(total_h)(
                        downspout_profile()))

        self.add(base)
        self.con['main'] = Connector([w/2, h/2, back_th], [0.01,0.01,1])  # /////////////////////////////////


class Endcap180Connector(Part):
    # TODO: share with endcap()
    # thickness of connector wall
    def __init__(self):
        super().__init__(collect_subconnectors=False)

        wall_th = 1

        # distance between the two downspouts
        downspout_spacing = 15

        endcap_th = 2

        # add two endcaps
        dx = w + downspout_spacing -wall_th*2
        conn = translate([0, 0, -endcap_th+INC])( # embed endcaps into backing
                Endcap() + translate([dx, 0])(Endcap()))

        # water hole cut out of each endcap that connects to channel
        hole_r = 10

        # distance from back of wall to start of water hole/channel
        chan_wall_th = 3
        chan_w = 4
        chan_h = hole_r*2

        # thickness of main backing body
        backing_th = chan_wall_th*2 + chan_w # TODO calculate from chan_wall_th
        conn += translate([-wall_th, -wall_th, -backing_th])(
                    linear_extrude(backing_th)(
                        rrect(w+dx+wall_th*2, h+wall_th*2, r+wall_th)))

        # water channel holes in back of endcaps
        for x in [w/2+wall_th, w/2+wall_th + dx]:
            conn -= translate([x, h/2+wall_th, -backing_th+chan_wall_th])(
                        cylinder(r=hole_r, h=100))

        # horizontal channel connecting two water holes
        conn -= translate([w/2+wall_th, h/2+wall_th-chan_h/2, -chan_wall_th])(
                rotate([0, 90, 0])(
                    linear_extrude(dx)(
                        square([chan_w, chan_h]))))

        # # add cross-hatch filter/screen to entry holes
        # conn = translate([0, 0, -endcap_th+INC])( # embed endcaps into backing
        #         Endcap() + translate([dx, 0])(Endcap()))
        for x in [0, dx]:
            conn += translate([w/2+wall_th - hole_r + x, h/2+wall_th-hole_r, -1])(
                linear_extrude(1)(
                    hatch(sz=[hole_r*2+2, hole_r*2+2])))

        self.add(color("gray")(conn))
        self.con['left'] = Connector([w/2, h/2, 0.001], [.001,.001,1])
        self.con['right'] = Connector([w/2 + dx, h/2, 0], [0.001,.001,1])


class Downspout(Part):
    def __init__(self, l=35*in2mm, has_holes=True, hole_spacing=20, hole_r=1*in2mm):
        super().__init__()
        d = color("white")(
                linear_extrude(l)(
                    downspout_profile()))

        if has_holes:
            n = math.floor((l - hole_spacing) / (hole_spacing + hole_r*2))
            sp = (l - 2*n*hole_r) / (n + 1)
            # print("n = %d" % n)
            for i in range(n):
                d -= rotate([0,0,0])(rotate([-90, 0, 0])(
                        translate([w/2, -(sp + hole_r + i*(sp+hole_r*2)), h/2])(
                            cylinder(r=hole_r, h=100))))


        self.add(color("white")(render()(d)))

        self.con['back'] = Connector([w/2, h/2, 0], [0.001,0.001,1])
        self.con['front'] = Connector([w/2, h/2, l], [0.001,0.001,-1]) #/////////////////////////////////

def shelf_plumbing():
    c = Endcap180Connector()
    d1 = Downspout()
    d2 = Downspout()

    asm = c
    asm += attach(c.con['right'], d1.con['back'])(d1)
    asm += attach(c.con['left'], d2.con['back'])(d2)

    c2 = Endcap180Connector()
    asm += attach(d1.con['front'], c2.con['left'])(c2)

    # d3 = Downspout()
    # asm += attach(c2.con['right'], d3.con['front'])(d3)

    # asm = cube()
    return asm


def with_conn(x):
    return x + x.draw_connectors()

model = item_grid([
    # ("downspout profile", downspout_profile()),
    ("endcap", with_conn(Endcap())),
    ("hatch", hatch()),
    ("endcap 180", Endcap180Connector()),
    ("downspout", rotate([180,0,0])(
                    with_conn(Downspout()))),
    # ("sin wave", wavy_piece()),
], spacing=200)

# model += translate([600, 500, 0])(rotate([90,0,0])(shelf_plumbing()))

# model = Downspout()

if __name__ == '__main__':
    # write scad
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
