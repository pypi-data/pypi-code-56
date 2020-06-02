from muscad import Part, Sphere, Surface, Circle, Cylinder, Volume
from muscad.vitamins.bolts import Bolt
from muscad.vitamins.brackets import CastBracket
from muscad.vitamins.extrusions import Extrusion


class Feet(Part):
    z_extrusion = ~Extrusion.e3030(60).background()
    y_extrusion = (
        ~Extrusion.e3030(60)
        .bottom_to_front()
        .align(
            center_x=z_extrusion.center_x,
            back=z_extrusion.front,
            bottom=z_extrusion.bottom,
        )
        .background()
    )
    x_extrusion = (
        ~Extrusion.e3030(60)
        .bottom_to_right()
        .align(
            left=z_extrusion.right,
            center_y=z_extrusion.center_y,
            bottom=z_extrusion.bottom,
        )
        .background()
    )

    cast_bracket = (
        ~CastBracket.bracket3030()
        .align(
            left=y_extrusion.right,
            back=x_extrusion.front,
            center_z=x_extrusion.center_z,
        )
        .background()
    )
    base = Surface.free(
        Circle(d=2).align(left=z_extrusion.left, back=z_extrusion.back),
        Circle(d=10).align(left=z_extrusion.left, front=cast_bracket.front),
        Circle(d=10).align(right=cast_bracket.right, back=z_extrusion.back),
        Circle(d=20).align(
            right=cast_bracket.right + 2, center_y=x_extrusion.front
        ),
        Circle(d=20).align(
            center_x=y_extrusion.right, front=cast_bracket.front + 2
        ),
    ).z_linear_extrude(6, top=z_extrusion.bottom)

    right_bolt = ~Bolt.M6(10).align(
        center_x=base.right - 10,
        center_y=x_extrusion.center_y,
        center_z=x_extrusion.bottom - 2,
    )

    front_bolt = ~Bolt.M6(10).align(
        center_x=y_extrusion.center_x,
        center_y=base.front - 10,
        center_z=y_extrusion.bottom - 2,
    )

    center_bolt = ~Bolt.M8(20).align(
        center_x=z_extrusion.center_x,
        center_y=z_extrusion.center_y,
        center_z=z_extrusion.bottom - 2,
    )

    FEET_DIAMETER = 44
    FILLET_RADIUS = 4

    def init(self, height=33):
        self.ball_holder = Cylinder(d=self.FEET_DIAMETER, h=height).align(
            left=self.z_extrusion.left,
            back=self.z_extrusion.back,
            bottom=self.base.bottom - height,
        )

        self.fillet = Surface.fillet(
            self.FILLET_RADIUS
        ).y_mirror().z_rotational_extrude(
            radius=self.FEET_DIAMETER / 2,
            center_x=self.ball_holder.center_x,
            center_y=self.ball_holder.center_y,
            top=self.base.bottom,
        ) & Volume(
            left=self.base.left,
            right=self.base.right,
            back=self.base.back,
            front=self.base.front,
            top=self.base.bottom,
            height=self.FILLET_RADIUS,
        )

        self.squash_ball = (
            ~Sphere(40)
            .align(
                center_x=self.ball_holder.center_x,
                center_y=self.ball_holder.center_y,
                center_z=self.ball_holder.bottom + 1,
            )
            .debug()
        )


if __name__ == "__main__":
    Feet().render_to_file(openscad=False)
