import math
from asyncio.test_utils import force_legacy_ssl_support

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

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __eq__(self, other):
        return is_zero(self.x - other.x) and is_zero(self.y - other.y)

    def __ne__(self, other):
        return not(self == other)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __mul__(self, other):
        if type(other) in (int, float, long )
        return Vector(self.x * other, self.y * other)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def mu
# // scaller or dot
# product
# double
# operator * (const Vector & a)
# const
# {
# return (x * a.x + y * a.y);
# }
#
# // Vector or cross
# porduct
# double
# operator % (const Vector & a)
# const
# {
# return (x * a.y - y * a.x);
# }
#
# double
# squareDistance()
# {
# return ((*this) * (*this));
# }
#
# double
# value()
# {
# return sqrt((*this).squareDistance());
# }
#
# double
# angleWithXAxis()
# {
# double
# ang = atan2((*this).y, (*this).x);
# return ang + EPS < 0.0 ? ang + 2 * PI: ang;
# }


p1 = Pt(3, 5)
print(p1)
p2 = Pt()
print(p2)
# print(p1.__getattribute__(p1, p1.__slots__))
# print(p1.__str__)
# p1.print()
# p1.z = 8
# p2.print()

print(PI)
print(EPS)

print(is_equal(5.00000000000000, 4.9999999))

print('======================')
# Same as def funcvar(x): return x + 1
funcvar = lambda x: x + 1
print(funcvar(1))

# an_int and a_string are optional, they have default values
# if one is not passed (2 and "A default string", respectively).


def passing_example(a_list, an_int, a_string="A default string"):
    a_list.append("A new item")
    an_int = 4
    return a_list, an_int, a_string


my_list = [1, 2, 3]
my_int = 10
# my_list_cp = [my_list]
print(passing_example(my_list.copy(), my_int))

print(my_list)

print(my_int)
