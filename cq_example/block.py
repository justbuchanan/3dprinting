import cadquery as cq
import cqparts
from cqparts.params import *

class MyBlock(cqparts.Part):
    def make(self):
        # Copied from cadquery examples
        (length,height,bearing_diam, thickness,padding) = ( 30.0, 40.0, 22.0, 10.0, 8.0)

        result = cq.Workplane("XY").box(length,height,thickness).faces(">Z").workplane().hole(bearing_diam) \
                .faces(">Z").workplane() \
                .rect(length-padding,height-padding,forConstruction=True) \
                .vertices().cboreHole(2.4, 4.4, 2.1)
        return result

show_object(MyBlock())
