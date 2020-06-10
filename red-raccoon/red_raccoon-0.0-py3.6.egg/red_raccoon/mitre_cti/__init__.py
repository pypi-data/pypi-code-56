import os

#: Locations of different STIX 2.x TAXII feeds.
DEFAULT_MITRE_CTI_URL = "https://cti-taxii.mitre.org/stix/collections"

#: MITRE ATT&CK Enterprise matrix.
DEFAULT_MITRE_ATTACK_ENTERPRISE_COLLECTION_ID = "95ecc380-afe9-11e4-9b6c-751b66dd541e"
DEFAULT_MITRE_ATTACK_ENTERPRISE_URL = os.path.join(
    DEFAULT_MITRE_CTI_URL, DEFAULT_MITRE_ATTACK_ENTERPRISE_COLLECTION_ID
)

#: MITRE ATT&CK Mobile matrix.
DEFAULT_MITRE_ATTACK_MOBILE_COLLECTION_ID = "2f669986-b40b-4423-b720-4396ca6a462b"
DEFAULT_MITRE_ATTACK_MOBILE_URL = os.path.join(
    DEFAULT_MITRE_CTI_URL, DEFAULT_MITRE_ATTACK_MOBILE_COLLECTION_ID
)

#: MITRE ATT&CK Pre-ATT&CK matrix.
DEFAULT_MITRE_ATTACK_PRE_ATTACK_COLLECTION_ID = "062767bd-02d2-4b72-84ba-56caef0f8658"
DEFAULT_MITRE_ATTACK_PRE_ATTACK_URL = os.path.join(
    DEFAULT_MITRE_CTI_URL, DEFAULT_MITRE_ATTACK_PRE_ATTACK_COLLECTION_ID,
)

#: Locations of different STIX 2.x offline collections.
DEFAULT_MITRE_CTI_DIRECTORY = os.getenv(
    'RED_RACCOON_MITRE_CTI_DIRECTORY', os.path.join(os.path.dirname(__file__), "../../../cti")
)

#: MITRE ATT&CK Enterprise matrix.
DEFAULT_MITRE_ATTACK_ENTERPRISE_PATH = os.path.join(
    DEFAULT_MITRE_CTI_DIRECTORY, 'enterprise-attack', 'enterprise-attack.json'
)

#: MITRE ATT&CK Mobile matrix.
DEFAULT_MITRE_ATTACK_MOBILE_PATH = os.path.join(
    DEFAULT_MITRE_CTI_DIRECTORY, 'mobile-attack', 'mobile-attack.json'
)

#: MITRE ATT&CK Pre-ATT&CK matrix.
DEFAULT_MITRE_ATTACK_PRE_ATTACK_PATH = os.path.join(
    DEFAULT_MITRE_CTI_DIRECTORY, 'pre-attack', 'pre-attack.json'
)

#: STIX 2.x data types.
MATRIX = "x-mitre-matrix"
TACTIC = "x-mitre-tactic"

#: STIX 2.x source names.
MITRE_CWE = "cwe"
MITRE_CAPEC = "mitre-capec"
MITRE_ATTACK_ENTERPRISE = "mitre-attack"
MITRE_ATTACK_MOBILE = "mitre-mobile-attack"
MITRE_ATTACK_PRE_ATTACK = "mitre-pre-attack"
NIST_MOBILE_THREAT_CATALOGUE = "NIST Mobile Threat Catalogue"

ALL_MITRE_CTI_COLLECTIONS = {
    MITRE_ATTACK_ENTERPRISE,
    MITRE_ATTACK_MOBILE,
    MITRE_ATTACK_PRE_ATTACK,
}
