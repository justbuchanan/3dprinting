// originally from: http://www.thingiverse.com/thing:790339/#files

include <MCAD/units.scad>

diameter_top=1.98*inch; // was 1.96 in first print - slightly small. 2.05 second print - too big.
diameter_bottom=1.47*inch;

height=2*inch;

overhang_extent=3;
overhang_height=1;
overhang_angle=55;

thickness_bottom=1.2;
thickness_walls=1.2;

width_connections=3;

pie_segments_1=4;
pie_segments_2=8;
pie_segments_3=16;

pie_segments_wall=16;



// Hidden variables:

eps=0.03*1;

$fn=100*1;



// HELPERS
module cyl_sect(r1, r2, h) {
    difference() {
        cylinder(r=r1, h=h);
        translate([0,0,-eps])
            cylinder(r=r2, h=h+2*eps);
    }
}
module connect(r, w, h, phi) {
    rotate(phi, [0,0,1])
        translate([0,-w/2,0])
            cube([r,w,h]);
}



// OBJECT PARTS
module positive() {
    cylinder(r1=diameter_bottom/2, r2=diameter_top/2, h=height);

    // Overhang
    translate([0,0,height-overhang_height]) {
        cylinder(r=diameter_top/2+overhang_extent, h=overhang_height);
        // printing aid (overhang_angle degrees of overhang are assumed to be printable)
        mirror([0,0,1]) {
            intersection() {
                cylinder(r2=0, r1=diameter_top/2+overhang_extent,
                         h=(diameter_top/2+overhang_extent)/tan(overhang_angle));
                cylinder(r=diameter_top/2+overhang_extent, h=height-overhang_height);
            }
        }
    }
}

module negative() {
    module make_bottom_holes(begin,end,pie_segments) {
        translate([0,0,-eps])
        difference() {
            cyl_sect(r1=end*diameter_bottom, r2=begin*diameter_bottom, h=thickness_bottom+2*eps);
            for (i=[0:pie_segments]) {
                connect(r=diameter_bottom,
                        w=width_connections,
                        h=thickness_bottom+2*eps,
                        phi=i*360/pie_segments);
            }
        }
    }
    module make_wall_holes(begin,end,pie_segments) {
        translate([0,0,begin*height])
        difference() {
            cylinder(r=diameter_bottom+diameter_top, h=(end-begin)*height);
            for (i=[0:pie_segments]) {
                connect(r=diameter_bottom+diameter_top,
                        w=width_connections,
                        h=(end-begin)*height,
                        phi=i*360/pie_segments);
            }
        }
    }

    union() {
        // inside
        difference() {
            cylinder(r1=diameter_bottom/2-thickness_walls, r2=diameter_top/2-thickness_walls, h=height+eps);
            cylinder(r=diameter_top+diameter_bottom, h=thickness_bottom);
        }

        // holes on wall
        union() {
            make_wall_holes(.05, .25, pie_segments_wall);
            make_wall_holes(.30, .50, pie_segments_wall);
            make_wall_holes(.55, .75, pie_segments_wall);
        }

        // holes on bottom
        union() {
            // make_bottom_holes(.08, .18, pie_segments_1);
            // make_bottom_holes(.22, .32, pie_segments_2);
            // make_bottom_holes(.36, .46, pie_segments_3);
            make_bottom_holes(.08, .25, pie_segments_1);
            // make_bottom_holes(.22, .32, pie_segments_2);
            make_bottom_holes(.29, .46, pie_segments_2);
        }
    }
}

// MAIN
difference() {
    positive();
    negative();
}
