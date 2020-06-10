import os

#: Locations of different STIX 2.x TAXII feeds.
DEFAULT_MITRE_CTI_URL = "https://cti-taxii.mitre.org/stix/collections"

#: MITRE ATT&CK Enterprise matrix.
DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_URL = os.path.join(
    DEFAULT_MITRE_CTI_URL, "95ecc380-afe9-11e4-9b6c-751b66dd541e"
)

#: MITRE ATT&CK Mobile matrix.
DEFAULT_MITRE_ATTACK_MOBILE_STIX_DATA_URL = os.path.join(DEFAULT_MITRE_CTI_URL, "2f669986-b40b-4423-b720-4396ca6a462b")

#: MITRE ATT&CK Pre-ATT&CK matrix.
DEFAULT_MITRE_ATTACK_PRE_ATTACK_STIX_DATA_URL = os.path.join(
    DEFAULT_MITRE_CTI_URL, "062767bd-02d2-4b72-84ba-56caef0f8658",
)

#: Locations of different STIX 2.x offline collections.
DEFAULT_MITRE_CTI_DIRECTORY = os.path.join(os.path.dirname(__file__), "../../../resources/mitre/cti/matrices")

#: MITRE ATT&CK Enterprise matrix.
DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_PATH = os.path.join(
    DEFAULT_MITRE_CTI_DIRECTORY, 'enterprise-attack.json.gz'
)

#: MITRE ATT&CK Mobile matrix.
DEFAULT_MITRE_ATTACK_MOBILE_STIX_DATA_PATH = os.path.join(
    DEFAULT_MITRE_CTI_DIRECTORY, 'mobile-attack.json.gz'
)

#: MITRE ATT&CK Pre-ATT&CK matrix.
DEFAULT_MITRE_ATTACK_PRE_ATTACK_STIX_DATA_PATH = os.path.join(
    DEFAULT_MITRE_CTI_DIRECTORY, 'pre-attack.json.gz'
)

#: STIX 2.x data types.
MATRIX = "x-mitre-matrix"
TACTIC = "x-mitre-tactic"

#: STIX 2.x source names.
MITRE_CWE = "cwe"
MITRE_CAPEC = "capec"
MITRE_ATTACK_ENTERPRISE = "mitre-attack"
MITRE_ATTACK_MOBILE = "mitre-mobile-attack"
MITRE_ATTACK_PRE_ATTACK = "mitre-pre-attack"
NIST_MOBILE_THREAT_CATALOGUE = "NIST Mobile Threat Catalogue"
