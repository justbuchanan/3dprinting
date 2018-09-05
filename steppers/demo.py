#!/usr/bin/env python3

from solid import *
from solid.utils import *
from util import *

# nema17 stepper motor
use('steppers/utl.NEMA.scad')

Motor = Part("Nema 17 Stepper Motor")(nema17(True, True))

model = union()([
    Motor,
    translate([0, 50, 0])(Motor),
    translate([0, 100, 0])(PrintedPart("Plastic Block")(cube([10, 20, 30])), ),
])

print(generate_bom(model))
