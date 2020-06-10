#: The set of supported MITRE ATT&CK matrices.
MITRE_ATTACK_ENTERPRISE = "mitre-attack"
MITRE_ATTACK_MOBILE = "mitre-mobile"
SUPPORTED_LAYER_DOMAINS = [MITRE_ATTACK_ENTERPRISE, MITRE_ATTACK_MOBILE]

#: Example colors that can be used when creating MITRE ATT&CK Navigator layers.
BLUE = "#0074D9"
RED = "#FF4136"
YELLOW = "#FFDC00"
GREEN = "#2ECC40"
OLIVE = "#3D9970"
GRAY = "#AAAAAA"
AQUA = "#7FDBFF"
TEAL = "#39CCCC"
LIME = "#01FF70"
ORANGE = "#FF851B"
MAROON = "#85144b"
FUCHSIA = "#F012BE"
PURPLE = "#B10DC9"
SILVER = "#DDDDDD"
NAVY = "#001F3F"
WHITE = "#FFFFFF"
DEFAULT_COLOR = BLUE

#: Defaults to use when creating MITRE ATT&CK Navigator layers.
DEFAULT_LAYER_NAME = "layer"
DEFAULT_LAYER_DESCRIPTION = ""
DEFAULT_LAYER_DOMAIN = MITRE_ATTACK_ENTERPRISE
DEFAULT_LAYER_VERSION = "2.2"

#: Parameters related to the creation of heatmaps.
DEFAULT_MINIMUM_COLOR_FOR_GRADIENT = AQUA
DEFAULT_MAXIMUM_COLOR_FOR_GRADIENT = NAVY

#: Parameters related to the creation of diffs.
DEFAULT_COLOR_FOR_TECHNIQUES_ONLY_IN_FIRST_LAYER = OLIVE
DEFAULT_COLOR_FOR_TECHNIQUES_ONLY_IN_SECOND_LAYER = BLUE
DEFAULT_COLOR_FOR_TECHNIQUES_IN_BOTH_LAYERS = YELLOW

#: Parameters related to the translation of MITRE ATT&CK Evaluations into MITRE ATT&CK Navigator layers.
DEFAULT_COLOR_FOR_DETECTED_TECHNIQUES = GREEN
DEFAULT_COLOR_FOR_UNDETECTED_TECHNIQUES = ORANGE
DEFAULT_COLOR_FOR_UNTESTED_TECHNIQUES = GRAY

#: Everything but 'TA0001: Initial Access', and 'TA0040: Impact' are in-scope.
IN_SCOPE_MITRE_ATTACK_ENTERPRISE_TACTIC_IDS_FOR_MITRE_ATTACK_EVALUATIONS = [
    'TA0002',   #: Execution.
    'TA0003',   #: Persistence.
    'TA0004',   #: Privilege Escalation.
    'TA0005',   #: Defense Evasion.
    'TA0006',   #: Credential Access.
    'TA0007',   #: Discovery.
    'TA0008',   #: Lateral Movement.
    'TA0009',   #: Collection.
    'TA0010',   #: Exfiltration.
    'TA0011',   #: Command and Control.
]
