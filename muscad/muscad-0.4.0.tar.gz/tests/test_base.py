import pytest

from muscad import (
    Volume,
    Square,
    Cube,
    Sphere,
    Text,
    E,
    Circle,
    Echo,
    Union,
    calc,
)


def test_cube():
    cube = Cube(50, 50, 50)
    cube -= Text("top", halign="center", valign="center").z_linear_extrude(
        1, top=cube.top + E
    )
    cube -= Text("bottom", halign="center", valign="center").z_linear_extrude(
        1, bottom=cube.bottom - E, downwards=True
    )
    cube -= Text("right", halign="center", valign="center").x_linear_extrude(
        1, right=cube.right + E
    )
    cube -= Text("left", halign="center", valign="center").x_linear_extrude(
        1, left=cube.left - E, leftwards=True
    )
    cube -= Text("front", halign="center", valign="center").y_linear_extrude(
        1, front=cube.front + E
    )
    cube -= Text("back", halign="center", valign="center").y_linear_extrude(
        1, back=cube.back - E, backwards=True
    )

    assert (
        str(cube)
        == """difference() {
  cube(size=[50, 50, 50], center=true);
  translate(v=[0, 0, 24.02]) 
  linear_extrude(height=1, center=false, convexity=10, twist=0.0, scale=1.0) 
  text(text="top", size=10, halign="center", valign="center");
  translate(v=[0, 0, -24.02]) 
  rotate(a=[180, 0, 0]) 
  linear_extrude(height=1, center=false, convexity=10, twist=0.0, scale=1.0) 
  text(text="bottom", size=10, halign="center", valign="center");
  translate(v=[24.02, 0, 0]) 
  rotate(a=[90, 0, 90]) 
  linear_extrude(height=1, center=false, convexity=10, twist=0.0, scale=1.0) 
  text(text="right", size=10, halign="center", valign="center");
  translate(v=[-24.02, 0, 0]) 
  rotate(a=[90, 0, 270]) 
  linear_extrude(height=1, center=false, convexity=10, twist=0.0, scale=1.0) 
  text(text="left", size=10, halign="center", valign="center");
  translate(v=[0, 24.02, 0]) 
  rotate(a=[270, 180, 0]) 
  linear_extrude(height=1, center=false, convexity=10, twist=0.0, scale=1.0) 
  text(text="front", size=10, halign="center", valign="center");
  translate(v=[0, -24.02, 0]) 
  rotate(a=[90, 0, 0]) 
  linear_extrude(height=1, center=false, convexity=10, twist=0.0, scale=1.0) 
  text(text="back", size=10, halign="center", valign="center");
}"""
    )


def test_volume():
    LEFT = -12
    RIGHT = 10
    BACK = -22
    FRONT = 20
    BOTTOM = -33
    TOP = 30

    ref = Volume(
        left=LEFT, right=RIGHT, back=BACK, front=FRONT, bottom=BOTTOM, top=TOP
    )

    assert ref.left == LEFT
    assert ref.right == RIGHT
    assert ref.back == BACK
    assert ref.front == FRONT
    assert ref.bottom == BOTTOM
    assert ref.top == TOP

    front_to_top = ref.front_to_top()
    assert front_to_top.left == -RIGHT
    assert front_to_top.right == -LEFT
    assert front_to_top.back == BOTTOM
    assert front_to_top.front == TOP
    assert front_to_top.bottom == BACK
    assert front_to_top.top == FRONT

    bottom_to_left = ref.bottom_to_left()
    assert bottom_to_left.left == BOTTOM
    assert bottom_to_left.right == TOP
    assert bottom_to_left.back == -RIGHT
    assert bottom_to_left.front == -LEFT
    assert bottom_to_left.bottom == -FRONT
    assert bottom_to_left.top == -BACK

    front_to_right = ref.front_to_right()
    assert front_to_right.left == BACK
    assert front_to_right.right == FRONT
    assert front_to_right.back == -RIGHT
    assert front_to_right.front == -LEFT
    assert front_to_right.bottom == BOTTOM
    assert front_to_right.top == TOP

    upside_down = ref.upside_down()
    assert upside_down.left == -RIGHT
    assert upside_down.right == -LEFT
    assert upside_down.back == BACK
    assert upside_down.front == FRONT
    assert upside_down.bottom == -TOP
    assert upside_down.top == -BOTTOM

    upside_down_x = ref.upside_down(True)
    assert upside_down_x.left == LEFT
    assert upside_down_x.right == RIGHT
    assert upside_down_x.back == -FRONT
    assert upside_down_x.front == -BACK
    assert upside_down_x.bottom == -TOP
    assert upside_down_x.top == -BOTTOM

    front_to_back = ref.front_to_back()
    assert front_to_back.left == -RIGHT
    assert front_to_back.right == -LEFT
    assert front_to_back.back == -FRONT
    assert front_to_back.front == -BACK
    assert front_to_back.bottom == BOTTOM
    assert front_to_back.top == TOP

    front_to_bottom = ref.front_to_bottom()
    assert front_to_bottom.left == -RIGHT
    assert front_to_bottom.right == -LEFT
    assert front_to_bottom.back == -TOP
    assert front_to_bottom.front == -BOTTOM
    assert front_to_bottom.bottom == -FRONT
    assert front_to_bottom.top == -BACK

    bottom_to_right = ref.bottom_to_right()
    assert bottom_to_right.left == -TOP
    assert bottom_to_right.right == -BOTTOM
    assert bottom_to_right.back == LEFT
    assert bottom_to_right.front == RIGHT
    assert bottom_to_right.bottom == -FRONT
    assert bottom_to_right.top == -BACK

    front_to_right = ref.front_to_right()
    assert front_to_right.left == BACK
    assert front_to_right.right == FRONT
    assert front_to_right.back == -RIGHT
    assert front_to_right.front == -LEFT
    assert front_to_right.bottom == BOTTOM
    assert front_to_right.top == TOP

    back_to_right = ref.back_to_right()
    assert back_to_right.left == -FRONT
    assert back_to_right.right == -BACK
    assert back_to_right.back == LEFT
    assert back_to_right.front == RIGHT
    assert back_to_right.bottom == BOTTOM
    assert back_to_right.top == TOP

    back_to_bottom = ref.back_to_bottom()
    assert back_to_bottom.left == LEFT
    assert back_to_bottom.right == RIGHT
    assert back_to_bottom.back == -TOP
    assert back_to_bottom.front == -BOTTOM
    assert back_to_bottom.bottom == BACK
    assert back_to_bottom.top == FRONT

    left_to_bottom = ref.left_to_bottom()
    assert left_to_bottom.left == -FRONT
    assert left_to_bottom.right == -BACK
    assert left_to_bottom.back == -TOP
    assert left_to_bottom.front == -BOTTOM
    assert left_to_bottom.bottom == LEFT
    assert left_to_bottom.top == RIGHT

    left_to_top = ref.left_to_top()
    assert left_to_top.left == -FRONT
    assert left_to_top.right == -BACK
    assert left_to_top.back == BOTTOM
    assert left_to_top.front == TOP
    assert left_to_top.bottom == -RIGHT
    assert left_to_top.top == -LEFT

    left_to_front = ref.left_to_front()
    assert left_to_front.left == BACK
    assert left_to_front.right == FRONT
    assert left_to_front.back == -RIGHT
    assert left_to_front.front == -LEFT
    assert left_to_front.bottom == BOTTOM
    assert left_to_front.top == TOP

    left_to_back = ref.left_to_back()
    assert left_to_back.left == -FRONT
    assert left_to_back.right == -BACK
    assert left_to_back.back == LEFT
    assert left_to_back.front == RIGHT
    assert left_to_back.bottom == BOTTOM
    assert left_to_back.top == TOP

    right_to_bottom = ref.right_to_bottom()
    assert right_to_bottom.left == BACK
    assert right_to_bottom.right == FRONT
    assert right_to_bottom.back == -TOP
    assert right_to_bottom.front == -BOTTOM
    assert right_to_bottom.bottom == -RIGHT
    assert right_to_bottom.top == -LEFT

    right_to_top = ref.right_to_top()
    assert right_to_top.left == -FRONT
    assert right_to_top.right == -BACK
    assert right_to_top.back == -TOP
    assert right_to_top.front == -BOTTOM
    assert right_to_top.bottom == LEFT
    assert right_to_top.top == RIGHT

    right_to_front = ref.right_to_front()
    assert right_to_front.left == -FRONT
    assert right_to_front.right == -BACK
    assert right_to_front.back == LEFT
    assert right_to_front.front == RIGHT
    assert right_to_front.bottom == BOTTOM
    assert right_to_front.top == TOP

    right_to_back = ref.right_to_back()
    assert right_to_back.left == BACK
    assert right_to_back.right == FRONT
    assert right_to_back.back == -RIGHT
    assert right_to_back.front == -LEFT
    assert right_to_back.bottom == BOTTOM
    assert right_to_back.top == TOP

    X = 26
    Y = 34
    Z = 45
    translated = ref.translate(x=X, y=Y, z=Z)
    assert translated.left == LEFT + X
    assert translated.right == RIGHT + X
    assert translated.back == BACK + Y
    assert translated.front == FRONT + Y
    assert translated.bottom == BOTTOM + Z
    assert translated.top == TOP + Z


def test_modifiers():
    ref = Square(1, 1)
    rendered = ref.render()
    assert ref.root().render() == f"!{rendered}"
    assert ref.disable().render() == f"*{rendered}"
    assert ref.debug().render() == f"#{rendered}"
    assert ref.background().render() == f"%{rendered}"
    assert ref.background().remove_modifier().render() == rendered


def test_sum():

    assert (
        str(sum(Cube(1, 1, x) for x in range(2)))
        == """union() {
  cube(size=[1, 1, 0], center=true);
  cube(size=[1, 1, 1], center=true);
}"""
    )


def test_resize():
    cube = (
        Cube(2, 4, 6)
        .align(center_x=10, center_y=20, center_z=-10)
        .resize(width=4, depth=2, height=12)
    )
    assert cube.width == 4
    assert cube.depth == 2
    assert cube.height == 12
    assert cube.left == 18
    assert cube.right == 22
    assert cube.back == 9
    assert cube.front == 11
    assert cube.bottom == -26
    assert cube.top == -14
    assert cube.center_x == 20
    assert cube.center_y == 10
    assert cube.center_z == -20

    assert (
        str(cube)
        == """resize(newsize=[4, 2, 12]) 
translate(v=[10.0, 20.0, -10.0]) 
cube(size=[2, 4, 6], center=true);"""
    )


def test_translate():
    sphere = Sphere(d=10, segments=8).up(5).rightward(4).backward(3)

    assert (
        str(sphere)
        == """translate(v=[4, -3, 5]) 
sphere(d=10, $fn=8);"""
    )


def test_rotational_extrusion():
    buoy = Circle(d=10).align(center_x=10).rotational_extrude()
    assert (
        str(buoy)
        == """rotate_extrude(angle=360, $fn=2826) 
translate(v=[10.0, 0, 0]) 
circle(d=10, $fn=78);"""
    )


def test_mirror():
    x_mirrored_circle = Circle(d=10).align(left=0).x_mirror()
    assert x_mirrored_circle.left == -10
    assert x_mirrored_circle.right == 0

    y_mirrored_circle = Circle(d=10).align(back=0).y_mirror()
    assert y_mirrored_circle.back == -10
    assert y_mirrored_circle.front == 0

    z_mirrored_circle = Sphere(d=10).align(bottom=0).z_mirror()
    assert z_mirrored_circle.bottom == -10
    assert z_mirrored_circle.top == 0
    assert z_mirrored_circle.left == -5
    assert z_mirrored_circle.right == 5

    x_mirrored_circle = Circle(d=10).align(left=0).x_mirror(keep=True)
    assert x_mirrored_circle.left == -10
    assert x_mirrored_circle.right == 10

    y_mirrored_circle = Circle(d=10).align(back=0).y_mirror(keep=True)
    assert y_mirrored_circle.back == -10
    assert y_mirrored_circle.front == 10

    z_mirrored_circle = Sphere(d=10).align(bottom=0).z_mirror(keep=True)
    assert z_mirrored_circle.bottom == -10
    assert z_mirrored_circle.top == 10


def test_hull():
    hulled_mirrored_circle = (
        Circle(d=10).align(left=0).x_mirror(keep=True).hull()
    )
    assert (
        str(hulled_mirrored_circle)
        == """hull() 
{
  mirror(v=[1, 0, 0]) 
  translate(v=[5.0, 0, 0]) 
  circle(d=10, $fn=78);
  translate(v=[5.0, 0, 0]) 
  circle(d=10, $fn=78);
}"""
    )

    assert (
        str(hulled_mirrored_circle.bounding_box())
        == """translate(v=[-10.0, -5.0, 0]) 
cube(size=[20.0, 10.0, 0], center=true);"""
    )


def test_echo():
    echo = Echo(foo="bar")
    assert str(echo) == 'echo(foo="bar");'


def test_inner_union():
    union = Union(Union(Union(Circle(d=4))))
    assert str(union) == "circle(d=4, $fn=31);"


def test_intersection():
    intersect = Cube(10, 8, 6) & Cube(6, 8, 10) & Cube(6, 10, 8)
    assert intersect.left == -3
    assert intersect.right == 3
    assert intersect.center_x == 0
    assert intersect.back == -4
    assert intersect.front == 4
    assert intersect.center_y == 0
    assert intersect.bottom == -3
    assert intersect.top == 3
    assert intersect.center_z == 0


def test_calc():
    from_, center, to, distance = calc(from_=0, center=5, to=10, distance=10)
    assert from_ == 0
    assert center == 5
    assert to == 10
    assert distance == 10

    from_, center, to, distance = calc(from_=0, center=5)
    assert from_ == 0
    assert center == 5
    assert to == 10
    assert distance == 10

    from_, center, to, distance = calc(from_=5, center=0)
    assert from_ == -5
    assert center == 0
    assert to == 5
    assert distance == 10

    from_, center, to, distance = calc(from_=5, distance=10)
    assert from_ == 5
    assert center == 10
    assert to == 15
    assert distance == 10

    from_, center, to, distance = calc(center=5, to=10)
    assert from_ == 0
    assert center == 5
    assert to == 10
    assert distance == 10

    from_, center, to, distance = calc(center=10, to=5)
    assert from_ == 5
    assert center == 10
    assert to == 15
    assert distance == 10

    from_, center, to, distance = calc(from_=10, distance=-10)
    assert from_ == 0
    assert center == 5
    assert to == 10
    assert distance == 10

    from_, center, to, distance = calc(from_=10, to=-10)
    assert from_ == -10
    assert center == 0
    assert to == 10
    assert distance == 20

    with pytest.raises(ValueError):
        calc(from_=5, center=0, to=-8)

    with pytest.raises(ValueError):
        calc(from_=0, center=4, to=10, distance=10)


def test_color():
    colored_cube = Cube(10, 10, 10).color("blue")
    assert (
        str(colored_cube)
        == """color("blue") 
cube(size=[10, 10, 10], center=true);"""
    )


def test_rotation():
    cube = Cube(10, 8, 6)

    assert cube.top_to_back()
