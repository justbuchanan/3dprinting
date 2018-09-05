#!/usr/bin/env python3

import math
import numpy as np
import sympy
import solid as S
import succulent_planter.util as util

fn = 100

# we're trying to solve for the location of the ellipse center
ell_center_x, ell_center_y = sympy.symbols('ell_center_x ell_center_y')
ell_center = [ell_center_x, ell_center_y]

edge_r = 1
min_th = 2
brim_w = 7
h = 25

# ellipse axes lengths for ellipse cut out of side profile
# note: these are not the width and height of the ellipse
ellV = 28
ellH = 15

# ellipse is rotated slightly
ellipse_angle_deg = 10

slant_dx = h / 4

edge_circ_pt = np.array([slant_dx + brim_w - edge_r, h - edge_r])

# point where edge circle meets cutout ellipse
# Decide the slope we want, then find the point on the circle with that slope
meet_slope = math.pi / 6
# TODO: better math
upper_meet_pt = edge_circ_pt + edge_r * np.array(
    [math.sin(meet_slope), -math.cos(meet_slope)])

bottom_meet_pt = np.array([min_th, 0])


def solve_for_ell_center():
    # Calculate the center of the ellipse given the two points we want it to intersect
    eqs = [
        # intersection with bottom of pot
        util.eq_gen_ellipse(bottom_meet_pt, ell_center, ellH, ellV,
                            -util.deg2rad(ellipse_angle_deg)),
        # intersection with upper edge of pot
        util.eq_gen_ellipse(upper_meet_pt, ell_center, ellH, ellV,
                            -util.deg2rad(ellipse_angle_deg)),
    ]
    possible_ell_centers = sympy.solve(eqs, ell_center)
    print(possible_ell_centers)

    # filter out imaginary solutions
    def filter_solns(solutions):
        for s in solutions:
            if not any(np.iscomplex([complex(d) for d in s])):
                yield s

    possible_ell_centers = list(filter_solns(possible_ell_centers))

    if len(possible_ell_centers) == 0:
        raise RuntimeError("No solution found for ellipse center")

    if len(possible_ell_centers) > 1:
        possible_ell_centers = [
            min(possible_ell_centers, key=lambda pt: pt[1])
        ]
        pass

    return possible_ell_centers[0]


ell_center = solve_for_ell_center()

# The below shapes are arranged like:
#
#           *
#     *
#
#
#
#
#    ===
#
# upper brim outer edge circle
brim_edge_circ = S.translate(edge_circ_pt)(S.circle(edge_r))
upper_inner_circ = S.translate([slant_dx + edge_r,
                                edge_circ_pt[1] - 1])(S.circle(edge_r))
bottom_rect = S.square([min_th, 0.1])

ell_scale = ellV / ellH
print("sc: %f" % ell_scale)

prof_p1 = S.hull()(bottom_rect, brim_edge_circ, upper_inner_circ)

# cut out ellipse
prof_n1 = S.translate(ell_center)(S.rotate(-ellipse_angle_deg)(S.scale(
    [1, ell_scale])(S.circle(ellH))))


def draw_profile():
    obj = prof_p1 + S.color("black")(prof_n1)

    # draw intersection points
    if True:
        obj += S.color("red")(S.linear_extrude(10)(S.union()(
            S.translate(bottom_meet_pt)(S.circle(0.2)),
            S.translate(upper_meet_pt)(S.circle(0.2)),
        )))
    return obj


pot_l = 120
pot_lw_ratio = util.GOLDEN_RATIO
pot_w = pot_l / pot_lw_ratio

# def bottom_plate():
#     return S.difference()(
#             # bottom plate
#             S.linear_extrude(min_th)(
#                S.scale([1, pot_lw_ratio])(S.circle(pot_w/2+min_th))
#             ),
#             # cut out bottom holes
#             S.translate([0,0,-0.1])(
#                 S.linear_extrude(10)(hole_pattern())
#             )
#         )


def pot():
    return S.union()(
        util.generalized_pot(
            lambda prof: util.along_ellipse(pot_l / 2, pot_w / 2, fn, prof),
            prof_p1=prof_p1,
            prof_n1=prof_n1,
            pot_l=pot_l,
            pot_w=pot_w,
            base_th=min_th * 2),
        # bottom_plate(),
    )


def pot_ell3():
    s2 = 0.9
    rectl = pot_l * 2

    def ell_main():
        return S.translate([0, 0, pot_w])(
            S.difference()(
                S.scale([1, pot_lw_ratio, 1])(S.sphere(pot_w)),

                # cut out inside
                S.scale([s2, pot_lw_ratio * s2, s2])(S.sphere(pot_w)),
                S.translate([-rectl / 2, -rectl / 2,
                             -pot_w + 50])(S.cube([rectl, rectl, rectl])),
            ))

    base_scale = 0.7

    def bottom(th=min_th):
        return S.linear_extrude(th)(S.scale(
            [base_scale, pot_lw_ratio * base_scale,
             base_scale])(S.circle(pot_w)))

    return ell_main() + bottom(min_th * 2)


def square_pot():
    return S.translate([0, 0, h / 2])(S.difference()(S.cube(
        [pot_w, pot_l, h], center=True), S.translate([0, 0, min_th])(S.cube(
            [pot_w - min_th * 2, pot_l - min_th * 2, h], center=True))))


def rounded_rect_pot(r):
    return S.union()(util.generalized_pot(
        lambda prof: util.rounded_rect_extrude_func(prof, r,sizes=[pot_l,pot_w]),
        base_th=min_th * 2,
        prof_p1=prof_p1,
        prof_n1=prof_n1,
        pot_l=pot_l,
        pot_w=pot_w))


def rounded_rect_tray(r):
    extra_width = 25

    r = r + extra_width / 2

    edge_r = 1
    min_th = 1.5
    brim_w = 2.5
    h = 11

    slant_dx = h / 4

    edge_circ_pt = np.array([slant_dx + brim_w - edge_r, h - edge_r])

    # point where edge circle meets cutout ellipse
    # Decide the slope we want, then find the point on the circle with that slope
    meet_slope = math.pi / 6
    # TODO: better math
    upper_meet_pt = edge_circ_pt + edge_r * np.array(
        [math.sin(meet_slope), -math.cos(meet_slope)])

    bottom_meet_pt = np.array([min_th, 0])

    # upper brim outer edge circle
    brim_edge_circ = S.translate(edge_circ_pt)(S.circle(edge_r))
    upper_inner_circ = S.translate([slant_dx + edge_r,
                                    edge_circ_pt[1] - 0.5])(S.circle(edge_r))
    bottom_rect = S.square([min_th, 0.1])

    # ell_scale = ellV / ellH
    # print("sc: %f" % ell_scale)

    prof_p1 = S.hull()(bottom_rect, brim_edge_circ, upper_inner_circ)

    prof_n1 = S.union()

    main_tray = S.union()(
            util.generalized_pot(
                lambda prof: util.rounded_rect_extrude_func(prof, r, sizes=[pot_l+extra_width, pot_w+extra_width]),
                prof_p1=prof_p1,
                prof_n1=prof_n1,
                pot_l=pot_l,pot_w=pot_w,
                holes=False,
                base_th = 2),
        )

    pot = rounded_rect_pot(rpot_r)

    slice_ht = h - 1
    slice_th = 2
    slice_inset = 30
    slice_y_inset = 30 + 20
    pot_z_inset = 3

    sides = S.union()(
        S.translate([-slice_th / 2, -pot_l,
                     0])(S.cube([slice_th, pot_l - slice_y_inset, slice_ht])),
        S.translate([-slice_th / 2, slice_y_inset,
                     0])(S.cube([slice_th, pot_l, slice_ht])),
    )
    for y in [-25, 25]:
        sides.add(
            S.translate([-pot_w, y, 0])(S.cube(
                [pot_w - slice_inset, slice_th, slice_ht])))
        sides.add(
            S.translate([slice_inset, y,
                         0])(S.cube([pot_w, slice_th, slice_ht])))

    main_tray = S.union()(
        main_tray,
        S.difference()(
            S.intersection()(
                sides,
                S.hull()(main_tray),
            ),

            # TODO: cutout pot
            S.translate([0, 0, h - pot_z_inset])(S.hull()(pot)),
        ))

    return main_tray


rpot_r = pot_l / 4

model = S.union()(
    rounded_rect_pot(rpot_r),
    S.translate([0, 0, -25])(rounded_rect_tray(rpot_r)),

    # S.translate([-200, 0,0])(pot()),

    # S.translate([200,0,0])(pot_ell3()),

    # S.translate([100,0])(draw_profile()),

    # S.translate([0,200,0])(square_pot()),
)

if __name__ == '__main__':
    # write scad
    fname = "genpot.scad"
    S.scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
