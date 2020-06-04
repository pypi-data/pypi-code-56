from __future__ import annotations

import math
import cmath


def convert_angle(angle, unit: str):
    """Convert an angle to radians"""
    unit = unit.lower()
    if unit in {"d", "deg", "degrees", "degree", "°"}:
        return angle * math.tau / 360
    if unit in {"r", "", None, "rad", "radian", "radians"}:
        return angle
    if unit in {
        "g",
        "grad",
        "gradians",
        "gradian",
        "gons",
        "gon",
        "grades",
        "grade",
    }:
        return angle * math.tau / 400
    if unit in {"mins", "min", "minutes", "minute", "'", "′"}:
        return angle * math.tau / 21600
    if unit in {"secs", "sec", "seconds", "seconds", '"', "″"}:
        return angle * math.tau / 1296000
    if unit in {"turn", "turns"}:
        return angle * math.tau
    else:
        raise ValueError(f"Invalid angle unit: '{unit}'")


class Vector(complex):
    """A two dimensional vector"""

    def __new__(cls, x=None, y=None, r=None, theta=None, angle_unit="rad"):
        if theta is not None:
            theta = convert_angle(theta, angle_unit)
        if y is None and r is None and theta is None and x is not None:
            if isinstance(x, complex):
                return super().__new__(cls, x)
            if isinstance(x, str):
                raise TypeError("Cannot create Vector from string")
            try:
                iterable = iter(x)
                try:
                    x = next(iterable)
                    y = next(iterable)
                except StopIteration:
                    raise ValueError("Iterable is too short to create Vector")
                try:
                    next(iterable)
                    raise ValueError("Iterable is too long to create Vector")
                except StopIteration:
                    return super().__new__(cls, x, y)
            except TypeError:
                raise TypeError("Single argument Vector must be complex or iterable")
        if all((x is None, y is None, r is not None, theta is not None)):
            return super().__new__(cls, r * math.cos(theta), r * math.sin(theta))

        if all((r is None, theta is None, y is not None, x is not None)):
            return super().__new__(cls, x, y)
        raise ValueError("Invalid arguments to create Vector")

    def dot(self, other):
        """Return the dot product of self and other."""
        return self.x * other.x + self.y * other.y

    def perpdot(self, other):
        """
        Get the perpendicular dot product of self and other.

        This is the signed area of the parallelogram they define. It is
        also one of the 'cross products' that can be defined on 2d
        vectors.
        """
        return self.x * other.y - self.y * other.y

    def perp(self) -> Vector:
        """
        Get the vector, rotated anticlockwise by pi / 2.

        This is one of the 'cross products' that can be defined on 2d
        vectors.
        """
        return Vector(self.y, -self.x)

    def rotate(self, angle, unit="rad") -> Vector:
        """Return a self, rotated by angle anticlockwise."""
        angle = self.convert_angle(angle, unit)
        return Vector(r=self.r, theta=self.theta + angle)

    def rec(self) -> tuple:
        """Get the vector as (x, y)."""
        return (self.x, self.y)

    def pol(self) -> tuple:
        """Get the vector as (r, theta)."""
        return (self.r, self.theta)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x} {self.y})"

    def __len__(self):
        return 2

    def __length_hint__(self):
        return 2

    def __getitem__(self, key):
        if isinstance(key, int):
            if key in {0, -2}:
                return self.x
            if key in {1, -1}:
                return self.y
            raise IndexError("Vector index out of range")

        elif isinstance(key, slice):
            return self.rec()[key]

        else:
            raise TypeError("Vector indices must be integers or slices, not str")

    def __iter__(self):
        yield self.x
        yield self.y

    def __reversed__(self):
        yield self.y
        yield self.x

    def __round__(self, ndigits=0):
        return (round(self.x, ndigits), round(self.y, ndigits))

    @property
    def x(self):
        return self.real

    @property
    def y(self):
        return self.imag

    @property
    def r(self):
        return abs(self)

    @property
    def theta(self):
        return cmath.phase(self)
