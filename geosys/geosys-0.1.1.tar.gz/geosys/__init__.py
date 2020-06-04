import math


class WSG84:
    a = 6378137
    f = 0.0033528106647474805
    b = 6356752.314245179
    e = 0.08181919084262157

    # @property
    # def a(self):
    #     return 6378137
    #
    # @property
    # def f(self):
    #     # return 1 / 298.257223563
    #     return 0.0033528106647474805
    #
    # @property
    # def b(self):
    #     # return self.a - self.a * self.f
    #     return 6356752.314245179
    #
    # @property
    # def e(self):
    #     # return math.sqrt(1 - (self.b**2 / self.a**2))
    #     return 0.08181919084262157

    @classmethod
    def to_cartesian(cls, latitude, longitude, altitude=0):
        return to_cartesian(latitude, longitude, altitude, cls)


class Vertex:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None

    def __str__(self):
        return "[%s, %s, %s]" % (self.x, self.y, self.z)


def to_cartesian(latitude, longitude, altitude=0, model=WSG84()):
    # TODO: Invalid values
    vertex = Vertex()

    latitude_phi = math.radians(latitude)
    longitude_lambda = math.radians(longitude)

    n = ReferenceEllipsoid.radius(latitude_phi, model)

    vertex.x = (n + altitude) * math.cos(latitude_phi) * math.cos(longitude_lambda)
    vertex.y = (n + altitude) * math.cos(latitude_phi) * math.sin(longitude_lambda)
    vertex.z = ((1 - model.e ** 2) * n + altitude) * math.sin(latitude_phi)

    return vertex


class ReferenceEllipsoid:
    @staticmethod
    def radius(latitude_radians, model):
        return model.a / math.sqrt(1 - model.e ** 2 * math.sin(latitude_radians) ** 2)
