#!/usr/bin/env python3

from solid import *
from solid.utils import *
import numpy as np
import math
from tools.util import *

def wheel():
    h = 5
    w = Part("wheel")(
            cylinder(r=20, h=h))
    con = {name: invert_connector(c) for name, c in cylinder_connectors(w.children[0]).items()}
    w.con.update(con)
    print(w.con)
    return w


def axle():
    cyl = cylinder(r=2, h=40)
    c = Part("axle")(color("blue")(cyl))
    c.con = cylinder_connectors(cyl)
    return c


a = axle()
model = a + wheel()@('bottom', a.con['bottom']) + wheel()@('bottom', a.con['top'])

if False:
    axle()({
        'top': (wheel(), 'top'),
        'bottom': (wheel(), 'top'),
        })

# model = union()(
#     axle(),
#     wheel(),
#     wheel(),
#     )



# print(scad_render(model))
scad_render_to_file(model, 'tx_test.scad', file_header='$fn=100;')
print("wrote file")
