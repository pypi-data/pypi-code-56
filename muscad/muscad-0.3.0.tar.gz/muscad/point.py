from muscad.helpers import cos, sin, radians, atan2


class Vector:
    def __init__(self, **kwargs: float):
        self.kwargs = kwargs

    def __getattr__(self, item):
        return self.kwargs[item]

    def __str__(self):
        return str([round(i, 4) for i in self.kwargs.values()])


class Point2D(Vector):
    def __init__(self, x, y):
        super().__init__(x=x, y=y)

    def z_rotate(self, angle):
        return Point2D(
            cos(angle) * self.x + sin(angle) * self.y,
            cos(angle) * self.y - sin(angle) * self.x,
        )

    def x_mirror(self):
        return Point2D(-self.x, self.y)

    def y_mirror(self):
        return Point2D(self.x, -self.y)

    def opposite(self):
        return Point2D(-self.x, -self.y)

    def angle(self):
        return atan2(self.y, self.x)

    @classmethod
    def from_radius_and_angle(cls, radius, angle):
        return cls(radius * cos(angle), radius * sin(angle))

    @classmethod
    def involute(cls, radius, angle):
        return cls(
            radius * (cos(angle) + radians(angle) * sin(angle)),
            radius * (sin(angle) - radians(angle) * cos(angle)),
        )

    def to_3d(self, z=0):
        return Point3D(self.x, self.y, z)


class Point3D(Vector):
    def __init__(self, x, y, z):
        super().__init__(x=x, y=y, z=z)
