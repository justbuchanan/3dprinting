from solid import *
import random


seed = random.randint(0,10000)
print("seed: %d" % seed)
# seed = 7675

random.seed(seed)

def tree(depth):
    if depth == 0:
        # a leaf
        return color("green")(
                        translate([10,0,0])(
                            scale([2, 1])(
                                circle(5))))

    branch_th = 3 * depth
    a1 = 30
    # a1 = random.normalvariate(a1, a1/8)
    a2 = -a1
    l = 10 + depth * 4

    weightedChoices = [depth-1]*20 + [depth]*3
    subd = random.choice(weightedChoices)

    subd = depth - 1

    t = cylinder(r=branch_th/2, h=l),
    for a in [a1, a2]:
        t+= translate([0, 0, l])(
                rotate([0,a, 45])(
                    union()(
                        cylinder(r1=branch_th/2, h=l, r2 = branch_th/2 - 3/2),

                        translate([0,0,l])(tree(subd)),
                    )
                )
            )

    return t


model = tree(7)

if __name__ == '__main__':
    # write scad
    fn = 100
    fname = "out.scad"
    scad_render_to_file(model, fname, file_header='$fn=%d;' % fn)
    print("Wrote scad: '%s'" % fname)
