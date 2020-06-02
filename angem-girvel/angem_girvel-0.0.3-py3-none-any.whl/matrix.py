from math import cos, sin, pi, asin, copysign, acos

from text_viewer import text_table


class Matrix:
    def __init__(self, *strings):
        assert not strings or all(len(s) == len(strings[0]) for s in strings)
        self.strings = list(list(s) for s in strings)

    @property
    def size(self):
        return (len(self.strings[0]), len(self.strings)) if self.strings else (0, 0)

    def clone(self):
        return Matrix(*self.strings)

    @staticmethod
    def filled(e, m, n):
        return Matrix(*((e, ) * m, ) * n)

    @staticmethod
    def generated(func, m, n):
        result = Matrix.zero(m, n)

        for y in range(m):
            for x in range(n):
                result[y, x] = func(y, x)

        return result

    @staticmethod
    def zero(m, n):
        return Matrix.filled(0, m, n)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            assert len(key) == 2
            return self.strings[key[0]][key[1]]
        if isinstance(key, Matrix):
            assert key.size == (2, 1)
            return self[key.strings[0][0], key.strings[0][1]]
        raise TypeError

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            assert len(key) == 2
            self.strings[key[0]][key[1]] = value
            return
        if isinstance(key, Matrix):
            assert key.size == (2, 1)
            self[key.strings[0][0], key.strings[0][1]] = value
            return
        raise TypeError

    def __iter__(self):
        return Matrix.Iterator(self)

    def __len__(self):
        s = self.size
        return s[0] * s[1]

    def enumerate(self):
        return Matrix.Iterator(self, True)

    #  Math:

    def __eq__(self, other):
        for y, x, e in other.enumerate():
            if self[y, x] != e:
                return False
        return True

    def __iadd__(self, other):
        for y, x, e in other.enumerate():
            self[y, x] += e
        return self

    def __isub__(self, other):
        for y, x, e in other.enumerate():
            self[y, x] -= e
        return self

    def __imul__(self, other):
        if isinstance(other, Matrix):
            assert self.size[1] == other.size[0]

            old_strings = self.strings
            self.strings = [[0] * other.size[1] for _ in range(self.size[0])]

            for y, x, _ in self.enumerate():
                for i in range(other.size[0]):
                    self[y, x] += old_strings[y][i] * other[i, x]
        else:
            for y, x, _ in self.enumerate():
                self[y, x] *= other
        return self

    def __itruediv__(self, other):
        for y, x, _ in self.enumerate():
            self[y, x] /= other
        return self

    # Dummy math:

    def __add__(self, other):
        result = self.clone()
        result += other
        return result

    def __sub__(self, other):
        result = self.clone()
        result -= other
        return result

    def __mul__(self, other):
        result = self.clone()
        result *= other
        return result

    def __truediv__(self, other):
        result = self.clone()
        result /= other
        return result

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        result = self.clone()
        result *= -1
        return result

    # Representation:

    def __str__(self):
        return '\n'.join(text_table(self.strings))

    def __repr__(self):
        return str(self)

#     def squared_magnitude(self):
#         return self.x ** 2 + self.y ** 2
#
#     def __abs__(self):
#         return self.squared_magnitude() ** 0.5
#
#     def __eq__(self, other):
#         return self.x == other.x and self.y == other.y
#
#     def __pow__(self, power, modulo=None):
#         if power == 0:
#             return self / abs(self) if self != zero else zero
#         if power % 2 == 0:
#             return abs(self) ** power
#         raise Exception
#
#     def __invert__(self):
#         return Vector(self.y, self.x)
#
#     def project(self, other):
#         return self * other / other.squared_magnitude() * other
#
#     def scalar_project(self, other):
#         return self * other / abs(other)
#
#     def rotated(self, angle):
#         if not angle:
#             return self
#
#         cs = cos(angle)
#         sn = sin(angle)
#
#         return Vector(
#             self.x * cs - self.y * sn,
#             self.x * sn + self.y * cs)
#
#     def angle(self):
#         return copysign(
#             acos(self.x / abs(self)),
#             asin(self.y / abs(self))
#         )
#
#     def __repr__(self):
#         return f'{{{round(self.x, 2)}; {round(self.y, 2)}}}'
#
#     def __bool__(self):
#         return self != zero
    class Iterator:
        def __init__(self, matrix, enumerated=False):
            self.enumerated = enumerated
            self.matrix = matrix
            self.m, self.n = self.matrix.size
            self.x = -1
            self.y = 0

        def __iter__(self):
            return self

        def __next__(self):
            self.x += 1

            if self.x >= self.m:
                self.x = 0
                self.y += 1

            if self.y >= self.n:
                raise StopIteration

            if self.enumerated:
                return self.y, self.x, self.matrix[self.y, self.x]
            return self.matrix[self.y, self.x]


# zero = Vector(0, 0)
# one = Vector(1, 1)
#
# up    = Vector( 0, -1)
# down  = Vector( 0,  1)
# right = Vector( 1,  0)
# left  = Vector(-1,  0)
