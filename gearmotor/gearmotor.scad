use <MCAD/2Dshapes.scad>

// https://www.aliexpress.com/store/product/Sindax-GA12-N20-DC-12V-600RPM-High-Torque-Speed-Reduce-Intelligent-Car-Gear-Motor/1199185_32696998510.html?aff_platform=aaf&cpt=1509418787723&sk=zj6qB6AIM&aff_trace_key=814e57ab4b524eab8a8e8b0936be09d4-1509418787723-06666-zj6qB6AIM&terminal_id=7a1122be3d3b4810b1263b08ac79819b
// https://www.walmart.com/ip/DC-6V-30RPM-3mm-Shaft-Diameter-Mini-Metal-Gear-Motor-with-Gearwheel-Model-N20/45586408
// http://www.sears.com/uxcell-dc-6v-30rpm-3mm-shaft-mini-metal/p-SPM8859079629

// "infintesimal" increment
inc=0.0001;

motor_edge_outset=5;
motor_r = 6;
motor_len = 14; // length of metal motor body

motor_out_shaft_r=1.15/2;
motor_out_shaft_len=3;

// brass bushing on front of motor
bushing_th=0.4;
bushing_radius=3.96/2;

out_shaft_len=8;
out_shaft_radius=1.5;
out_shaft_mill_depth = 2*out_shaft_radius - 2.45;
box_sz = [12,10,9];

box_plate_th = 0.72;
box_post_r = 1.5;


motor_mount_hole_r = 0.5;

module gearbox() {
    // milled output shaft
    color("silver")
    translate([0,0,box_sz[2]]) {
        difference() {
            cylinder(r=out_shaft_radius, h=out_shaft_len);

            translate([-5, out_shaft_radius-out_shaft_mill_depth, 1.2])
            cube([10, 10, 10]);
        }
    }

    // box posts that line up with motor mounts
    motor_hole_points() {
        // post
        cylinder(r=box_post_r, h=box_sz[2]);

        // screw
        translate([0,0,box_sz[2]+0.1])
        rotate([180,0,0])
        screw();
    }

    hole_offset = box_sz[0]/2 - 1.2;
    hole_r = 1.3/2;

    plate_corner_rad = 1.5;
    module plate_profile() {
        roundedSquare([box_sz[0], box_sz[1]], plate_corner_rad);
    }

    // front plate
    translate([0,0,box_sz[2]-box_plate_th]) {
        linear_extrude(box_plate_th)
        difference() {
            plate_profile();

            // holes
            for (x=[-hole_offset, hole_offset]) {
                translate([x,0])
                circle(r=hole_r);
            }
        }

        // bushing
        cylinder(r=out_shaft_radius+0.5, h=1.5);
    }

    // "middle" plate
    translate([0,0,2.5+box_plate_th])
    linear_extrude(box_plate_th)
    difference() {
        plate_profile();

        // take chunk out of middle plate
        // translate([box_sz[0]*2/6, box_sz[1]/4])
        // roundedSquare([box_sz[0]/3, box_sz[1]/2], plate_corner_rad);
    }

    // back plate
    linear_extrude(box_plate_th)
    difference() {
        plate_profile();

        circle(r=bushing_radius);

        motor_hole_points()
        circle(motor_mount_hole_r);
    }
}

module output_shaft_profile() {
    r = out_shaft_radius;
    difference() {
        circle(r=r);
        translate([-r, out_shaft_radius-out_shaft_mill_depth])
        square([r*2, r*2]);
    }
}

module motor_hole_points() {
    d=box_post_r+0.4;
    for (a=[0,180]) {
        rotate(a)
        translate([box_sz[0]/2-d, box_sz[1]/2-d])
        children();
    }
}

module motor() {
    module motor_profile() {
        difference() {
            circle(r=motor_r);

            // square off the sides of the motor by subtracting offset squares
            for (r=[0,180]) {
                rotate([0,0,r])
                translate([-motor_r, motor_edge_outset])
                square([motor_r*2, motor_r*2]);
            }
        }
    }

    cap_length = 1;

    // metal motor body
    color("silver")
    difference() {
        // motor
        linear_extrude(motor_len)
        motor_profile();

        // 4 small divots on sides of motor
        transl=2.5;
        th=0.3;
        for (x=[transl,-transl]) {
            for (r=[0,180]) {
                rotate([0,0,r])
                translate([x, motor_edge_outset-th,motor_len/2])
                rotate([-90,0,0])
                linear_extrude(th+inc)
                roundedSquare([0.66, 4], 0.3);
            }
        }

        // motor mounting holes
        translate([0,0,-inc])
        motor_hole_points()
        cylinder(r=motor_mount_hole_r, h=3);

        // vent hole
        translate([0, 4, -inc])
        cylinder(r=0.4, h=3);
    }

    // bushing by output shaft of motor
    translate([0,0,-bushing_th])
    linear_extrude(bushing_th)
    difference() {
        circle(r=bushing_radius);
        circle(r=motor_out_shaft_r);
    }


    translate([0,0, motor_len]) {
        // black cap on back of motor
        color("black")
        linear_extrude(cap_length)
        motor_profile();
    }

    // metal electrical contact "tabs"
    tab_w=1.5;
    tab_th=0.3;
    tab_h = 1.55;
    tab_offset = 4;
    for (dir=[1,-1]) {
        translate([dir*tab_offset,0,motor_len+cap_length])
        color("silver")
        rotate([90,0,dir*90])
        linear_extrude(tab_th)
        difference() {
            // rounded rect plate
            roundedSquare([tab_w, tab_h*2], 0.3);

            // hole
            hole_rr=0.77/2;
            d = (tab_w - hole_rr*2) / 2;
            translate([0,tab_h-d-hole_rr])
            circle(r=hole_rr);
        }
    }

    // plastic ring on motor cap
    ring_len = 1.25;
    ring_inner_rad = 1.85 / 2;
    ring_outer_rad = 5.0 / 2;
    translate([0, 0, motor_len+cap_length])
    color("black")
    linear_extrude(ring_len)
    difference() {
        circle(r=ring_outer_rad);
        circle(r=ring_inner_rad);
    }

    // rear shaft
    color("silver")
    cylinder(r=ring_inner_rad, h=motor_len+cap_length+ring_len/2);

    // output shaft
    color("silver")
    rotate([180,0,0])
    cylinder(r=motor_out_shaft_r,h=motor_out_shaft_len);
}


// GA12-N20 DC 6v geared motor
module gearmotor() {
    translate([0,0,-box_sz[2]]) {
        gearbox();

        rotate([180,0,0])
        motor();
    }
}

module screw() {
    diameter = 1;
    length = 10;
    tolerance=0.4;

    drive_tolerance = pow(3*tolerance/CountersunkDriveAcrossCorners(diameter),2)
    + 0.75*tolerance;

    color("silver")
    PhillipsTip(diameter*0.8)
    union() {
      cylinder(h=diameter/2, r1=diameter, r2=diameter/2, $fn=24*diameter);

      translate([0,0,diameter/2-0.01])
        ScrewThread(diameter, length-diameter/2+0.01, tolerance=tolerance,
                tip_height=diameter, tooth_angle=50);
        // ScrewThread(outer_diam, height, pitch=0, tooth_angle=30, tolerance=0.4, tip_height=0, tooth_height=0, tip_min_fract=0) {
    }
}
