import os
from solid import *
from solid.utils import *
from tools.util import *

use("external/scad_utils/morphology.scad")
use("external/mcad/2Dshapes.scad")
use("external/mcad/boxes.scad")


translucent = [1,1,1,0.4]
body_color = translucent

wheel_dist = 60

wheel_r = 12
wheel_th = 10
wheel_hole_r = 2

pla_color = "orange"

A_OPTS = {
    'gap': 30,
    # 'draw': True,
}


# wheel with an indent for treads
class TreadWheel(Part):
    def __init__(self, r, hole_r, th, **kwargs):
        super().__init__(**kwargs)
        gap_th = th / 2
        self.add(difference()(
            # main wheel shape
            cylinder(r=r, h=th),

            # center hole
            translate([0, 0, -INC])(
            cylinder(r=hole_r, h=th+2*INC)),

            # indent in the middle of the outer edge to accomodate treads
            translate([0,0,gap_th/2])(
            difference()(
                cylinder(r=r+INC, h=gap_th),
                cylinder(r=r*0.9,h=gap_th),
            )),
        ))
        self.con['main'] = Connector([0,0,0], [0,0,1])

def spoked_wheel(r, hole_r, th, **kwargs):
    innerSize = hole_r+2
    outerSize = r*0.8

    slices = [donutSlice(innerSize, outerSize, i*60, i*60+40) for i in range(0,6)]

    return Part("SpokedWheel", **kwargs)(difference()(
        TreadWheel(r, hole_r, th),

        # remove slices to create "spokes" and hollow out most of the wheel
        translate([0,0,-2*INC])(
        linear_extrude(th+INC*4)(union()(slices)))))


def main_wheel(**kwargs):
    w = Part("MainWheel", **kwargs)(color(pla_color)(
                spoked_wheel(r=wheel_r, hole_r=wheel_hole_r, th=wheel_th)))
    return w

tread_th = 2

leg_front_wheel_r = wheel_r/2
tread_gap_x = 1 # + leg_sideplate_th
leg_wheel_dist = wheel_dist * 2/3
leg_theta = 30
front_wheel_hole_r = 5


def treads(r1, r2, l=20, w=10, th=1, **kwargs):
    circles = [([0,0], r1), ([l,0], r2)]
    t = Part("Treads", **kwargs)(
        color("black")(
        linear_extrude(10)(
        difference()(
            hull()([translate(pt)(circle(r+th)) for pt, r in circles]),
            hull()([translate(pt)(circle(r)) for pt, r in circles])))))
    t.con['main'] = Connector([0,0,0], [0,0,1])
    # t.con['front'] = Connector([0,l,0], [0,0,1])

    return t


# chassis
chassis_w = 30
chassis_ht = 3
chassis_len = wheel_dist+2*wheel_r

def chassis():
    # color(pla_color)
    # union() {
    #     translate([-chassis_w/2, 0,0])
    #     cube([chassis_w, chassis_len, chassis_ht])

    #     # # part of main chassis that connects to front wheel brackets
    #     # w=30
    #     # l=8
    #     # h=5
    #     # translate([chassis_len-l,-w/2,0])
    #     # cube([l,w,h])
    # }

    # translucent body outline
    # color([1,1,1,0.4])
    body_gap = 2 # spacing from body to wheel
    return Part("Chassis")(translate([0,wheel_dist/2+wheel_r,wheel_r])(
            rotate([0,90,0])(
            scale([0.85, 0.85, 1])(
            union()(
                # h, l, w
                roundedBox([wheel_r*2, wheel_dist+wheel_r*2, half_wheel_spacing*2-body_gap*2], 10, True),
                translate([wheel_r*-0.1,0,0])(
                roundedBox([wheel_r*2 * 0.8, wheel_dist-wheel_r*2, (wheel_th+half_wheel_spacing)*2], 5, True)))))))



half_wheel_spacing = 20

leg_front_axle_r = 2

leg_sideplate_th=2
def leg_main(th=wheel_th, outer_scale=0.8, cutout_scale=1.2, **kwargs):
    def wheels(scale=1):
        return union()(
            circle(wheel_r*scale),
            translate([leg_wheel_dist, 0])(
                circle(leg_front_wheel_r*scale)))

    def main_chunk():
        return union()(
            linear_extrude(wheel_th)(
                difference()(
                hull()(wheels(scale=outer_scale)))),
            wheels(scale=cutout_scale))


    def sideplate():
        return linear_extrude(leg_sideplate_th)(
                hull()(
                wheels(scale=outer_scale)))


    def main():
        return union()(
            translate([0, 0, leg_sideplate_th])(
            main_chunk()),

            translate([0, 0, th+leg_sideplate_th])(
            sideplate()),

            # posts
            translate([0,0,th+leg_sideplate_th])(
            rotate([180,0,0])(
                cylinder(r=3,h=20),

                translate([leg_wheel_dist,0,0])(
                    cylinder(r=leg_front_axle_r,h=wheel_th + 2)))))


    leg = Part("Leg", **kwargs)(translate([0,0,-leg_sideplate_th])(main()))
    leg.con['main'] = Connector([0,0,0], [0,0,1])
    return leg


def double_wheel(**kwargs):
    # TODO: don't leave gap b/w wheels
    return Part("DoubleWheel", **kwargs)(union()(
            spoked_wheel(r=wheel_r, hole_r=front_wheel_hole_r, th=wheel_th),

            translate([0,0,wheel_th+tread_gap_x])(
                spoked_wheel(r=wheel_r, hole_r=front_wheel_hole_r, th=wheel_th))))


def packbot():
    # TODO: do better
    bot_main = union()
    bot = Thing("Packbot")

    # wheel connectors
    right, left = [1, 0, 0], [-1, 0, 0]
    bot.con = {
        'wheel_bl': Connector(
            [-half_wheel_spacing, wheel_r, wheel_r],
            left,
            90,
        ),
        'wheel_br': Connector(
            [half_wheel_spacing, wheel_r, wheel_r],
            right,
            90,
        ),
        'wheel_fl': Connector(
            [-half_wheel_spacing, wheel_dist+wheel_r, wheel_r],
            left,
            90,
        ),
        'wheel_fr': Connector(
            [half_wheel_spacing, wheel_dist+wheel_r, wheel_r],
            right,
            90,
        ),
    }
    bot.con['leg_br'] = bot.con['wheel_fr'].translated([wheel_th+tread_gap_x, 0, 0]).rotated(leg_theta)
    bot.con['leg_bl'] = bot.con['wheel_fl'].translated([-wheel_th-tread_gap_x, 0, 0]).rotated(-leg_theta)

    leg_front_translate = [
        0,
        leg_wheel_dist*math.cos(deg2rad(leg_theta)),
        leg_wheel_dist*math.sin(deg2rad(leg_theta))
    ]
    bot.con['leg_fr'] = bot.con['leg_br'].translated(leg_front_translate)
    bot.con['leg_fl'] = bot.con['leg_bl'].translated(leg_front_translate)

    for pos in ['bl', 'br']:
        # rear wheels
        bot_main += main_wheel(tag=pos) @ bot.con['wheel_' + pos]

        # treads
        bot_main += treads(
                        wheel_r,
                        wheel_r,
                        l=wheel_dist,
                        w=wheel_th/2,
                        th=tread_th,
                        tag=pos) @ bot.con['wheel_' + pos]

    # bot_main += color(body_color)(chassis())

    # front wheels
    for pos in ['fl', 'fr']:
        bot_main += double_wheel(tag=pos) @ bot.con['wheel_' + pos]


    # leg treads
    for pos in ['br', 'bl']:
        t = treads(wheel_r, leg_front_wheel_r, l=leg_wheel_dist, th=tread_th, tag=pos)
        bot_main += t @ bot.con['leg_' + pos]


    # front axle tied to leg pivot
    extra=2
    double_wheel_th = wheel_th*2 + tread_gap_x
    post_len = (half_wheel_spacing + double_wheel_th + extra)*2

    def axle():
        return Part("FrontAxle")(
            rotate([0,90,0])(
            color(pla_color)(
            cylinder(r=front_wheel_hole_r-1, h=post_len))))


    bot_main += translate([-post_len/2, wheel_dist + wheel_r, wheel_r])(axle())


    for conname in ['leg_fl', 'leg_fr']:
        # TODO: set pla_color
        bot_main += spoked_wheel(r=leg_front_wheel_r, hole_r=wheel_hole_r, th=wheel_th, tag=conname) @ bot.con[conname]


    # leg frames
    for conname in ['leg_bl', 'leg_br']:
        bot_main += leg_main(tag=conname) @ bot.con[conname]


    # raspi
    if False:
        bot_main += translate([0, PiSizeX/2 + 10, wheel_r*1.5])(
        rotate([0,0,90])(
        union()(
            PiZeroBody(),
            PiZeroTestPads())))

    return bot(bot_main)


def axle2():
    return cube(1)


pbot = packbot()
model = pbot + translate([0,0,30])(axle2())


# TODO: refactor and mind that a lot of this only applies to assemblies

basename = "%s.scad" % os.path.basename(sys.argv[0])

# These additions don't affect the BOM or part connect listing
model += translate([0,0,-100])(part_grid(model))
model += pbot.draw_connectors()

if __name__ == "__main__":
    # write bom
    with open("%s.bom" % basename, "w") as f:
        f.write(generate_bom(model))

    with open("%s.parttree" % basename, "w") as f:
        f.write(part_tree_str(model))

    with open("%s.partconnects" % basename, "w") as f:
        f.write(part_tree_connector_str(model))

    scad_render_to_file(model, "%s.scad" % basename, file_header='$fn=100;')
    print("Wrote file")
