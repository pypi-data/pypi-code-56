#: STIX 2.x object types.
EXTERNAL_REFERENCE = "external-reference"
KILL_CHAIN_PHASE = "kill-chain-phase"
GRANULAR_MARKING = "granular-marking"
IDENTITY = "identity"
MARKING_DEFINITION = "marking-definition"
ATTACK_PATTERN = "attack-pattern"
INTRUSION_SET = "intrusion-set"
TOOL = "tool"
MALWARE = "malware"
COURSE_OF_ACTION = "course-of-action"
RELATIONSHIP = "relationship"

#: STIX 2.x field names.
ID = "id"
TYPE = "type"
NAME = "name"
ALIASES = "aliases"
SOURCE_REF = "source_ref"
TARGET_REF = "target_ref"
EXTERNAL_ID = "external_references.external_id"
RELATIONSHIP_TYPE = "relationship_type"

#: STIX 2.x pattern operators.
EQ = "="
IN = "in"

#: STIX 2.x relationship types.
USES = "uses"
MITIGATES = "mitigates"
RELATIONSHIP_TYPES = sorted([USES, MITIGATES])
