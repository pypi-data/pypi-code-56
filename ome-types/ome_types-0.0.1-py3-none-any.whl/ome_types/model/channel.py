from dataclasses import field
from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .annotation_ref import AnnotationRef
from .detector_settings import DetectorSettings
from .filter_set_ref import FilterSetRef
from .light_path import LightPath
from .light_source_settings import LightSourceSettings
from .simple_types import (
    ChannelID,
    Color,
    PositiveFloat,
    PositiveInt,
    UnitsLength,
)


class AcquisitionMode(Enum):
    BRIGHT_FIELD = "BrightField"
    FLUORESCENCE_CORRELATION_SPECTROSCOPY = (
        "FluorescenceCorrelationSpectroscopy"
    )
    FLUORESCENCE_LIFETIME = "FluorescenceLifetime"
    FSM = "FSM"
    LASER_SCANNING_CONFOCAL_MICROSCOPY = "LaserScanningConfocalMicroscopy"
    LCM = "LCM"
    MULTI_PHOTON_MICROSCOPY = "MultiPhotonMicroscopy"
    NEAR_FIELD_SCANNING_OPTICAL_MICROSCOPY = (
        "NearFieldScanningOpticalMicroscopy"
    )
    OTHER = "Other"
    PALM = "PALM"
    SECOND_HARMONIC_GENERATION_IMAGING = "SecondHarmonicGenerationImaging"
    SINGLE_MOLECULE_IMAGING = "SingleMoleculeImaging"
    SLIT_SCAN_CONFOCAL = "SlitScanConfocal"
    SPECTRAL_IMAGING = "SpectralImaging"
    SPIM = "SPIM"
    SPINNING_DISK_CONFOCAL = "SpinningDiskConfocal"
    STED = "STED"
    STORM = "STORM"
    STRUCTURED_ILLUMINATION = "StructuredIllumination"
    SWEPT_FIELD_CONFOCAL = "SweptFieldConfocal"
    TIRF = "TIRF"
    TOTAL_INTERNAL_REFLECTION = "TotalInternalReflection"
    WIDE_FIELD = "WideField"


class ContrastMethod(Enum):
    BRIGHTFIELD = "Brightfield"
    DARKFIELD = "Darkfield"
    DIC = "DIC"
    FLUORESCENCE = "Fluorescence"
    HOFFMAN_MODULATION = "HoffmanModulation"
    OBLIQUE_ILLUMINATION = "ObliqueIllumination"
    OTHER = "Other"
    PHASE = "Phase"
    POLARIZED_LIGHT = "PolarizedLight"


class IlluminationType(Enum):
    EPIFLUORESCENCE = "Epifluorescence"
    NON_LINEAR = "NonLinear"
    OBLIQUE = "Oblique"
    OTHER = "Other"
    TRANSMITTED = "Transmitted"


@dataclass
class Channel:
    id: ChannelID
    acquisition_mode: Optional[AcquisitionMode] = None
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    color: Optional[Color] = -1
    contrast_method: Optional[ContrastMethod] = None
    detector_settings: Optional[DetectorSettings] = None
    emission_wavelength: Optional[PositiveFloat] = None
    emission_wavelength_unit: Optional[UnitsLength] = UnitsLength("nm")
    excitation_wavelength: Optional[PositiveFloat] = None
    excitation_wavelength_unit: Optional[UnitsLength] = UnitsLength("nm")
    filter_set_ref: Optional[FilterSetRef] = None
    fluor: Optional[str] = None
    illumination_type: Optional[IlluminationType] = None
    light_path: Optional[LightPath] = None
    light_source_settings: Optional[LightSourceSettings] = None
    name: Optional[str] = None
    nd_filter: Optional[float] = None
    pinhole_size: Optional[float] = None
    pinhole_size_unit: Optional[UnitsLength] = UnitsLength("µm")
    pockel_cell_setting: Optional[int] = None
    samples_per_pixel: Optional[PositiveInt] = None
