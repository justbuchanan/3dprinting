include <hydroponic_garden/hose_fitting.scad>;

nozzle_len = 10;


inner_thread_od = 9.5; // was 10, tried 7 - was pretty small

// Tolerance value is difference in size b/w threads. male_thread_r + tol = female thread radius
splitter_thread_tol = 0.2;
splitter_thread_od = inner_thread_od; // TODO: change value

module splitter_thread(length, tol=0, cs=2) {
    screw_thread(
        splitter_thread_od + tol*2,
        1.5, // tooth ht. was previously 2 for test prints
        45, // tooth shape (degrees). was previuosly 55
        length,
        PI/2, // resolution
        cs // countersunk ends
    );
}

input_thread_len = 7;


module splitter(demo=false) {
    output_angle = 28;
    // dist from interior edge of nozzle to the center point of the splitter.
    output_extra_len = 7;
    translate_noz = 2.5;

    extra_thread = 1;
    thread_ht = input_thread_len + extra_thread;
    cyl_ht = thread_ht + 2;

    inc = 0.01;

    nozzle_offsets = [translate_noz,0,-translate_noz];

    module nozzle_transform(i) {
        // maps from [0, 1, 2] -> [1, 0, -1]
        ii = i - 1;

        translate([0,0,cyl_ht])
        rotate([0,0,ii*120])
        translate([translate_noz,0,0])
        rotate([0,output_angle,0])
        translate([0, 0, output_extra_len])
        children();
    }

    module main() {
        branch_cyl_r_extra = 0;

        branch_cyl_extra_len = 5;



        module bigpiece() {
            // large cylinder for the base
            // The thread takes up most of this space
            r = inner_thread_od/2 + 2;
            cylinder(r=r,h=cyl_ht);

            // for (i=[0:2])
            // translate([nozzle_offsets[i],0,cyl_ht])
            translate([0,0,cyl_ht])
            sphere(r=r);


            // output nozzles
            for (i=[0:2]) {
                nozzle_transform(i)
                union() {
                    nozzle(length=nozzle_len, r_bottom=nozzle_r_large);

                    l = output_extra_len + branch_cyl_extra_len;
                    translate([0,0,-l+inc])
                    cylinder(r=nozzle_r_large+branch_cyl_r_extra, h=l);
                }
            }
        }

        difference() {
            bigpiece();

            union() {
                // take the main part and drill a threaded area in the base
                translate([0,0,-inc])
                splitter_thread(length=thread_ht, tol=splitter_thread_tol, cs=1);

                // tapered surface to match input piece
                inc = 0.001;
                translate([0,0,-inc])
                rotate([180,0,0])
                connection_taper();
            }
        }
    }

    module waterflow() {
        for (i=[0:2]) {
            nozzle_transform(i)
            translate([0,0,-output_extra_len-5])
            union() {
                // sphere(r=nozzle_r_inner);

                // cylinder of water through each nozzle
                cylinder(r=nozzle_r_inner,h=output_extra_len+nozzle_len+10);
            }
        }

        translate([0,0,cyl_ht])
        sphere(r=translate_noz+nozzle_r_inner/2);

        // center waterway up through the bottom
        translate([0,0,-10])
        cylinder(r=inner_thread_od/2-1,h=cyl_ht+10);
    }

    if (demo) {
        % main();
        color("blue")
        waterflow();
    } else {
        difference() {
            main();
            waterflow();
        }
    }
}

flange_extra_r=1.5;
flange_thick=1.5;
flange_r = splitter_thread_od/2+flange_extra_r;

module connection_taper(tdh=2) {
    translate([0,0,-tdh])
    cylinder(r1=splitter_thread_od/2-1,r2=flange_r,h=tdh);
}


// nozzle with threaded base - it screws into the bottom of the main piece and is
// the input connector
module splitter_input_tip(
    demo=false,
    thread_len=input_thread_len)
{

    thread_len = thread_len + flange_thick;
    module main() {
        // threaded part
        splitter_thread(length=thread_len);

        translate([0,0,thread_len-flange_thick])
        connection_taper();

        // flange
        translate([0,0,thread_len-flange_thick])
        cylinder(r=flange_r,h=flange_thick);

        // nozzle
        translate([0,0,thread_len])
        nozzle(nozzle_len);
    }

    module water() {
        translate([0,0,-10])
        cylinder(r=nozzle_r_inner,h=40);
    }

    if (demo) {
        % main();
        color("blue")
        water();
    } else {
        difference() {
            main();
            water();
        }
    }
}

module all(demo=false) {
    splitter(demo=demo);

    translate([15, 15, 0])
    splitter_input_tip(demo=demo);
}

// all(demo=true);
