$fn=50;

r=2;

n2 = 3;

for (i=[0:n2-1]) {
    for (j=[0:n2-1]) {
        sp = r*3;
        translate([i*sp,j*sp,0])
        sphere(r=1.5);
    }
}
