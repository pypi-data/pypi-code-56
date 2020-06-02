from muscad import Cylinder, EE


class Shape:
    @classmethod
    def pipe(
        cls, height, outer_diameter, inner_diameter,
    ):
        return Cylinder(d=outer_diameter, h=height) - Cylinder(
            d=inner_diameter, h=height + EE
        )

    @classmethod
    def cone(cls, height, diameter):
        return Cylinder(d=diameter, d2=0, h=height)

    @classmethod
    def oval_prism(cls, height, x_diameter, y_diameter):
        return Cylinder(h=height, d=y_diameter).scale(
            y=x_diameter / y_diameter
        )

    @classmethod
    def oval_tube(cls, height, x_diameter, y_diameter, wall):
        return Cylinder(h=height, d=x_diameter).scale(
            y=y_diameter / x_diameter
        ) - Cylinder(h=height + EE, d=x_diameter).scale(
            x=(x_diameter - wall * 2) / x_diameter,
            y=(y_diameter - wall * 2) / x_diameter,
        )
