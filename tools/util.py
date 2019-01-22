# Credits:
# A large chunk of this was borrowed from https://github.com/Obijuan/obiscad

from solid import *
from solid.utils import *
import numpy as np
from functools import reduce
import math

INC = 0.001


class Connector:
    def __init__(self, pos, dir, angle=0):
        super().__init__()
        # assert isinstance(pos, np.array)
        # assert isinstance(dir, np.array)
        self._pos = np.array(pos)
        self._dir = np.array(dir)
        self._angle = angle

    @property
    def pos(self):
        return self._pos

    @property
    def dir(self):
        return self._dir

    # angle is in degrees
    @property
    def angle(self):
        return self._angle

    def draw(self):
        return color("Gray")(attach(self,
                                    Connector([0, 0, 0], [0, 0, 1]))(vectorz(
                                        np.linalg.norm(self.dir) * 6,
                                        l_arrow=2,
                                        mark=True)))

    def translated(self, t):
        new_pos = self.pos + t
        return Connector(new_pos, self.dir, self.angle)

    def rotated(self, r):
        return Connector(self.pos, self.dir, self.angle + r)


#------------------------------------------------------------------
#-- Draw a vector poiting to the z axis
#-- This is an auxiliary module for implementing the vector module
#--
#-- Parameters:
#--  l: total vector length (line + arrow)
#--  l_arrow: Vector arrow length
#--  mark: If true, a mark is draw in the vector head, for having
#--    a visual reference of the rolling angle
#------------------------------------------------------------------
def vectorz(l=10, l_arrow=4, mark=False):
    #-- Draw a sphere in the vector base
    v = sphere(r=1 / 2)

    #-- vector body length (not including the arrow)
    lb = l - l_arrow

    #-- Draw the arrow
    v += translate([0, 0, lb / 2])(translate([0, 0, lb / 2])(cylinder(
        r1=2 / 2, r2=0.2, h=l_arrow)))

    #-- Draw the mark
    if mark:
        v += translate([0, 0, lb / 2])(translate([0, 0, lb / 2 + l_arrow / 2])(
            translate([1, 0, 0])(cube([2, 0.3, l_arrow * 0.8], center=True))))

    #-- Draw the body
    v += translate([0, 0, lb / 2])(cylinder(r=1 / 2, h=lb, center=True))

    return v


def cylinder_connectors(cyl):
    return {
        'bottom': [[0, 0, 0], [0, 0, -1], 0],
        'top': [[0, 0, cyl.params['h']], [0, 0, 1], 0],
    }


def invert_connector(c):
    normal = np.array(c[1])
    inverted = c.copy()
    inverted[1] = normal * -1
    return inverted


def rad2deg(r):
    return r * 180 / math.pi


def anglev(u, v):
    c = np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(
        v)  # cosine of the angle
    return math.acos(np.clip(c, -1, 1))


def find_descendent_part(tree):
    node = tree
    while True:
        if isinstance(node, Part):
            return node
        assert len(node.children) == 1
        node = node.children[0]


# https://stackoverflow.com/questions/6802577/python-rotation-of-3d-vector
def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    # print(axis)
    axis = np.asarray(axis)
    # print(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    # print(axis)
    a = math.cos(theta / 2.0)
    # print(a)
    b, c, d = -axis * math.sin(theta / 2.0)
    # print(b)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    # yapf: disable
    x = np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac), 0],
                  [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab), 0],
                  [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc, 0],
                  [0,                         0,                 0, 1]])
    # yapf: enable

    return x


# copied from obiscad/attach.scad
# TODO: properly attribute or rewrite
def create_attach_xform(a, b):
    assert isinstance(a, Connector)
    assert isinstance(b, Connector)

    #-------- Calculations for the "orientate operator"------
    #-- Calculate the rotation axis
    raxis = np.cross(b.dir, a.dir)
    # print("raxis: %s" % str(raxis))

    #-- Calculate the angle between the vectors
    ang = anglev(b.dir, a.dir)

    #-- Apply the transformations to the child ---------------------------
    #-- Place the attachable part on the main part attachment point
    #-- Orientate operator. Apply the orientation so that
    #-- both attachment axis are paralell. Also apply the a1 angle
    #-- Attachable part to the origin
    # TODO: is angle a1+a2 or a1-a2?
    t = xform_translate(a.pos)
    t = t @ rotation_matrix(a.dir, deg2rad(a.angle + b.angle))
    if np.linalg.norm(raxis) > 0.0001:
        t = t @ rotation_matrix(raxis, ang)
    t = t @ xform_translate(-b.pos)
    return t


def attach(con1, con2, gap=0):
    assert isinstance(con1, Connector)
    assert isinstance(con2, Connector)
    con1 = con1.translated(np.array(con1.dir) * gap)
    r = multmatrix(create_attach_xform(con1, con2))
    return r


def iterate_tree(root):
    yield root
    for c in root.children:
        yield from iterate_tree(c)


# yields node, node's parent, node's grandparent, etc
def iterate_lineage(node, stop_node=None):
    current = node
    while current is not None:
        yield current
        # end after yielding the stop_node
        if stop_node is not None and current == stop_node:
            break
        current = current.parent


def deg2rad(a):
    return a * math.pi / 180


# rotation matrices
def xform_rotate_x(a):
    return np.array([[1, 0, 0,
                      0], [0, cos(deg2rad(a)), -math.sin(deg2rad(a)), 0],
                     [0, sin(deg2rad(a)),
                      math.cos(deg2rad(a)), 0], [0, 0, 0, 1]])


def xform_rotate_y(a):
    return np.array([[math.cos(deg2rad(a)),
                      math.sin(deg2rad(a)), 0, 0], [0, 1, 0, 0],
                     [-math.sin(deg2rad(a)), 0,
                      math.cos(deg2rad(a)), 0], [0, 0, 0, 1]])


def xform_rotate_z(a):
    return np.array([[math.cos(deg2rad(a)), -math.sin(deg2rad(a)), 0, 0],
                     [math.sin(deg2rad(a)),
                      math.cos(deg2rad(a)), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def xform_translate(t=[0, 0, 0]):
    return np.array([[1, 0, 0, t[0]], [0, 1, 0, t[1]], [0, 0, 1, t[2]],
                     [0, 0, 0, 1]])


def xform_scale(s=[1, 1, 1]):
    return np.array([[s[0], 0, 0, 0], [0, s[1], 0, 0], [0, 0, s[2], 0],
                     [0, 0, 0, 1]])


def xform_rotate(r=[0, 0, 0]):
    return xform_rotate_z(r[2]) @ xform_rotate_y(r[1]) @ xform_rotate_x(r[0])


# https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
# @param v unit vector axis of rotation
# @param a angle of rotation about the vector
def xform_rotate_axis(a, v):
    return rotation_matrix(v, a)


def xform_extract_translate(x):
    return x[:3, 3]


def xform(t=[0, 0, 0], s=[1, 1, 1], r=[0, 0, 0]):
    return xform_rotate(r) @ xform_translate(t) @ xform_scale(s)


def xform_eye():
    return np.eye(4)


def xform_from_node(node):
    x = None
    if isinstance(node, translate):
        # print('translate')
        x = xform_translate(node.params['v'])
    elif isinstance(node, scale):
        # print('scale')
        x = xform_scale(node.params['v'])
    elif isinstance(node, multmatrix):
        # print('multmatrix')
        x = np.array(node.params['m'])
    elif isinstance(node, rotate):
        # TODO: there's also a variant using the 'v' parameter
        x = np.array(node.params['a'])
        # print("rotate", x)
        x = xform(r=x)  # TODO: rotate-only
    return x


# Calculate the transform needed to move a sibling of @root into the space of @child's children
# Example:
#
#  part = cube([1, 1, 1]);
#  root = transform([10, 20, 30]) rotate([30, 0, 60]) part();
#  # The X transform matrix incorporates the transform and rotation applied to the part.
#  x = accumulate_transforms(root, part);
#  # Now an equivalent model can be made using the transform matrix
#  root2 = multmatrix(x) part();
#
# returns a numpy transform matrix
# includes @child as a transform object
def accumulate_transforms(root, child):
    transforms = list(
        reversed([xform_from_node(n) for n in iterate_lineage(child, root)]))
    transforms = list(filter(lambda n: n is not None, transforms))
    if len(transforms) == 0:
        return xform_eye()
    return reduce(np.matmul, transforms)


def xform_unittest():
    c = cube([2, 3, 5])
    p = translate([0, 30, 10])(rotate([30, 0, 0])(translate([1, 2, 3])(c)))
    # p = translate([1, 2, 3])(c)

    m = accumulate_transforms(p, c)
    # print("m = ", m)

    p = union()([
        # original
        p,
        # copy with transform applied - it should mirror the original
        translate([20, 0, 0])(multmatrix(m)(c))
    ])

    scadfile = "tx_test.scad"
    scad_render_to_file(p, scadfile)
    print("wrote %s" % scadfile)


# Provides a "con" property, which is a collection of named connectors
class Connectable:
    def __init__(self):
        super().__init__()
        self.con = {}

    # Dictionary of named connectors
    @property
    def con(self):
        return self._con

    @con.setter
    def con(self, value):
        self._con = value

    def draw_connectors(self):
        return union()([con.draw() for name, con in self.con.items()])

    def __matmul__(self, other_con):
        assert 'main' in self.con
        return attach(other_con, self.con['main'])(self)


# A wrapper element that can be used to annotate certain objects as "things".
class Thing(part, Connectable):
    def __init__(self,
                 typename=None,
                 tag=None,
                 is_atomic=False,
                 collect_subconnectors=False):
        part.__init__(self)
        Connectable.__init__(self)
        self.typename = typename or self.__class__.__name__
        self.tag = tag
        self.is_atomic = is_atomic
        self._collect_subconnectors = collect_subconnectors

    def __str__(self):
        return "Thing '%s'" % self.typename

    # Identifies the instance of this part (i.e. "front_left")
    # Should be unique
    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    # Identifies what this part is (i.e. "Wheel", "Sprocket")
    @property
    def typename(self):
        return self._typename

    @typename.setter
    def typename(self, value):
        self._typename = value

    @property
    def is_atomic(self):
        return self._is_atomic

    @is_atomic.setter
    def is_atomic(self, value):
        self._is_atomic = value

    @property
    def collect_subconnectors(self):
        return self._collect_subconnectors

    def __hash__(self):
        return hash(self.typename)

    def __eq__(self, other):
        if not isinstance(other, Thing):
            return False

        return self.typename == other.typename

    def add(self, child):
        OpenSCADObject.add(self, child)

        # add connectors from sub-objects
        if self.collect_subconnectors:
            for subpart in self.iterate_subparts():
                x = accumulate_transforms(self, subpart)
                for conname, con in subpart.con.items():
                    # name = subpart.name + ":" + conname
                    name = conname
                    # TODO: transform con using x
                    self.con[name] = con

        return self

    def iterate_subparts(self):
        for c in self.children:
            yield from iterate_parts(c)


# atomic part (contains no subparts)
class Part(Thing):
    def __init__(self, typename=None, tag=None, collect_subconnectors=True):
        super(Part, self).__init__(
            typename,
            tag,
            is_atomic=True,
            collect_subconnectors=collect_subconnectors)


class PrintedPart(Part):
    pass


def part_tree_str(model, tostr=lambda p, indent: '  ' * indent + p.typename):
    def _yield_part_tree(model, indent=0):
        if isinstance(model, Thing):
            yield tostr(model, indent)
            indent += 1
            if model.is_atomic:
                return

        for c in model.children:
            yield from _yield_part_tree(c, indent=indent)

    return '\n'.join(list(_yield_part_tree(model)))


def part_tree_connector_str(model):
    def tostr(p, indent):
        base_indent = '  ' * indent
        s = base_indent + p.typename
        if p.tag is not None:
            s += ":" + p.tag
        if len(p.con):
            prefix = "\n%s->" % base_indent
            s += prefix + prefix.join(p.con.keys())
            s += "\n"
        return s

    return part_tree_str(model, tostr=tostr)


def part_grid(model, spacing=100):
    all_parts = sorted(iterate_parts(model), key=lambda p: p.typename)
    names_and_parts = [(p.typename, p) for p in all_parts]
    return item_grid(names_and_parts, spacing)


# items: list of (name, scadobj) tuples
def item_grid(items, spacing=100):
    grid_sz = math.ceil(math.sqrt(len(items)))
    part_grid = union()

    for i in range(len(items)):
        name = items[i][0]
        obj = items[i][1]
        x = i % grid_sz
        y = floor(i / grid_sz)
        txt = translate([0, -30, 0])(text(name))
        part_grid += translate([x * spacing, y * spacing, 0])(obj, txt)
    d = (grid_sz - 1) * spacing / 2
    return translate([-d, -d, 0])(part_grid)


def iterate_class(model, klass, enter_items=True):
    if isinstance(model, klass):
        yield model
        # TODO: is_atomic
        if not enter_items:
            return

    for c in model.children:
        yield from iterate_class(c, klass, enter_items=enter_items)


def iterate_things(model):
    yield from iterate_class(model, Thing)


def iterate_parts(model):
    yield from iterate_class(model, Part, enter_items=False)


def count_map(items):
    counts = {}
    for item in items:
        key = item
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1
    return counts


def generate_bom(model):
    def collect_partmap(parts_list):
        out = ""
        partcounts = count_map(parts_list)
        for part, count in partcounts.items():
            out += part.name + " x %d\n" % count
        return out

    all_parts = list(iterate_parts(model))

    bom = "Parts\n-----------------\n"
    bom += collect_partmap(all_parts) + "\n"

    bom += "3d printed parts\n--------------------\n"
    bom += collect_partmap(
        filter(lambda x: isinstance(x, PrintedPart), all_parts)) + "\n"
    return bom


# translate obiscad connector
def translate_con(con, t):
    tmp = con.copy()
    tmp[0] = [con[0][i] + t[i] for i in range(3)]
    return tmp
