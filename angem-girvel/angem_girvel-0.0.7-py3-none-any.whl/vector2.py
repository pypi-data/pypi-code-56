from math import cos, sin, pi, asin, copysign, acos


class Vector2:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return iter((self.__x, self.__y))

    def __add__(self, other):
        return Vector2(
            self.__x + other.__x,
            self.__y + other.__y
        )

    def __neg__(self):
        return Vector2(
            -self.__x,
            -self.__y
        )

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return self.__x * other.__x + self.__y * other.__y

        return Vector2(
            self.__x * other,
            self.__y * other
        )

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * (1 / other)

    def squared_magnitude(self):
        return self.__x ** 2 + self.__y ** 2

    def __abs__(self):
        return self.squared_magnitude() ** 0.5

    def __eq__(self, other):
        return self.__x == other.__x and self.__y == other.__y

    def __pow__(self, power, modulo=None):
        if power == 0:
            return self / abs(self) if self != zero else zero
        if power % 2 == 0:
            return abs(self) ** power
        raise Exception

    def __invert__(self):
        return Vector2(self.__y, self.__x)

    def project(self, other):
        return self * other / other.squared_magnitude() * other

    def scalar_project(self, other):
        return self * other / abs(other)

    def rotated(self, angle):
        if not angle:
            return self

        cs = cos(angle)
        sn = sin(angle)

        return Vector2(
            self.__x * cs - self.__y * sn,
            self.__x * sn + self.__y * cs)

    def angle(self):
        return copysign(
            acos(self.__x / abs(self)),
            asin(self.__y / abs(self))
        )

    def __repr__(self):
        return f'{{{round(self.__x, 2)}; {round(self.__y, 2)}}}'

    def __bool__(self):
        return self != zero


zero = Vector2(0, 0)
one = Vector2(1, 1)

up    = Vector2(0, -1)
down  = Vector2(0, 1)
right = Vector2(1, 0)
left  = Vector2(-1, 0)
