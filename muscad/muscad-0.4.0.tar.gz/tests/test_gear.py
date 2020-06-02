from muscad.vitamins.gears import (
    BevelGear,
    Gear,
)
from tests.conftest import compare


def test_bevel_gear():
    gear = Gear(
        circular_pitch=700,
        gear_thickness=12,
        rim_thickness=15,
        hub_thickness=17,
        nb_holes=8,
    )
    compare(gear, "gear.scad")
    bevel_gears_pair = BevelGear.pair()
    compare(bevel_gears_pair, "bevel_gears_pair.scad")
