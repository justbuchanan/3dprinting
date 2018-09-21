include <gearmotor.scad>
use <parametric_gears.scad>



module gears(sel) {
    bevel_gear_pair(
        gear1_teeth=20,
        gear2_teeth=7,
        axis_angle=90,
        outside_circular_pitch=250,
        face_width=5,
        clearance = 0.1,
        bore_diameter=0,
        gear_thickness = 4,
        sel=sel
    );
}


difference() {
    gears(2);

    dr = 0.1; // add this amount to the radius of the cutout
    c_scale = (out_shaft_radius + dr) / out_shaft_radius;

    translate([0,0,-1000])
    linear_extrude(2000)
    scale(c_scale)
    output_shaft_profile();
}

// echo($fn);
$fn=150;