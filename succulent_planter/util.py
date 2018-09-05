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


def rounded_rect_extrude_func(prof, r, sizes=[pot_l, pot_w]):
    edges = []

    for i in range(4):
        l = sizes[i % 2]
        tx = [0, 0, 0]

        if i == 0:
            tx[1] = -r
        if i == 1:
            tx[0] = -sizes[1] + r
        if i == 2:
            tx[0] = -sizes[1]
            tx[1] = -sizes[0] + r
        if i == 3:
            tx[0] = -r
            tx[1] = -sizes[0]

        edge = S.translate(tx)(S.rotate([90, 0, i * 90])(
            S.linear_extrude(l - r * 2)(prof)))
        edges.append(edge)

        tx2 = list(tx)
        if i == 0 or i == 3:
            tx2[0] -= r
        if i == 1:
            tx2[1] -= r
        if i == 2:
            tx2[0] += r
        if i == 3:
            tx2[1] += r
            tx2[0] += r

        edges.append(
            S.translate(tx2)(S.rotate([0, 0, i * 90])(S.rotate_extrude(90)(
                S.translate([r, 0, 0])(prof)))))

    obj = S.translate([sizes[1] / 2, sizes[0] / 2, 0])(S.union()(edges))
    return obj


# Extrude a given profile along an elliptical path.
# Note: @d2profile should be a convex since extrusions are done using the hull()
#       command
def along_ellipse(x1, x2, fn_a, d2profile):
    # Place an object at a certain point along an elliiptical path
    def place(x1, x2, aa, e, obj):
        return S.translate([x2 * math.sin(aa), x1 * math.cos(aa), 0])(S.rotate(
            util.rad2deg(-aa + math.pi / 2))(S.rotate([90, 0, 0])(
                S.linear_extrude(e)(obj))))

    obj = S.union()

    # small thickness of the 2d profile
    e = 0.05
    for a in range(0, fn_a):
        aa = a * 2 * math.pi / fn_a
        obj += S.hull()(place(x1, x2, aa, e, d2profile),
                        place(x1, x2, aa + 2 * math.pi / fn_a, e, d2profile))
    return obj
