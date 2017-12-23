use <obiscad/obiscad/attach.scad>


ball_bearing_connector = [
    [0,0,0],
    [0,0,1],
    0
];

module ball_bearing(
    outer_r = 25,
    inner_r = 10,
    width = 8,

    wall_th = 2,
    spacing = 0.4
    ) {

    ball_diameter = outer_r - inner_r - 2*wall_th - 2*spacing;
    center_radius = inner_r + wall_th + spacing + ball_diameter/2;
    ball_spacing = 0.2;
    center_circum = 2 * PI * center_radius;
    num_balls = floor(center_circum / (ball_diameter + ball_spacing)); // note: this is an approximation
    ang_inc = 360 / num_balls;

    module balls() {
        translate([0, 0, width/2])
        for (i=[0:ang_inc:360]) {
            rotate([0, 0, i])
            translate([0, inner_r+wall_th+spacing+ball_diameter/2, 0])
            sphere(r=ball_diameter/2);
        }
    }

    // module v1() {
    //     linear_extrude(width)
    //     difference() {
    //         circle(r=inner_r+wall_th);
    //         circle(r=inner_r);
    //     }

    //     linear_extrude(width)
    //     difference() {
    //         circle(r=outer_r);
    //         circle(r=outer_r-wall_th);
    //     }

    //     balls();
    // }

    module v2() {
        difference() {
            linear_extrude(width)
            difference() {
                circle(r=outer_r);
                circle(r=inner_r);
            }

            // cutout for balls
            translate([0,0,width/2])
            rotate_extrude(convexity=10)
            translate([center_radius,0,0])
            circle(r=ball_diameter/2+spacing);
        }

        balls();
    }

    v2();
}


module demo() {
    $fn=100;
    ball_bearing();
    connector(ball_bearing_connector);
}

demo();
