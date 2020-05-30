from enum import Enum
from typing import Optional

from pydantic.dataclasses import dataclass

from .light_source import LightSource
from .pump import Pump
from .simple_types import (
    PositiveFloat,
    PositiveInt,
    UnitsFrequency,
    UnitsLength,
)


class Type(Enum):
    DYE = "Dye"
    EXCIMER = "Excimer"
    FREE_ELECTRON = "FreeElectron"
    GAS = "Gas"
    METAL_VAPOR = "MetalVapor"
    OTHER = "Other"
    SEMICONDUCTOR = "Semiconductor"
    SOLID_STATE = "SolidState"


class LaserMedium(Enum):
    AG = "Ag"
    ALEXANDRITE = "Alexandrite"
    AR = "Ar"
    AR_CL = "ArCl"
    AR_FL = "ArFl"
    CO = "CO"
    CO2 = "CO2"
    COUMARIN_C30 = "CoumarinC30"
    CU = "Cu"
    E_MINUS = "EMinus"
    ER_GLASS = "ErGlass"
    ER_YAG = "ErYAG"
    GA_AL_AS = "GaAlAs"
    GA_AS = "GaAs"
    H2_O = "H2O"
    H_FL = "HFl"
    HE_CD = "HeCd"
    HE_NE = "HeNe"
    HO_YAG = "HoYAG"
    HO_YLF = "HoYLF"
    KR = "Kr"
    KR_CL = "KrCl"
    KR_FL = "KrFl"
    N = "N"
    ND_GLASS = "NdGlass"
    ND_YAG = "NdYAG"
    OTHER = "Other"
    RHODAMINE6_G = "Rhodamine6G"
    RUBY = "Ruby"
    TI_SAPPHIRE = "TiSapphire"
    XE = "Xe"
    XE_BR = "XeBr"
    XE_CL = "XeCl"
    XE_FL = "XeFl"


class Pulse(Enum):
    CW = "CW"
    MODE_LOCKED = "ModeLocked"
    OTHER = "Other"
    Q_SWITCHED = "QSwitched"
    REPETITIVE = "Repetitive"
    SINGLE = "Single"


@dataclass
class Laser(LightSource):
    frequency_multiplication: Optional[PositiveInt] = None
    laser_medium: Optional[LaserMedium] = None
    pockel_cell: Optional[bool] = None
    pulse: Optional[Pulse] = None
    pump: Optional[Pump] = None
    repetition_rate: Optional[float] = None
    repetition_rate_unit: Optional[UnitsFrequency] = UnitsFrequency("Hz")
    tuneable: Optional[bool] = None
    type: Optional[Type] = None
    wavelength: Optional[PositiveFloat] = None
    wavelength_unit: Optional[UnitsLength] = UnitsLength("nm")
