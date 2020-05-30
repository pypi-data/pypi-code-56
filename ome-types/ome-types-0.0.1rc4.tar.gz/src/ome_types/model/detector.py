from dataclasses import field
from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import DetectorID, UnitsElectricPotential


class Type(Enum):
    ANALOG_VIDEO = "AnalogVideo"
    APD = "APD"
    CCD = "CCD"
    CMOS = "CMOS"
    CORRELATION_SPECTROSCOPY = "CorrelationSpectroscopy"
    EBCCD = "EBCCD"
    EMCCD = "EMCCD"
    FTIR = "FTIR"
    INTENSIFIED_CCD = "IntensifiedCCD"
    LIFETIME_IMAGING = "LifetimeImaging"
    OTHER = "Other"
    PHOTODIODE = "Photodiode"
    PMT = "PMT"
    SPECTROSCOPY = "Spectroscopy"


_no_default = object()


@dataclass
class Detector(ManufacturerSpec):
    id: DetectorID = _no_default  # type: ignore
    amplification_gain: Optional[float] = None
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    gain: Optional[float] = None
    offset: Optional[float] = None
    type: Optional[Type] = None
    voltage: Optional[float] = None
    voltage_unit: Optional[UnitsElectricPotential] = UnitsElectricPotential(
        "V"
    )
    zoom: Optional[float] = None

    # hack for dataclass inheritance with non-default args
    # https://stackoverflow.com/a/53085935/
    def __post_init__(self):
        if self.id is _no_default:
            raise TypeError("__init__ missing 1 required argument: 'id'")
