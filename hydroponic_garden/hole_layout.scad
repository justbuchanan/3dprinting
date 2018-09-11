include <MCAD/units.scad>
include <MCAD/regular_shapes.scad>


fitting_od = 5/8*inch;

length = 26.25*inch;

w = 3*inch;

module hole(r) {
    inc = 2;
    translate([0,0,-inc])
    cylinder(r=r, h = 1000);
}

pot_od = 2*inch;

fitting_inset = 9/8*inch + 1/4*inch + fitting_od/2;
first_pot_center = fitting_inset + fitting_od/2 + pot_od / 2 + 1/2*inch;

num_pots = 5;
span = length - 2*first_pot_center;
hole_spacing = span / (num_pots - 1);

module body(first_pot_center=first_pot_center, num_pots=5) {
    difference() {
        color("white")
        cube([length, w, 2*inch]);

        union() {
            // fitting holes
            for (x = [fitting_inset, length - fitting_inset]) {
                translate([x, w/2, 0])
                hole(r=fitting_od/2);
            }

            // pot holes
            pot_xs = [first_pot_center, length - first_pot_center];

            xs2 = [for(i=[0:num_pots-2]) first_pot_center + hole_spacing*i];
            for (x = concat(pot_xs, xs2)) {
                translate([x, w/2, 0])
                hole(r=pot_od/2);
            }
        }
    }
}

module body_5h() {
    body();
}

module body_4h() {
    body(first_pot_center = first_pot_center + hole_spacing/2, num_pots=4);
}

spacing = (12*inch - 3*w) / 2;

body_5h();

translate([0, spacing + w, 0])
body_4h();

translate([0, spacing*2 + w*2, 0])
body_5h();
