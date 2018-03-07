// Status: modelled the 2 psus and ramps board. Haven't done much with the case
// design since I ended up just throwing together out of a couple pieces of
// wood.
//
// TODO: spindle psu speed knob
// TODO: connect to flexi-cord
// TODO: refactor psus and ramps board to separate files - they might be useful again

INC = 0.001;


stepper_subboard_dims = [15, 20, 2];
module stepper_subboard() {
    color("red")
    cube(stepper_subboard_dims);
}

ramps_dims = [101.62, 60.5, 10];
module ramps_board() {
    board_th = 2;
    color("green")
        cube(ramps_dims);

    // usb plug
    uw=8;
    color("blue")
    translate([22,-uw, board_th])
    cube([12, uw, 11]);

    // translate([0, 0, 20])
    // stepper_subboard();
}

module _psu(dims, bay_inset) {
    wall_th = 2;
    color("silver") difference() {
        cube(dims);

        hole_sp = 10;
        for (x = [0:hole_sp:dims[0]]) {
            for (y = [0:hole_sp:dims[1]]) {
                translate([x+hole_sp/2, y+hole_sp/2, dims[2]*0.95])
                cylinder(r=2,h=1000);
            }
        }

        // connector bay/inset
        translate([-INC, wall_th, wall_th])
        cube([bay_inset, dims[1]-wall_th*2, 1000]);
    }

    con_w = dims[1]*0.7;
    color("black")
    translate([1, (dims[1]-con_w)/2, wall_th])
    cube([6, con_w, 6]);

    // translate([0,0,-10])
    // cylinder(r=5,h=100);
}

spindle_psu_size = [140, 109.4, 50];
spindle_psu_bay_inset = 11.5;
module spindle_psu() {
    _psu(spindle_psu_size, spindle_psu_bay_inset);
}

stepper_psu_size = [160, 97, 37.4];
stepper_psu_bay_inset = 11.5;
module stepper_psu() {
    _psu(stepper_psu_size, stepper_psu_bay_inset);
}

module case(show_items=true) {
    if (show_items) {
        translate([0, -spindle_psu_size[1], 0])
        spindle_psu();

        gap = 10;
        translate([0, gap, stepper_psu_size[1]])
        rotate([-90,0,0])
        stepper_psu();

        translate([0, -ramps_dims[1], spindle_psu_size[2]+30])
        ramps_board();
    }

    // www = 100;
    // color("orange")
    // translate([0, 0, -5]) {
    //     cube([100, -www, 4]);
    // }
}

case();

translate([0, 200, 0])
case(show_items=false);
