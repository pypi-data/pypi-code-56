from Mensuration.Parameters import Parameters, uninitialized_params_check
from Mensuration.Error_Handler import *


class Volume(Parameters):

    def __init__(self, radius=None, length=None, base=None, height=None, width=None):
        # Initializing the Area_parameters
        Parameters.__init__(self, radius, length, None, height, width)

    def Cube(self):  # edge_length^3
        edge_length = self.length
        return edge_length ** 3

    def Sphere(self):  # (4/3) * π * radius^3
        return 4 / 3 * self.pi * self.radius ** 3

    def Cylinder(self):  # π * radius^2 * height
        return self.pi * self.radius ** 2 * self.height

    def Cone(self):  # (1/3) * π * radius^2 * height
        return 1 / 3 * self.pi * self.radius ** 2 * self.height

    def Cuboid(self):  # height * length * width
        return self.height * self.length * self.width

    def Ellipsoid(self, radius1, radius2, radius3):  # (4/3) * π * radius1 * radius2 * radius3
        expected_type = [[int, float], [int, float], [int, float]]
        result, user_type = uninitialized_params_check(expected_type, [radius1, radius2, radius3])

        if result:
            return 4 / 3 * self.pi * radius1 * radius2 * radius3
        else:
            raise ExpectedTypeError(user_type, "[<class 'int'>] or [<class 'float'>]")

    def Pyramid(self, base_area):  # (1/3) * base_area * height
        expected_type = [[int, float]]
        result, user_type = uninitialized_params_check(expected_type, [base_area])

        if result:
            return 1 / 3 * base_area * self.height
        else:
            raise ExpectedTypeError(user_type, "[<class 'int'>] or [<class 'float'>]")

    def Torus(self, minor_radius, major_radius):  # π^2	* (1/4) * (R + r) * (R - r)^2
        expected_type = [[int, float], [int, float]]
        result, user_type = uninitialized_params_check(expected_type, [minor_radius, major_radius])

        if result:
            return self.pi ** 2 * 1 / 4 * (minor_radius + major_radius) * (major_radius - minor_radius) ** 2
        else:
            raise ExpectedTypeError(user_type, "[<class 'int' or 'float'>] and [<class 'int' or 'float'>]")
