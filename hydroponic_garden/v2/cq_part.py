import cadquery as cq
from math import pi, sin, cos


h = 58.7
w = 78.7
corner_r = 15

# b = cq.Workplane("XY").box(w, h, 5).edges("|Z").fillet(corner_r)


# c = cq.Workplane("XY") \
#     .moveTo(0, h/2) \
#     .lineTo(w/2,h/2) \
#     .lineTo(w/2, -h/2) \
#     .lineTo(-w/2, -h/2) \
#     .lineTo(-w/2, h/2) \
#     .close() \
#     .extrude(3)

# c = c.faces(">Z or <Z").shell(2)

# s = cq.Workplane("XY").box(1,1,1).faces(">Z").workplane().pushPoints([(-0.3,0.3),(0.3,0.3),(0,0)])
# body = s.circle(0.05).cutThruAll()



# s = cq.Workplane("XY").rect(w, h).extrude(3).edges("|Z").fillet(corner_r)


def part():
    s = cq.Workplane("XY").rect(w * 3, h).extrude(10).edges("|Z").fillet(corner_r)

    wp = s.faces(">Z").workplane()
    s = wp.pushPoints([(-w,0), (w,0)]).rect(w,h).extrude(8).edges("|Z").fillet(corner_r)
    # s2 = wp.move(w*2,0).rect(w,h).extrude(2)
    # .rect(w,h).move(w*2, 0).rect(w,h).extrude(3)

    return s


# p = part()

def diffed():
    wp = cq.Workplane("XY")

    wall_th = 1

    x = wp.rect(w,h).extrude(10).edges("|Z").fillet(corner_r)
    x = x.faces(">Z").rect(w-wall_th,h-wall_th).cutThruAll()

    return x

def circle_with_holes():
    result = cq.Workplane("front").circle(3.0) #current point is the center of the circle, at (0,0)
    result = result.center(1.5, 0.0).rect(0.5, 0.5) # new work center is  (1.5, 0.0)

    result = result.center(-1.5, 1.5).circle(0.25) # new work center is ( 0.0, 1.5).
    #the new center is specified relative to the previous center, not global coordinates!

    result = result.extrude(0.25)
    return result

# r = circle_with_holes()





# wall_th = 1
# wp = cq.Workplane("XY")
# x = wp.rect(w,h).center(1,1).rect(w-6,h-6).extrude(3)
# # x = x.faces(">Z").rect(w-wall_th,h-wall_th).cutThruAll()



# rounded rect. clockwise starting at top left corner
def rrect(wp, w, h, r):
    T = r*cos(pi/4)
    return wp.moveTo(0, h-r) \
        .threePointArc( (r-T, h-r+T), (r,h)) \
        .hLine(w-2*r) \
        .threePointArc( (w-r+T, h-r+T), (w, h-r)) \
        .vLine(-(h-2*r)) \
        .threePointArc( (w-r+T, r-T), (w-r, 0)) \
        .hLine(-(w-2*r)) \
        .threePointArc( (r-T, r-T), (0, r) ) \
        .close() \
        .moveTo(0,0)


# a = rrect(cq.Workplane("XY"), w, h, corner_r).extrude(1)
# # b = a.faces(">Z")
# a = rrect(a.faces(">Z"), w-10, h-10, corner_r-4).extrude(3)





a = cq.Workplane("XY").rect(10,10).center(3,3).rect(2,2).extrude(4)
