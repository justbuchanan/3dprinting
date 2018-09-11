include <MCAD/materials.scad>;
include <MCAD/units.scad>;
include <MCAD/screw.scad>;

$fn=50;


// Lowes vinyl downspout
// https://www.lowes.com/pd/Severe-Weather-10-ft-White-Vinyl-Downspout/1007997
kDownspoutWidth = 3.188*inch;
kDownspoutHeight = (2+3/8)*inch;
kDownspoutLength=120*inch;
module downspout(len=kDownspoutLength) {
    color("white")
    cube([kDownspoutWidth, kDownspoutHeight, len]);
}


// downspout();

// include <downspout-thingiverse/2x3_End_Cap.stl>;
// import("downspout-thingiverse/2x3_End_Cap.stl");

module screw() {
    pitch = 3;
    length = 30;
    outside_radius = 4;
    inner_radius = 3;
    taper_ratio = 0.25;
    auger(pitch, length, outside_radius, inner_radius, taper_ratio);
}



module rounded_rect(w,h,r) {
    render() {
        union() {
            translate([r,r,0])
            circle(r=r);

            translate([r,h-r,0])
            circle(r=r);

            translate([w-r,h-r,0])
            circle(r=r);

            translate([w-r,r,0])
            circle(r=r);

            translate([r, 0, 0])
            square(size=[w-2*r,h]);

            translate([0, r, 0])
            square(size=[w,h-2*r]);
        }
    }
}

// tube: 0.25" id, 0.375 od

// i have 5/8" hole saw



module rr_cup(w=30,h=20,r=5,d=10,inset=3,thick=3, id=3, od=4, fitting_l=15) {
    difference() {
        difference() {
            linear_extrude(height=d)
            rounded_rect(w=w,h=h,r=r);

            translate([inset, inset, thick])
            linear_extrude(height=d)
            rounded_rect(w=w-inset*2,h=h-inset*2,r=r-inset);
        }

        translate([w/2, h/2, -20])
        cylinder(r=id/2, h=100);
    }

    translate([w/2,h/2,0])
    difference() {
        cylinder(r=od/2,h=fitting_l);

        translate([0,0,-fitting_l/2])
        cylinder(r=id/2, h=fitting_l*2);
    }
}

// translate([4*inch,-4*inch,0])
// rr_cup(w=3*inch,h=2*inch,r=15);



