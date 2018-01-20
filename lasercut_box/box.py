from solid import *
from solid.utils import *
from tools.util import *
import sys
import os
import math
import numpy as np


# @param num The number of teeth + gaps to draw
def teeth(h, tooth_len, num, startup=False, extra_thick=0):
    rects = []
    x = 0
    gap_len = tooth_len
    is_gap = not startup
    for i in range(num):
        if is_gap:
            x += gap_len
        else:
            rects.append(translate([x, 0])(square([tooth_len, h])))
            x += tooth_len
        is_gap = not is_gap
    return union()(rects)


def calculate_tooth_len(target_tooth_len, span_dist, even=True):
    num_teeth = float(span_dist) / target_tooth_len
    if not even:
        # round to nearest odd number
        num_teeth = 2 * floor(num_teeth / 2) + 1
    else:
        num_teeth = 2 * round(num_teeth / 2)
    tooth_len = float(span_dist) / num_teeth
    return tooth_len


def box_pattern(dims=[200, 300, 25], sheet_thick=5, tooth_extra_ht=0.7):

    # calculate tooth sizes for each dimension/interface
    x_tooth_len = calculate_tooth_len(
        target_tooth_len=sheet_thick * 2, span_dist=dims[0], even=True)
    y_tooth_len = calculate_tooth_len(
        target_tooth_len=sheet_thick * 2, span_dist=dims[1], even=False)
    z_tooth_len = calculate_tooth_len(
        target_tooth_len=sheet_thick * 2, span_dist=dims[2], even=False)

    # spacing between main and side pieces
    gap = sheet_thick + 2

    main_teeth = []
    sides = []
    for i in range(4):
        # transform to a space to draw the i'th side piece
        x = xform_rotate_z(90 * i)
        txs = [
            xform_translate([0, 0, 0]),
            xform_translate([dims[0], 0, 0]),
            xform_translate([dims[0], dims[1], 0]),
            xform_translate([0, dims[1], 0])
        ]
        x = txs[i] @ x

        ll = dims[1] if i % 2 == 1 else dims[0]
        t_len = y_tooth_len if i % 2 == 1 else x_tooth_len

        c = teeth(
            h=sheet_thick + tooth_extra_ht,
            tooth_len=t_len,
            num=int(ll / t_len) - 1)

        # cutout for bottom piece
        main_teeth.append(
            multmatrix(x.tolist())(teeth(
                h=sheet_thick + tooth_extra_ht,
                tooth_len=t_len,
                num=int(ll / t_len) - 1,
                startup=True)))

        plt = union()(
            # main side panel body
            translate([sheet_thick + tooth_extra_ht, -dims[2]])
            (square([ll - (sheet_thick + tooth_extra_ht) * 2 + INC, dims[2]])),

            # teeth to interface with bottom plate
            c,

            # front (vertical)
            translate([ll, -dims[2]])(rotate([0, 0, 90])(teeth(
                h=sheet_thick + tooth_extra_ht,
                tooth_len=z_tooth_len,
                num=int(dims[2] / z_tooth_len)))),

            # back (vertical)
            rotate([0, 0, -90])(teeth(
                h=sheet_thick + tooth_extra_ht,
                startup=True,
                tooth_len=z_tooth_len,
                num=int(dims[2] / z_tooth_len))),
        )

        side = multmatrix(x.tolist())(translate([0, -gap])(plt))
        sides.append(side)

    inset = tooth_extra_ht + sheet_thick
    box = union()
    box_main = translate([inset, inset])(square(
        [dims[0] - inset * 2, dims[1] - inset * 2]))
    box += union()(box_main, *main_teeth)
    for side in sides:
        box += side

    return box


# 2mm cut initially with pow 100, speed 6 - this was slightly overbaked
# redid 2mm cut with pow 100, speed 10, which was about right
# laser model
# model = box_pattern(
#     dims = [40, 40, 20],
#     tooth_extra_ht = 1,
#     sheet_thick=2,
#     )

# big box, acrylic
model = box_pattern(
    dims=[200, 123, 42],
    tooth_extra_ht=0.8,
    sheet_thick=3,
)
