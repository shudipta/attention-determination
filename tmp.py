# from numpy.core import long

from calc import *
from types import *

class complex:
    def __init__(self, a, b):
        self.a = a
        self.b = b

        # adding two objects

    def __add__(self, other):
        return complex(self.a + other.a, self.b + other.b)

    def __str__(self):
        return '({0}, {1})'.format(self.a, self.b)


Ob1 = complex(1, 2)
Ob2 = complex(2, 3)
Ob3 = Ob1 + Ob2
print(Ob1, Ob2)
print(Ob3)
Ob4 = Ob1 + Ob3
print(Ob4)

print(Vector(0, 2) == Vector(1, 2))
print(Vector(1, 2) == Vector(1, 2))

print(Vector(0, 2) != Vector(1, 2))
print(Vector(1, 2) != Vector(1, 2))
print(Vector(0, 2) - Vector(1, 2))
print(Vector(2, 3) * 5)
print(Vector(0, 2) * Vector(1, 2))
print(Vector(0, 2) % Vector(1, 2))
print(Vector(1, 2).square_distance())
print(Vector(1, 2).value())
print(Vector(1, 1).angle_with_x_axis())

print("""scanline:
---------""")
print(Segment(Vector(0, 2), Vector(0, 3)).distance_from(Vector(5, 2)))


def test(a):
    b = 4
    if a < 5:
        b = a
    print(a, b)


for i in range(7): test(i)

# print([i for i in range(5)])
obj1 = Obj(1, 1, 2, 2, 0)
obj2 = Obj(5, 1, 2, 2, 1)
scan_lines = [ScanLine(0, 0, -1)]
print(str(scan_lines))
obj1.append_scan_lines(scan_lines, Vector(0, 0))
print(scan_lines)
obj2.append_scan_lines(scan_lines, Vector(0, 0))
print(scan_lines)
print(obj1.face_dist(Vector(0, 0)))
print(obj1.face_dist(Vector(5, 5)))

# m = list(map(float, input("(x, y): ").split()))
#
# print(Vector(m[0], m[1]))
#
# m = list(map(float, input("enter face view angles point p1(x, y), p2(x, y): ").split()))
# p1 = Vector(m[0], m[1])
# p2 = Vector(m[2], m[3])
# print(p1, p2)

# print(int(input('number of objects: ')))
# print(Vector(list(map(float, input("(x, y): ").split()))))


def cmp_scan_lines(line: ScanLine):
    return line.ang

l = []
l.append(ScanLine(0.5, 1, 0))
l.append(ScanLine(0.5, 0, 0))
l.append(ScanLine(0.4, 2, 0))
l.append(ScanLine(0.4, 3, 0))
l.append(ScanLine(0.3, 4, 0))

l.sort(key=cmp_scan_lines)
print(l)

print(type(11111111111111111111111111000000000000) is int)
