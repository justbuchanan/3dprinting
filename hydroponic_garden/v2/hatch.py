# hexagonal hole pattern
def hatch(sz=[100,100], r=2, wall_th=1):
    h = square(sz)
    dx = r*2*.866 + wall_th
    dy = r*1.5 + wall_th

    holes = union()
    for i in range(ceil(sz[0]/r)):
        for j in range(ceil(sz[1]/r)):
            # shirt alternate layers horizontally relative to eachother
            xshift = r if (j % 2 == 0) else 0
            # cut out a hexagon at each location
            holes += translate([i*dx+xshift, j*dy])(
                rotate(30)(circle(r=r, segments=6)))
    return h - holes


        # # add cross-hatch filter/screen to entry holes
        # # TODO: this doesn't print well because it's a flat bridge over a gap
        # screen_th=2
        # for x in [0, dx]:
        #     conn += translate([w/2+wall_th - hole_r*1.5 + x, h/2+wall_th-hole_r*1.5, -screen_th])(
        #                 linear_extrude(screen_th)(
        #                     hatch(sz=[hole_r*3, hole_r*3], r=2, th=1.2)))

# A circle with hexagonal holes.
def hatchring(
    r=50,
    hex_th=0.5,
    circ_th=1,
    ):

    # hatch
    h = translate([-r*2, -r*2])(
            hatch(sz=[r*4, r*4], r=1, wall_th=hex_th))
    # boundary circle
    ring = circle(r=r) - circle(r=r-circ_th)
    return render()(
        intersection()(
            h + ring,
            # trim off everything outside the circle
            circle(r)
        )
    )

# def ball():
#     return difference()(
#         sphere(r=10),
#         [rotate([i*360/20,j*360/20,0])(cylinder(r=1,h=100)) for i in range(20) for j in range(20)]
#         )

