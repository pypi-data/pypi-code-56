import re
from enum import Enum

from pydantic.types import ConstrainedFloat, ConstrainedInt, ConstrainedStr


class base64Binary(ConstrainedStr):
    pass


class Binning(Enum):
    EIGHTBYEIGHT = "8x8"
    FOURBYFOUR = "4x4"
    ONEBYONE = "1x1"
    OTHER = "Other"
    TWOBYTWO = "2x2"


class Color(ConstrainedInt):
    pass


class FontFamily(Enum):
    CURSIVE = "cursive"
    FANTASY = "fantasy"
    MONOSPACE = "monospace"
    SANSSERIF = "sans-serif"
    SERIF = "serif"


class Hex40(ConstrainedStr):
    min_length = 20
    max_length = 20


class LSID(ConstrainedStr):
    regex = re.compile(r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:\S+:\S+)|(\S+:\S+)")


class Marker(Enum):
    ARROW = "Arrow"


class NamingConvention(Enum):
    LETTER = "letter"
    NUMBER = "number"


class NonNegativeFloat(ConstrainedFloat):
    ge = 0.0


class NonNegativeInt(ConstrainedInt):
    ge = 0


class NonNegativeLong(ConstrainedInt):
    ge = 0


class PercentFraction(ConstrainedFloat):
    le = 1.0
    ge = 0.0


class PixelType(Enum):
    BIT = "bit"
    COMPLEXDOUBLE = "double-complex"
    COMPLEXFLOAT = "complex"
    DOUBLE = "double"
    FLOAT = "float"
    INT16 = "int16"
    INT32 = "int32"
    INT8 = "int8"
    UINT16 = "uint16"
    UINT32 = "uint32"
    UINT8 = "uint8"


class PositiveFloat(ConstrainedFloat):
    gt = 0.0


class PositiveInt(ConstrainedInt):
    ge = 1


class UnitsAngle(Enum):
    DEGREE = "deg"
    GRADIAN = "gon"
    RADIAN = "rad"


class UnitsElectricPotential(Enum):
    ATTOVOLT = "aV"
    CENTIVOLT = "cV"
    DECAVOLT = "daV"
    DECIVOLT = "dV"
    EXAVOLT = "EV"
    FEMTOVOLT = "fV"
    GIGAVOLT = "GV"
    HECTOVOLT = "hV"
    KILOVOLT = "kV"
    MEGAVOLT = "MV"
    MICROVOLT = "µV"
    MILLIVOLT = "mV"
    NANOVOLT = "nV"
    PETAVOLT = "PV"
    PICOVOLT = "pV"
    TERAVOLT = "TV"
    VOLT = "V"
    YOCTOVOLT = "yV"
    YOTTAVOLT = "YV"
    ZEPTOVOLT = "zV"
    ZETTAVOLT = "ZV"


class UnitsFrequency(Enum):
    ATTOHERTZ = "aHz"
    CENTIHERTZ = "cHz"
    DECAHERTZ = "daHz"
    DECIHERTZ = "dHz"
    EXAHERTZ = "EHz"
    FEMTOHERTZ = "fHz"
    GIGAHERTZ = "GHz"
    HECTOHERTZ = "hHz"
    HERTZ = "Hz"
    KILOHERTZ = "kHz"
    MEGAHERTZ = "MHz"
    MICROHERTZ = "µHz"
    MILLIHERTZ = "mHz"
    NANOHERTZ = "nHz"
    PETAHERTZ = "PHz"
    PICOHERTZ = "pHz"
    TERAHERTZ = "THz"
    YOCTOHERTZ = "yHz"
    YOTTAHERTZ = "YHz"
    ZEPTOHERTZ = "zHz"
    ZETTAHERTZ = "ZHz"


class UnitsLength(Enum):
    ANGSTROM = "Å"
    ASTRONOMICALUNIT = "ua"
    ATTOMETER = "am"
    CENTIMETER = "cm"
    DECAMETER = "dam"
    DECIMETER = "dm"
    EXAMETER = "Em"
    FEMTOMETER = "fm"
    FOOT = "ft"
    GIGAMETER = "Gm"
    HECTOMETER = "hm"
    INCH = "in"
    KILOMETER = "km"
    LIGHTYEAR = "ly"
    LINE = "li"
    MEGAMETER = "Mm"
    METER = "m"
    MICROMETER = "µm"
    MILE = "mi"
    MILLIMETER = "mm"
    NANOMETER = "nm"
    PARSEC = "pc"
    PETAMETER = "Pm"
    PICOMETER = "pm"
    PIXEL = "pixel"
    POINT = "pt"
    REFERENCEFRAME = "reference frame"
    TERAMETER = "Tm"
    THOU = "thou"
    YARD = "yd"
    YOCTOMETER = "ym"
    YOTTAMETER = "Ym"
    ZEPTOMETER = "zm"
    ZETTAMETER = "Zm"


class UnitsPower(Enum):
    ATTOWATT = "aW"
    CENTIWATT = "cW"
    DECAWATT = "daW"
    DECIWATT = "dW"
    EXAWATT = "EW"
    FEMTOWATT = "fW"
    GIGAWATT = "GW"
    HECTOWATT = "hW"
    KILOWATT = "kW"
    MEGAWATT = "MW"
    MICROWATT = "µW"
    MILLIWATT = "mW"
    NANOWATT = "nW"
    PETAWATT = "PW"
    PICOWATT = "pW"
    TERAWATT = "TW"
    WATT = "W"
    YOCTOWATT = "yW"
    YOTTAWATT = "YW"
    ZEPTOWATT = "zW"
    ZETTAWATT = "ZW"


class UnitsPressure(Enum):
    ATMOSPHERE = "atm"
    ATTOPASCAL = "aPa"
    BAR = "bar"
    CENTIBAR = "cbar"
    CENTIPASCAL = "cPa"
    DECAPASCAL = "daPa"
    DECIBAR = "dbar"
    DECIPASCAL = "dPa"
    EXAPASCAL = "EPa"
    FEMTOPASCAL = "fPa"
    GIGAPASCAL = "GPa"
    HECTOPASCAL = "hPa"
    KILOBAR = "kbar"
    KILOPASCAL = "kPa"
    MEGABAR = "Mbar"
    MEGAPASCAL = "MPa"
    MICROPASCAL = "µPa"
    MILLIBAR = "mbar"
    MILLIPASCAL = "mPa"
    MILLITORR = "mTorr"
    MMHG = "mm Hg"
    NANOPASCAL = "nPa"
    PASCAL = "Pa"
    PETAPASCAL = "PPa"
    PICOPASCAL = "pPa"
    PSI = "psi"
    TERAPASCAL = "TPa"
    TORR = "Torr"
    YOCTOPASCAL = "yPa"
    YOTTAPASCAL = "YPa"
    ZEPTOPASCAL = "zPa"
    ZETTAPASCAL = "ZPa"


class UnitsTemperature(Enum):
    CELSIUS = "°C"
    FAHRENHEIT = "°F"
    KELVIN = "K"
    RANKINE = "°R"


class UnitsTime(Enum):
    ATTOSECOND = "as"
    CENTISECOND = "cs"
    DAY = "d"
    DECASECOND = "das"
    DECISECOND = "ds"
    EXASECOND = "Es"
    FEMTOSECOND = "fs"
    GIGASECOND = "Gs"
    HECTOSECOND = "hs"
    HOUR = "h"
    KILOSECOND = "ks"
    MEGASECOND = "Ms"
    MICROSECOND = "µs"
    MILLISECOND = "ms"
    MINUTE = "min"
    NANOSECOND = "ns"
    PETASECOND = "Ps"
    PICOSECOND = "ps"
    SECOND = "s"
    TERASECOND = "Ts"
    YOCTOSECOND = "ys"
    YOTTASECOND = "Ys"
    ZEPTOSECOND = "zs"
    ZETTASECOND = "Zs"


class UniversallyUniqueIdentifier(ConstrainedStr):
    regex = re.compile(
        r"(urn:uuid:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"
    )


class AnnotationID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Annotation:\S+)|(Annotation:\S+)"
    )


class ChannelID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Channel:\S+)|(Channel:\S+)"
    )


class DatasetID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Dataset:\S+)|(Dataset:\S+)"
    )


class DetectorID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Detector:\S+)|(Detector:\S+)"
    )


class DichroicID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Dichroic:\S+)|(Dichroic:\S+)"
    )


class ExperimenterGroupID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:ExperimenterGroup:\S+)|(ExperimenterGroup:\S+)"
    )


class ExperimenterID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Experimenter:\S+)|(Experimenter:\S+)"
    )


class ExperimentID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Experiment:\S+)|(Experiment:\S+)"
    )


class FilterID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Filter:\S+)|(Filter:\S+)"
    )


class FilterSetID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:FilterSet:\S+)|(FilterSet:\S+)"
    )


class FolderID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Folder:\S+)|(Folder:\S+)"
    )


class ImageID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Image:\S+)|(Image:\S+)"
    )


class InstrumentID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Instrument:\S+)|(Instrument:\S+)"
    )


class LightSourceID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:LightSource:\S+)|(LightSource:\S+)"
    )


class MicrobeamManipulationID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:MicrobeamManipulation:\S+)|(MicrobeamManipulation:\S+)"
    )


class ModuleID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Module:\S+)|(Module:\S+)"
    )


class ObjectiveID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Objective:\S+)|(Objective:\S+)"
    )


class PixelsID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Pixels:\S+)|(Pixels:\S+)"
    )


class PlateAcquisitionID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:PlateAcquisition:\S+)|(PlateAcquisition:\S+)"
    )


class PlateID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Plate:\S+)|(Plate:\S+)"
    )


class ProjectID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Project:\S+)|(Project:\S+)"
    )


class ReagentID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Reagent:\S+)|(Reagent:\S+)"
    )


class ROIID(LSID):
    regex = re.compile(r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:\S+)|(\S+)")


class ScreenID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Screen:\S+)|(Screen:\S+)"
    )


class ShapeID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Shape:\S+)|(Shape:\S+)"
    )


class WellID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:Well:\S+)|(Well:\S+)"
    )


class WellSampleID(LSID):
    regex = re.compile(
        r"(urn:lsid:([\w\-\.]+\.[\w\-\.]+)+:WellSample:\S+)|(WellSample:\S+)"
    )
