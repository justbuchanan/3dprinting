// Status: this design was not used. It's saved in case parts of it are useful later
include <MCAD/materials.scad>;
include <MCAD/units.scad>;
include <downspout.scad>;

$fn = 100;

ft = 12*inch;

// two*four boards are these dimensions - not 2"*4"
four = 89;
two = 38;
one=two/2;

module vertical(len) {
    cube([4*inch, 2*inch, len]);
}


module frame() {
    h = 50*inch;
    vertical(h);

    translate([0, 36*inch, 0])
    vertical(h);
}




// Lowes vinyl downspout
// https://www.lowes.com/pd/Severe-Weather-10-ft-White-Vinyl-Downspout/1007997
kDownspoutWidth = 3.188*inch;
kDownspoutHeight = (2+3/8)*inch;
kDownspoutLength=120*inch;
module downspout(len=kDownspoutLength) {
    color("white")
    cube([kDownspoutWidth, kDownspoutHeight, len]);
}

kBucketHeight = 15*inch;
kBucketTopSpacing = 10*inch;
kLayerHeight = 4*inch;
kLayer1VerticalSpace = 14*inch;
kLightHeight = 5*inch;
kLayer2VerticalSpace = 18*inch;


module cabinet() {
    d = 13*inch;
    w = 30*inch;
    h = kBucketHeight + kBucketTopSpacing + kLayerHeight * 2 + kLightHeight * 2 + kLayer1VerticalSpace + kLayer2VerticalSpace;

    // color("gray", 0.1)
    // cube([w, d, h]);

    color(Oak)
    cube([30*inch, 5*inch, 3*inch]);
}

// cabinet();


// downspout();

kBucketHeight = 17*inch;
kBucketRadius = 6*inch;

module bucket() {
    cylinder(r=kBucketRadius, h=kBucketHeight);
}

// translate([24*inch,0,0])
// bucket();




module frame() {
    tray_w = 20*inch;
    tray_d = 12*inch;
    w = tray_w + 1;
    d = tray_d + two*2;
    tray_h = one;

    cube([two, two, 5*ft]);

    translate([0, d-two, 0])
    cube([two, two, 5*ft]);

    translate([w-two, 0, 0])
    cube([two, two, 5*ft]);

    translate([w-two, d-two, 0])
    cube([two, two, 5*ft]);

    translate([0,two,10*inch])
    cube([w, tray_d, tray_h]);

    translate([0,two,(10+3+16+5+3)*inch])
    cube([w, tray_d, tray_h]);

    translate([0,two,5*ft - 3*inch])
    cube([w, tray_d, tray_h]);
}

frame();

