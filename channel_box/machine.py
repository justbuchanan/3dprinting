from solid import *
import math

# simple box made of aluminum channel with plexiglass walls

translucent_orange = "#FF990080"


def channel_profile(w=20):
    hdiag = math.sqrt(2 * w**2) / 2
    bw = 1.8
    outer_r = 1.5

    dim_3 = 9.5
    dim_5 = 6.2
    dim_4 = 10.5
    edge_th = 2

    mn = union()(square([w * 0.5, w * 0.5], center=True), )

    def corner_half():
        return polygon([
            [w / 2, w / 2 - outer_r / 2],
            [w / 2 - outer_r / 2, w / 2],
            [dim_3 / 2, w / 2],
            [dim_5 / 2, w / 2 - edge_th],
            [dim_4 / 2, w / 2 - edge_th],
            [dim_4 / 2, w / 2 - 2 * edge_th],
            [w / 2 - 2 * edge_th, dim_4 / 2],
        ])

    for i in range(4):
        xsign = 1 if i % 2 == 0 else -1
        ysign = 1 if i < 2 else -1
        mn += rotate(i * 90)(union()(
            rotate(45)(translate([0, -bw / 2])(square([hdiag - outer_r,
                                                       bw])), ),
            translate([w / 2 - outer_r, w / 2 - outer_r])(circle(outer_r)),
            corner_half(),
            mirror([1, 1])(corner_half(), ),
        ))

    return difference()(
        mn,
        circle(r=2.5),
    )


def channel(l=10, w=20):
    return color("#C0C0C0")(linear_extrude(l)(channel_profile(w=20)))


def machine():
    l = 300
    h = 100
    w = 200
    gap = 15
    channel_w = 20
    plate_th = 5

    def lateral_frame():
        return union()(
            # front
            translate([0, channel_w / 2, 0])(rotate([0, 90, 0])(channel(
                w, w=channel_w))),

            # left
            translate([channel_w / 2, channel_w + gap,
                       0])(rotate([-90, 0, 0])(channel(l, w=channel_w))),

            # back
            translate([0, l + channel_w * 1.5 + gap * 2,
                       0])(rotate([0, 90, 0])(channel(w, w=channel_w)), ),

            # right
            translate([w - channel_w / 2, channel_w + gap, 0])
            (rotate([-90, 0, 0])(channel(l, w=channel_w))),
        )

    return union()(
        lateral_frame(),
        translate([0, 0, gap * 2 + h + channel_w])(lateral_frame()),
        translate([0, 0, channel_w / 2 + gap])(
            union()([
                # front left post
                translate([channel_w / 2, channel_w / 2, 0])(channel(
                    h, w=channel_w)),

                # front right post
                translate([w - channel_w / 2, channel_w / 2, 0])(channel(
                    h, w=channel_w)),

                # back right post
                translate(
                    [w - channel_w / 2, channel_w * 1.5 + l + gap * 2,
                     0])(channel(h, w=channel_w)),

                # back left post
                translate([channel_w / 2, channel_w * 1.5 + l + gap * 2, 0])
                (channel(h, w=channel_w)),
            ])),

        # front plate
        translate([0, -gap, -channel_w / 2 + gap])(rotate([90, 0, 0])(
            color(translucent_orange)(cube([w, h + channel_w * 2, 5])))),

        # back plate
        translate(
            [0, l + channel_w * 2 + gap * 3 + plate_th, -channel_w / 2 + gap])
        (rotate([90, 0, 0])(color(translucent_orange)(cube(
            [w, h + channel_w * 2, plate_th])))),

        # left plate
        translate([-gap, gap, -channel_w / 2 + gap])(rotate([0, -90, 0])(
            color(translucent_orange)(cube(
                [h + channel_w * 2, l + channel_w * 2, plate_th])))),

        # top plate
        translate([0, gap, h + channel_w * 1.5 + gap * 3])(
            color(translucent_orange)(cube([w, l + channel_w * 2, plate_th]))),
    )


model = machine()
