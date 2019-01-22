from solid import *
from math import sin, cos, pi
import numpy as np
import math
from solid.utils import *
from functools import reduce

in2mm = 25.4

fn = 100

w = 78.7
h = 58.7
r = 15

# def simple():
#     return square([78.7, 58.7])

def wavy_piece():
    amp = 1
    wave = [(t, amp*sin(t)) for t in np.linspace(0, 8*pi, num=50)]
    # print(wave[0], wave[-1])
    h = 5
    model = polygon(points = [(wave[0][0],h)] + wave + [(wave[-1][0],h)] )
    return model

def circ():
    return [(r*cos(t), r*sin(t)) for t in np.linspace(0, 2*pi, num=fn)]


model = import_stl("downspout-endcap/2x3_End_Cap.stl")


def rrect(w, h, r):
    return union()(
        translate([0, r])(square([w, h-2*r])),
        translate([r, 0])(square([w-2*r, h])),
        translate([r,r])(circle(r)), # bottom right
        *[translate([x, y])(circle(r)) for x in [r, w-r] for y in [r, h-r]],
    )

model += rrect(w, h, r)


# def endcap_profile():


# items: list of (name, scadobj) tuples
def item_grid(items, spacing=100):
    grid_sz = math.ceil(math.sqrt(len(items)))
    part_grid = union()

    for i in range(len(items)):
        name = items[i][0]
        obj = items[i][1]
        x = i % grid_sz
        y = floor(i / grid_sz)
        txt = translate([0, -30, 0])(text(name))
        part_grid += translate([x * spacing, y * spacing, 0])(obj, txt)
    d = (grid_sz - 1) * spacing / 2
    return translate([-d, -d, 0])(part_grid)

# thickness of vinyl downspout walls
downspout_th = 2
def downspout_profile():
    th = downspout_th
    p = rrect(w, h, r) \
          - translate([th,th])(rrect(w-2*th, h-2*th, r-th))
    return p


def endcap():
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

    return base


def downspout(l=35*in2mm):
    return color("white")(linear_extrude(l)(downspout_profile()))

model = item_grid([
    ("downspout profile", downspout_profile()),
    ("endcap", endcap()),
    ("downspout", rotate([180,0,0])(
                    downspout())),
    ("sin wave", wavy_piece()),
], spacing=150)


if __name__ == '__main__':
    # write scad
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
