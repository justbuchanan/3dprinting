from solid import *
from solid.utils import *
from tools.util import *
import sys
import os
import math
import numpy as np


def pts_from_offsets(origin=[0,0], offsets=[]):
    pts = [origin]
    for o in offsets:
        pts.append((np.array(pts[-1]) + np.array(o)).tolist())
    return pts

def planter(r=80, h=50, wall_thick=4, main_color = "#dddd55", demo=False):
    slant_ht = 4.0
    slant_dx = 4.0
    vert_ht = math.sqrt(wall_thick)

    tray_ht = 3
    tray_wall_thick = 2
    tray_wall_ht = 5
    tray_w = 6
    vert_gap = 0
    center_ht = wall_thick*3

    pts = [
        [0,center_ht-wall_thick],
        [r-2*(tray_w + tray_wall_thick), 0],
        [r,0],

        # drop tray around outer bottom edge
        [r, tray_ht + tray_wall_ht],
        [r-tray_wall_thick, tray_ht+tray_wall_ht],
        [r-tray_wall_thick, tray_ht],
        [r-tray_wall_thick-tray_w, tray_ht], # flat of tray
        [r-tray_wall_thick-tray_w, tray_ht+tray_wall_ht+vert_gap],
        [r, tray_wall_thick+tray_w+vert_gap+tray_ht+tray_wall_ht],

        [r,h-slant_ht-vert_ht],
        [r+slant_dx, h-vert_ht], # create slanted segment
        [r+slant_dx, h], # vertical bit
        [r, h],
        [r-wall_thick, h-slant_dx],

        [r-wall_thick, tray_wall_thick+tray_w+vert_gap+tray_ht+tray_wall_ht],
        [r-tray_wall_thick-tray_w-wall_thick, tray_ht+tray_wall_ht+vert_gap], # slant inwards to mirror inset for moat
        [0, center_ht],
    ]
    floor_slope = (center_ht - wall_thick) / pts[-2][0]
    def profile():
        # counter-clockwise
        return polygon(pts)
    angle = 60 if demo else 360
    m = rotate_extrude(angle=angle)(
                profile())

    # hole_r=2
    # for angle in range(0,360,int(360/10)):
    #     m += hole()(translate([r-wall_thick-0.5, 0, wall_thick+hole_r])(
    #             rotate([0,90,0])(
    #                 cylinder(r=hole_r, h=wall_thick*3)
    #                 )))

    b = np.array(pts[-3])
    t = np.array(pts[-2])

    hole_r = 0.75

    holes = []
    dtheta = int(360 / 120)
    for i, ang in enumerate(range(0, 360, dtheta)):
        # print("i: %d" % i)
        if i % 2 == 0:
            p, q = 0.6, 0.4
            mid = b*p + t*q
            pt = [mid[0], 0, mid[1]]
            pt += np.array([0, 0, -0.9])
            # tilt = -45
            tilt = 90
            continue
        else:
            diff = b - t
            wall_len = np.linalg.norm(diff)
            wall_dir = diff / wall_len

            # print("wall_dir: %s" % str(wall_dir))
            mid = t + wall_dir*hole_r
            tilt = floor_slope*90 - 90
            # print("tilt: %f" % tilt)
            pt = [mid[0], 0, mid[1]]

        dr = translate(pt)(
                rotate([0,tilt,0])(
                    translate([0,0,-wall_thick])(
                cylinder(r=hole_r, h=wall_thick*2))))
        dr = rotate([0,0,ang])(dr)
        holes.append(dr)

    return color(main_color)(difference()([m, *holes]))

model = planter(
    # demo=True
    )
