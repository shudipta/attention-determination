import math

# from types import *
# from asyncio.test_utils import force_legacy_ssl_support

PI = math.pi
EPS = 1e-09


def is_equal(a, b):
    return abs(a - b) <= EPS


def is_zero(a):
    return abs(a) <= EPS


class Pt:
    __slots__ = ["x", "y"]

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    # def print(self):
    #     s = self.__slots__
    #     for i in range(len(s)):
    #
    #         if i == 0:
    #             print("{0} = {1}".format(s[i], self.__getattribute__(s[i])), end='')
    #         else:
    #             print(", {0} = {1}".format(s[i], self.__getattribute__(s[i])), end='')
    #     print("")

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)


class Vector:
    __slots__ = ["x", "y"]

    def __init__(self, x: object = 0.0, y: object = 0.0) -> object:
        self.x = x
        self.y = y

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __eq__(self, other):
        return is_zero(self.x - other.x) and is_zero(self.y - other.y)

    def __ne__(self, other):
        return not (self == other)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __mul__(self, other):
        if type(other) in (int, float):
            return Vector(self.x * other, self.y * other)
        elif type(other) is Vector:
            # scaller or dot product
            return self.x * other.x + self.y * other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    # Vector or cross porduct
    def __mod__(self, other):
        return self.x * other.y - other.x * self.y

    def square_distance(self):
        return self * self

    def value(self):
        return math.sqrt(self.square_distance())

    def angle_with_x_axis(self):
        ang = math.atan2(self.y, self.x)
        return ang + 2 * PI if ang + EPS < 0.0 else ang


class ScanLine:
    __slots__ = ["ang", "obj_idx", "pt_idx"]

    def __init__(self, ang=0.0, obj_idx=0, pt_idx=0):
        self.ang = ang
        self.obj_idx = obj_idx
        self.pt_idx = pt_idx

    def __str__(self):
        return '({0}, {1}, {2})'.format(self.ang, self.obj_idx, self.pt_idx)

    def __repr__(self):
        return str(self)


class Segment:
    __slots__ = ["a", "b"]

    def __init__(self, a=Vector(), b=Vector()):
        self.a = a
        self.b = b

    def distance_from(self, p):
        if ((self.b - self.a) * (p - self.a)) + EPS < 0.0:
            return (p - self.a).value()
        elif ((self.a - self.b) * (p - self.b)) + EPS < 0.0:
            return (p - self.b).value()
        else:
            return abs((self.b - self.a) % (p - self.a)) / (self.b - self.a).value()

    def __str__(self):
        return '({0}, {1})'.format(self.a, self.a)


class Obj:
    __slots__ = ["idx", "w", "h", "pts", "enter_ang", "leave_ang", "visible_area", "attention"]

    def __init__(self, x1=0.0, y1=0.0, w=0.0, h=0.0, idx=0):
        self.idx = idx
        self.w = w
        self.h = h

        self.pts = []
        self.pts.append(Vector(x1, y1))
        self.pts.append(Vector(x1 + w, y1))
        self.pts.append(Vector(x1 + w, y1 + h))
        self.pts.append(Vector(x1, y1 + h))

        self.visible_area = 0.0

        self.enter_ang = self.leave_ang = self.attention = 0.0

    def __str__(self):
        return '''({0}, {1}, {2}, {3}, 
            {4}, {5}, {6}, {7}'''.format(self.idx, self.w, self.h, self.pts,
                                         self.enter_ang, self.leave_ang,
                                         self.visible_area, self.attention)

    def area(self):
        return self.w * self.h

    def append_scan_lines(self, scan_lines, face):
        self.enter_ang = 1e9
        self.leave_ang = -1e9
        p1 = p2 = 0

        for i in range(4):
            ang = (self.pts[i] - face).angle_with_x_axis()
            if self.enter_ang > ang:
                self.enter_ang = ang
                p1 = i
            if self.leave_ang < ang:
                self.leave_ang = ang
                p2 = i

        scan_lines.append(ScanLine(self.enter_ang, self.idx, p1))
        scan_lines.append(ScanLine(self.leave_ang, self.idx, p2))

    def face_dist(self, face):
        return min(Segment(self.pts[i], self.pts[(i + 1) % 4]).distance_from(face) for i in range(4))

    def attention_dist(self, face, attention):
        center = Vector(self.pts[0].x + self.w / 2.0, self.pts[0].y + self.h / 2.0)
        return Segment(face, attention).distance_from(center)


class Line:
    __slots__ = ["a", "b", "c"]

    def __init__(self, p, q):
        self.a = p.y - q.y
        self.b = q.x - p.x
        self.c = - self.a * p.x - self.b * p.y


def det(a, b, c, d):
    return a * d - b * c


def intersection_line(a, b, c, d):
    m = Line(a, b)
    n = Line(c, d)
    zn = det(m.a, m.b, n.a, n.b)

    return Vector(- det(m.c, m.b, n.c, n.b) / zn, - det(m.a, m.c, n.a, n.c) / zn)


def clip_polygon(a: Vector, b: Vector, poly: "list of Vectors"):
    poly_size = len(poly)
    clipped = []
    for i in range(poly_size):
        e = (b - a) % (poly[i] - a)
        f = (b - a) % (poly[(i + 1) % poly_size] - a)

        if e + EPS > 0.0 and f + EPS > 0.0:
            clipped.append(poly[i])
        elif e + EPS > 0.0 and f + EPS < 0.0:
            clipped.append(poly[i])
            clipped.append(intersection_line(poly[i], poly[(i + 1) % poly_size], a, b))
        elif e + EPS < 0.0 and f + EPS > 0.0:
            clipped.append(intersection_line(poly[i], poly[(i + 1) % poly_size], a, b))
        # else if(e + eps < 0.0 && f + eps < 0.0)

    return clipped


def clip_obj(face: Vector, a: Vector, b: Vector, obj: list):
    clipped_obj = clip_polygon(face, a, obj)
    return clip_polygon(b, face, clipped_obj)


def polygon_area(poly: list):
    poly_size = len(poly)
    if poly_size == 0:
        return 0.0

    return sum((poly[i] % poly[(i + 1) % poly_size]) for i in range(poly_size)) / 2.0


def cmp_scan_lines(line: ScanLine):
    return line.ang

#######################################################
#            start main program from here             #
#######################################################

inp = list(map(float, input("enter face point f(x, y): ").split()))
face = Vector(inp[0], inp[1])

inp = list(map(float, input("enter face view angles point p1(x, y), p2(x, y): ").split()))
p1 = Vector(inp[0], inp[1])
p2 = Vector(inp[2], inp[3])
view_ang1 = (p1 - face).angle_with_x_axis()
view_ang2 = (p2 - face).angle_with_x_axis()
attention_dir = (view_ang1 + view_ang2) / 2.0

num_objs = int(input('number of objects: '))

objs = []
scan_lines = []
print("enter lower-left point (x, y), width and height of the objs")
for i in range(num_objs):
    inp = list(map(float, input("{0}'th obj: ".format(i)).split()))
    x_i = inp[0]
    y_i = inp[1]
    width_i = inp[2]
    height_i = inp[3]
    objs.append(Obj(x_i, y_i, width_i, height_i, i))
    objs[i].append_scan_lines(scan_lines, face)

scan_lines.sort(key=cmp_scan_lines)

for i in range(2 * num_objs):
    if i > 0:
        nearest_idx = -1
        min_dist = 1e9
        for j in range(num_objs):
            if scan_lines[i].ang < objs[j].enter_ang + EPS or scan_lines[i - 1].ang + EPS > objs[j].leave_ang:
                continue

            face_distance = objs[j].face_dist(face)
            if min_dist > face_distance + EPS:
                min_dist = face_distance
                nearest_idx = j

        if nearest_idx == -1:
            continue

        o1 = scan_lines[i - 1].obj_idx
        o2 = scan_lines[i].obj_idx
        i1 = scan_lines[i - 1].pt_idx
        i2 = scan_lines[i].pt_idx
        p1 = objs[o1].pts[i1]
        p2 = objs[o2].pts[i2]
        objs[nearest_idx].visible_area += polygon_area(clip_obj(face, p1, p2, objs[nearest_idx].pts))

total_attention = 0.0
for i in range(num_objs):
    objs[i].attention = 1.0
    objs[i].attention /= objs[i].attention_dist(face,
                                                (face + Vector(math.cos(attention_dir), math.sin(attention_dir))))
    objs[i].attention /= objs[i].face_dist(face)
    objs[i].attention *= objs[i].visible_area / (objs[i].area())

    total_attention += objs[i].attention

for i in range(num_objs):
    objs[i].attention *= (100.0 / total_attention)

    print("percentage attention of {0}'th obj = {1}%".format(i, objs[i].attention))

########################
#     test case 01     #
########################
#      0 0             #
#      1 2 -1 2        #
#      5               #
#      -6 32 10 5      #
#      8 33 3 2        #
#      -10 40 5 3      #
#      5 37 5 3        #
#      1 45 16 5       #
########################
#     test case 02     #
########################
#      0 0             #
#      1 2 -1 2        #
#      6               #
#      -6 32 10 5      #
#      8 33 3 2        #
#      -10 40 5 3      #
#      5 37 5 3        #
#      1 45 16 5       #
#      -5 20 12 5      #
########################