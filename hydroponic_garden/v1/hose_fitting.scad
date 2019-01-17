include <MCAD/units.scad>
include <MCAD/regular_shapes.scad>
include <hydroponic_garden/thingiverse/threads/polyScrewThread_r1.scad>

$fn = 200;

// 5/8" spade bit -> 0.625" od -> 15.875mm od

// m15
// 1.5mm thread pitch
// 5/8" or 15.75mm od
// 13.5mm id

downspout_thick = 1/16 * inch;


thread_tol = 0.25; // difference in radius between threads of different gender
thread_tol_inner = 0.3;

outer_thread_od = 15.75;

inner_thread_od = 9.5; // was 10, tried 7 - was pretty small

flange_radius = 0.5*inch;
flange_thick = 3.5;
nut_flange_thick = 2.5;


nut_height = 7;

// flanged hex nut
module fitting_nut(h=nut_height) {
    difference() {
        union() {
            cylinder(r=flange_radius, h=nut_flange_thick);
            linear_extrude(h)
            hexagon(flange_radius);
        }
        translate([0,0,-2])
        outer_thread(length=h*2, tol=thread_tol);
    }
}


nozzle_thick = 1.2;
nozzle_r_nominal = 0.25*inch/2+0.05;
nozzle_r_large = nozzle_r_nominal + 0.6;
nozzle_r_tip = nozzle_r_nominal-0.1;
nozzle_r_small = nozzle_r_nominal+0.05;
nozzle_r_inner = nozzle_r_small - nozzle_thick;
nozzle_r_bottom = nozzle_r_small;
module nozzle(
    length=8.5,
    r_inner = nozzle_r_inner,
    r_large=nozzle_r_large,
    r_small=nozzle_r_small,
    r_bottom=nozzle_r_bottom,
    r_tip=nozzle_r_tip)
{
    shallow_slope_dy = 3;
    steep_slope_dy = 1;
    flat_dist = 0;

    rotate_extrude(convexity=10)
    polygon([
        [r_inner, 0],
        [r_inner, length],
        [r_tip, length],
        // [r_small, length],

        [r_tip, length-flat_dist],
        [r_large, length-flat_dist-shallow_slope_dy],
        [r_small, length - flat_dist - shallow_slope_dy - steep_slope_dy],

        [r_small, length-shallow_slope_dy-steep_slope_dy-flat_dist],
        [r_large, length-shallow_slope_dy-steep_slope_dy-flat_dist-shallow_slope_dy],
        [r_small, length-shallow_slope_dy-steep_slope_dy - flat_dist - shallow_slope_dy - steep_slope_dy],

        [r_bottom,0],
    ]);
}

module outer_thread(length, tol=0, cs=2) {
    screw_thread(
        outer_thread_od + tol*2,
        1.5, // tooth ht. was previously 2 for test prpints
        45, // tooth shape (degrees). was previuosly 55
        length,
        PI/2, // resolution
        cs // countersunk ends
    );
}

module inner_thread(length, tol=0, cs=2) {
    screw_thread(
        inner_thread_od + tol*2,
        2, // tooth ht. was previously 2 for test prints
        45, // tooth shape (degrees). was previuosly 55
        length,
        PI/2, // resolution
        cs // countersunk ends
    );
}

washer_thick = 2;

outer_thread_len = flange_thick + downspout_thick + nut_height + washer_thick;
inner_thread_len = outer_thread_len - 2;

module main() {
    threaded_part_id = outer_thread_od - 2; // TODO: calculate this correctly
    slant_slope = 0.4; 
    taper_inner_r = nozzle_r_small;
    slant_dy = (threaded_part_id - taper_inner_r*2) * slant_slope;

    difference() {
        union() {
            // flange at the bottom
            outer_thread(length=outer_thread_len);
            cylinder(r=flange_radius, h=flange_thick);

            // taper between threaded part and hose nozzle
            // TODO: this doesn't merge well with the rest of the part
            hack=1;
            translate([0,0,outer_thread_len])
            cylinder(r1=threaded_part_id/2, r2=nozzle_r_large, h=slant_dy+hack);

            // hose nozzle
            translate([0, 0, outer_thread_len+slant_dy])
            nozzle();
        }

        union() {
            // drill a hole through the whole thing
            translate([0,0,-10])
            cylinder(r=nozzle_r_inner, h=100000);

            inc = 2;
            translate([0,0,-inc])
            inner_thread(length=inc + inner_thread_len, tol=thread_tol_inner);

            translate([0,0,inner_thread_len])
            cylinder(r1=(inner_thread_od+thread_tol*2)/2, r2=nozzle_r_inner, h = slant_dy);
        }
    }
}


module plug(water_level=1*cm) {
    above_flange_ht = water_level - flange_thick - washer_thick;
    outer_r = inner_thread_od/2 + 2;
    difference() {
        union() {
            linear_extrude(above_flange_ht)
            hexagon(outer_r);

            // circular flange at top of threads
            translate([0,0,above_flange_ht-flange_thick])
            cylinder(r=outer_r, h=flange_thick);

            translate([0,0,above_flange_ht])
            inner_thread(length=inner_thread_len-3);
        }

        union() {
            // bore center hole
            wall_thick = 2.1; // was 2 in the first print. was 1.75 for a while, but broke several times
            hole_r = inner_thread_od/2 - wall_thick;
            translate([0,0,-1]);
            cylinder(r=hole_r, h=1000);

            // trapezoidal spout shape
            translate([0,0,-0.1]);
            top_wall_thick = 2;
            cylinder(r1=outer_r -top_wall_thick, r2=hole_r, h = above_flange_ht);
        }
    }
}

module source_plug(demo=false,water_level=1.0*cm) {
    outer_r = 8;
    bulb_h = 1*cm;
    chamber_r = bulb_h / 2 - 1;

    module holes() {
        hole_r=0.7;
        // a bunch of radial holes stacked in layers
        for (ang=[0:20:360], h=[2:hole_r*3:8]) {
            translate([0,0, h])
            rotate([90, 0, ang])
            cylinder(r=hole_r, h=15);
        }

        // bulk inner chamber
        v_inset = 2;

        translate([0,0,bulb_h / 2])
        sphere(r=chamber_r);

        // source hole
        translate([0,0,4])
        cylinder(r=nozzle_r_inner, h=20+water_level);
    }

    module main() {
        ht = 1*cm;
        ht2 = water_level - flange_thick - washer_thick;
        cylinder(r=outer_r, h=bulb_h + ht2);

        translate([0,0,ht+ht2])
        inner_thread(length=inner_thread_len-3);
    }
    if (demo) {
        % main();
        color("blue")
        holes();
    } else {
        difference() {
            main();
            holes();
        }
    }
}

module demo_asm() {
    main();

    translate([0,0,flange_thick + downspout_thick])
    fitting_nut();

    translate([0,0, -1*cm + flange_thick])
    plug();
}

