import solid as S
import sympy
import math

GOLDEN_RATIO = 1.61803398875

# small increment to prevent edge co-incident edges/surfaces
INC = 0.0001


def rad2deg(r):
    return r * 180 / math.pi


def deg2rad(r):
    return r * math.pi / 180.0


# Simple ellipse - axis-aligned
# @param pt A point on the ellipse
# @param ctr The center of the ellipse
# @param H horizontal axis
# @param V vertical axis length
def eq_simple_ellipse(pt, ctr, H, V):
    return sympy.Eq((pt[0] - ctr[0])**2 / H**2 + (pt[1] - ctr[1])**2 / V**2, 1)


# Generalized ellipse - can be slanted
# @param pt A point on the ellipse
# @param ctr The center of the ellipse
# @param H horizontal axis length
# @param V vertical axis length
# @param rot counter-clockwise rotation (in radians)
#
# https://math.stackexchange.com/questions/426150
def eq_gen_ellipse(pt, ctr, H, V, rot=0):
    return sympy.Eq(((pt[0] - ctr[0]) * math.cos(rot) +
                     (pt[1] - ctr[1]) * math.sin(rot))**2 / H**2 + (
                         (pt[0] - ctr[0]) * math.sin(rot) -
                         (pt[1] - ctr[1]) * math.cos(rot))**2 / V**2, 1)


def hole_pattern(pot_l, pot_w):
    obj = S.union()

    r1 = 4

    pot_lw_ratio = pot_l / pot_w
    big_hole_dx = pot_w / 5
    big_hole_dy = big_hole_dx * pot_lw_ratio

    obj += S.circle(r1)

    for i in [-1, 1]:
        for j in [-1, 1]:
            obj += S.translate([big_hole_dx * i, big_hole_dy * j,
                                0])(S.circle(r1))
    return obj


# Extrudes the positive profiles and subtracts the negative extrusions.
# Adds a flat bottom with holes.
def generalized_pot(extrude_func,
                    prof_n1,
                    prof_p1,
                    pot_l,
                    pot_w,
                    holes=True,
                    base_th=3,
                    emboss_text=""):
    base_prof = S.difference()(
        # main profile
        S.difference()(
            prof_p1(),
            prof_n1(),
        ),

        # cut off everything above the base height
        S.translate([-pot_l * 5, base_th])(S.square(pot_l * 10), ),
    )
    base = S.hull()(extrude_func(base_prof))

    # bottom holes
    if holes:
        base = S.difference()(
            base,
            S.translate([0, 0,
                         -INC])(S.linear_extrude(base_th * 2)(hole_pattern(
                             pot_l, pot_w)), ),
        )

    # embossed text
    emboss_depth = 0.4
    font_size = 6
    if len(emboss_text):
        base = S.difference()(
            base,

            # text
            S.translate([0, 10, base_th - emboss_depth])(S.linear_extrude(
                emboss_depth * 2)(S.text(
                    EMBOSS_TEXT,
                    halign="center",
                    valign="center",
                    size=font_size)), ))

    return S.difference()(
        S.union()(extrude_func(prof_p1), base),
        extrude_func(prof_n1),
    )
