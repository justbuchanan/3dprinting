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

def circ():
    return [(r*cos(t), r*sin(t)) for t in np.linspace(0, 2*pi, num=fn)]


# model = import_stl("downspout-endcap/2x3_End_Cap.stl")


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
        self.con['main'] = Connector([w/2, h/2, 0], [0,0,1])


class EndcapConnector(Part):
    # TODO: share with endcap()
    # thickness of connector wall
    def __init__(self):
        super().__init__(collect_subconnectors=False)
        wall_th = 1

        # distance between the two downspouts
        downspout_spacing = 10

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

        self.add(conn)
        self.con['left'] = Connector([w/2, h/2, 0], [0,0,1])
        self.con['right'] = Connector([w/2 + dx, h/2, 0], [0,0,1])


class Downspout(Part):
    def __init__(self, l=35*in2mm):
        super().__init__()
        d = color("white")(
                linear_extrude(l)(
                    downspout_profile()))
        self.add(d)

        self.con['back'] = Connector([w/2, h/2, 0], [0,0,1])
        self.con['front'] = Connector([w/2, h/2, l], [0,0,-1])

def shelf_plumbing():
    c = EndcapConnector()

    d = Downspout()
    asm = c + attach(c.con['right'], d.con['front'])(d)

# def attach(con1, con2, gap=0):

    return asm


model = item_grid([
    ("downspout profile", downspout_profile()),
    ("endcap", Endcap()),
    ("endcap 180", EndcapConnector()),
    ("shelf", shelf_plumbing()),
    ("downspout", rotate([180,0,0])(
                    Downspout())),
    ("sin wave", wavy_piece()),
], spacing=200)

# model = EndcapConnector()


if __name__ == '__main__':
    # write scad
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
