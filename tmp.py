from calc import Vector

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
