from solid import *
from math import sin, cos, pi
import numpy as np
import math
from solid.utils import *
from functools import reduce
from solid.utils import *
from tools.util import *

fn = 100

w = 100
h = 30


# model -= 

# model = 

# model -= hull()(
    # translate([w/2, h/2])(
        # circle(r=4)))

left = union()
right = union()

for i in range(5):
    x = w/2
    x += 4* (1 if i % 2 == 0 else -1)

    r = 4
    xd = -1 if i % 2 == 0 else 1
    pc = circle(r) + translate([xd*r*2, 0])(square([r*4, r], center=True))


    left -= translate([x, i*10])(
                pc)

model = left + right

if __name__ == '__main__':
    # write scad
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
