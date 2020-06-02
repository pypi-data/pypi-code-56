from enum import IntEnum, unique


@unique
class MeasurementType(IntEnum):
    TEMPERATURE0 = 0  # vgms_l530_0
    EMISSION = 1      # vgms_l530_1
    TEMPERATURE2 = 2  # vgms_l530_2
    TEMPERATURE3 = 3  # vgms_l530_3
