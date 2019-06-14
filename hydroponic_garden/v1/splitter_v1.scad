include <hydroponic_garden/hose_fitting.scad>;

angles = [ for (i=[0:3]) i*360/3 ];

function pts(r) = [ for (a=angles) [r*cos(a),r*sin(a)] ];

// three small nozzles
r = 13;

nozzle_len = 10;

b_r = r + nozzle_r_large;

module plate(thick) {
    linear_extrude(thick)
    union() {
        polygon(pts(b_r));
        for (p=pts(r)) {
            translate([p[0], p[1],0])
            circle(r=nozzle_r_large);
        }
    }
}

// radius of the three water channels inside the fitting
channel_r = nozzle_r_inner;

top_thick = 1.5;
body_thick = top_thick + nozzle_r_inner + channel_r + top_thick;


module waterflow() {
    color("blue")
    translate([0,0,-channel_r-top_thick])
    union() {
        for (a=angles) {
            rotate([0,90,a])
            cylinder(r=channel_r, h=r);
        }

        // for each nozzle
        for(x = concat(pts(r), [0,0])) {
            translate([x[0], x[1], 0])
            union() {
                sphere(r=nozzle_r_inner);
                cylinder(r=nozzle_r_inner, h=20);
            }
        }
    }
}

module splitter_main() {
    // nozzle at the center
    nozzle(length=nozzle_len);

    // three small nozzles
    for (p=pts(r)) {
        translate([p[0], p[1], 0])
        nozzle(length=nozzle_len, r_bottom=nozzle_r_large);
    }

    // main fitting body, roughly a triangle
    translate([0,0,-body_thick])
    plate(thick=body_thick);
}

module splitter(demo=false) {
    if (demo) {
        % splitter_main();
        waterflow();
    } else {
        difference() {
            splitter_main();
            waterflow();
        }
    }
}

splitter(demo=true);
