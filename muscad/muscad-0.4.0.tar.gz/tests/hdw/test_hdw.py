from examples.hdw.extruder.bowden_extruder import (
    ExtruderStepperHolder,
    BowdenExtruder,
    ExtruderBracket,
)
from examples.hdw.extruder.spool_holder import SpoolHolder
from examples.hdw.misc.bed_bracket import BedBracket
from examples.hdw.misc.board_holder import BoardHolder
from examples.hdw.misc.cable_clip import CableClip
from examples.hdw.misc.extrusion_endcap import ExtrusionEndcap
from examples.hdw.misc.feet import Feet
from examples.hdw.misc.power_plug_holder import PowerPlugHolder
from examples.hdw.misc.power_supply_holder import PowerSupplyHolder
from examples.hdw.x_axis.x_carriage import (
    ExtruderClamp,
    XCarriage,
    XAxisPulleys,
)
from examples.hdw.y_axis.xy_idler import XYIdlerRight, XYIdlerLeft
from examples.hdw.y_axis.xy_stepper_mount import (
    XYStepperMountRight,
    XYStepperMountLeft,
)
from examples.hdw.y_axis.y_carriage import (
    YBeltFixBack,
    YBeltFixFront,
    YBeltFixLeft,
    YCarriageRight,
    YCarriageLeft,
    YClamp,
)
from examples.hdw.z_axis.z_bed_mount import ZBedMount
from examples.hdw.z_axis.z_bracket_down import (
    ZBracketDownRight,
    ZBracketDownLeft,
)
from examples.hdw.z_axis.z_bracket_up import ZBracketUpLeft, ZBracketUpRight
from examples.hdw.z_axis.z_stepper_mount import ZStepperMount
from tests.conftest import compare


def test_z_axis():
    compare(ZBedMount(), "../target_scad_files/z_bed_mount.scad")
    compare(
        ZBracketDownLeft(), "../target_scad_files/z_bracket_down_left.scad"
    )
    compare(
        ZBracketDownRight(), "../target_scad_files/z_bracket_down_right.scad"
    )
    compare(ZBracketUpLeft(), "../target_scad_files/z_bracket_up_left.scad")
    compare(ZBracketUpRight(), "../target_scad_files/z_bracket_up_right.scad")
    compare(ZStepperMount(), "../target_scad_files/z_stepper_mount.scad")


def test_y_axis():
    compare(XYIdlerRight(), "../target_scad_files/xy_idler_right.scad")
    compare(XYIdlerLeft(), "../target_scad_files/xy_idler_left.scad")
    compare(
        XYStepperMountRight(),
        "../target_scad_files/xy_stepper_mount_right.scad",
    )
    compare(
        XYStepperMountLeft(), "../target_scad_files/xy_stepper_mount_left.scad"
    )
    compare(YBeltFixBack(), "../target_scad_files/y_belt_fix_back.scad")
    compare(YBeltFixFront(), "../target_scad_files/y_belt_fix_front.scad")
    compare(YBeltFixLeft(), "../target_scad_files/y_belt_fix_left.scad")
    compare(YCarriageRight(), "../target_scad_files/y_carriage_right.scad")
    compare(YCarriageLeft(), "../target_scad_files/y_carriage_left.scad")
    compare(YClamp(), "../target_scad_files/y_clamp.scad")


def test_x_axis():
    compare(ExtruderClamp(), "../target_scad_files/extruder_clamp.scad")
    compare(XCarriage(), "../target_scad_files/x_carriage.scad")
    compare(XAxisPulleys(), "../target_scad_files/x_axis_pulleys.scad")


def test_misc():
    compare(BedBracket(), "../target_scad_files/bed_bracket.scad")
    compare(BoardHolder(), "../target_scad_files/board_holder.scad")
    compare(Feet(), "../target_scad_files/feet.scad")
    compare(PowerPlugHolder(), "../target_scad_files/power_plug_holder.scad")
    compare(
        PowerSupplyHolder(), "../target_scad_files/power_supply_holder.scad"
    )
    compare(CableClip(), "../target_scad_files/cable_clip.scad")
    compare(ExtrusionEndcap(), "../target_scad_files/extrusion_endcap.scad")


def test_extruder():
    compare(
        ExtruderStepperHolder(),
        "../target_scad_files/extruder_stepper_holder.scad",
    )
    compare(BowdenExtruder(), "../target_scad_files/bowden_extruder.scad")
    compare(ExtruderBracket(), "../target_scad_files/extruder_bracket.scad")
    compare(SpoolHolder(), "../target_scad_files/spool_holder.scad")
