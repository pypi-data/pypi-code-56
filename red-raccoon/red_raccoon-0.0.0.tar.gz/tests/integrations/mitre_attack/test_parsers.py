from red_raccoon.integrations.mitre_attack import TACTIC, MATRIX
from red_raccoon.integrations.stix import IDENTITY, ATTACK_PATTERN, INTRUSION_SET, RELATIONSHIP, TOOL, MALWARE, \
    COURSE_OF_ACTION

from red_raccoon.integrations.mitre_attack.types import Relationship, Tactic, EnterpriseTechnique, MobileTechnique, \
    PreAttackTechnique, Mitigation, Malware, Tool, Group, Identity, Matrix

import red_raccoon.integrations.mitre_attack.parsers
import unittest


TEST_MARKING_DEFINITION = {
    "type": "marking-definition",
    "id": "marking-definition--f88d31f6-486f-44da-b317-01333bde0b82",
    "created": "2017-01-20T00:00:00.000Z",
    "definition_type": "tlp",
    "definition": {
        "tlp": "amber"
    }
}

TEST_EXTERNAL_REFERENCE = {
    "external_id": "G0008",
    "source_name": "mitre-attack",
    "url": "https://attack.mitre.org/groups/G0008"
}

TEST_KILL_CHAIN_PHASE = {
    "kill_chain_name": "mitre-attack",
    "phase_name": "execution"
}

TEST_IDENTITY = {
    "type": "identity",
    "id": "identity--b38dfe21-7477-40d1-aa90-5c8671ce51ca",
    "created": "2017-04-27T16:18:24.318Z",
    "modified": "2017-04-27T16:18:24.318Z",
    "name": "Gotham National Bank",
    "identity_class": "organization",
    "contact_information": "contact@gothamnational.com",
    "sectors": [
        "financial-services"
    ]
}

TEST_MATRIX = {
    "type": "x-mitre-matrix",
    "name": "Network-Based Effects",
    "description": "...",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2018-10-17T00:14:20.652Z",
    "id": "x-mitre-matrix--5104d5f0-16b7-4aec-8ae3-0a90cd5494fc",
    "modified": "2018-10-17T00:14:20.652Z",
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "external_references": [
        {
            "source_name": "mitre-attack",
            "external_id": "mobile-attack",
            "url": "https://attack.mitre.org/matrices/mobile"
        }
    ],
    "tactic_refs": [
        "x-mitre-tactic--9eb4c21e-4fa8-44c9-b167-dbfc455f9210",
        "x-mitre-tactic--e78d7d60-41b5-49b7-b0a9-5c5d4cbabe17"
    ]
}

TEST_TACTIC = {
    "type": "x-mitre-tactic",
    "name": "Privilege Escalation",
    "description": "...",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2018-10-17T00:14:20.652Z",
    "id": "x-mitre-tactic--3e962de5-3280-43b7-bc10-334fbc1d6fa8",
    "x_mitre_shortname": "privilege-escalation",
    "modified": "2018-10-17T00:14:20.652Z",
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "external_references": [
        {
            "source_name": "mitre-attack",
            "external_id": "TA0029",
            "url": "https://attack.mitre.org/tactics/TA0029"
        }
    ]
}

TEST_ENTERPRISE_TECHNIQUE = {
    "x_mitre_data_sources": [
        "Packet capture",
        "Netflow/Enclave netflow",
        "Process use of network",
        "Malware reverse engineering",
        "Process monitoring"
    ],
    "name": "Standard Application Layer Protocol",
    "description": "...",
    "id": "attack-pattern--355be19c-ffc9-46d5-8d50-d6a036c675b6",
    "x_mitre_platforms": [
        "Linux",
        "macOS",
        "Windows"
    ],
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_version": "1.0",
    "type": "attack-pattern",
    "x_mitre_detection": "Analyze network test_data for uncommon test_data flows...",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "x_mitre_network_requirements": True,
    "created": "2017-05-31T21:30:56.776Z",
    "kill_chain_phases": [
        {
            "kill_chain_name": "mitre-attack",
            "phase_name": "command-and-control"
        }
    ],
    "external_references": [
        {
            "external_id": "T1071",
            "source_name": "mitre-attack",
            "url": "https://attack.mitre.org/techniques/T1071"
        },
    ],
    "modified": "2019-06-21T15:16:29.198Z"
}

TEST_MOBILE_TECHNIQUE = {
    "x_mitre_old_attack_id": "MOB-T1027",
    "name": "Process Discovery",
    "description": "...",
    "id": "attack-pattern--1b51f5bc-b97a-498a-8dbd-bc6b1901bf19",
    "x_mitre_platforms": [
        "Android"
    ],
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_version": "1.0",
    "type": "attack-pattern",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2017-10-25T14:48:33.926Z",
    "x_mitre_tactic_type": [
        "Post-Adversary Device Access"
    ],
    "kill_chain_phases": [
        {
            "kill_chain_name": "mitre-mobile-attack",
            "phase_name": "discovery"
        }
    ],
    "external_references": [
        {
            "external_id": "T1424",
            "source_name": "mitre-mobile-attack",
            "url": "https://attack.mitre.org/techniques/T1424"
        },
    ],
    "modified": "2018-10-17T00:14:20.652Z"
}

TEST_PRE_ATTACK_TECHNIQUE = {
    "x_mitre_old_attack_id": "PRE-T1040",
    "x_mitre_detectable_by_common_defenses_explanation": "...",
    "name": "Identify security defensive capabilities",
    "description": "...",
    "kill_chain_phases": [
        {
            "kill_chain_name": "mitre-pre-attack",
            "phase_name": "technical-information-gathering"
        }
    ],
    "id": "attack-pattern--04e93ca1-8415-4a46-8549-73b7c84f8dc3",
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_version": "1.0",
    "x_mitre_difficulty_for_adversary": "No",
    "type": "attack-pattern",
    "x_mitre_difficulty_for_adversary_explanation": "...",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2017-12-14T16:46:06.044Z",
    "modified": "2018-10-17T00:14:20.652Z",
    "external_references": [
        {
            "external_id": "T1263",
            "source_name": "mitre-pre-attack",
            "url": "https://attack.mitre.org/techniques/T1263"
        },
    ],
    "x_mitre_detectable_by_common_defenses": "Yes"
}

TEST_GROUP = {
    "aliases": [
        "Soft Cell"
    ],
    "name": "Soft Cell",
    "id": "intrusion-set--06a11b7e-2a36-47fe-8d3e-82c265df3258",
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_version": "1.0",
    "type": "intrusion-set",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "x_mitre_contributors": [
        "Cybereason Nocturnus, @nocturnus"
    ],
    "created": "2019-07-18T20:47:50.050Z",
    "modified": "2019-07-22T15:49:28.637Z",
    "external_references": [
        {
            "source_name": "mitre-attack",
            "external_id": "G0093",
            "url": "https://attack.mitre.org/groups/G0093"
        }
    ]
}

TEST_MITIGATION = {
    "type": "course-of-action",
    "name": "Query Registry Mitigation",
    "description": "...",
    "external_references": [
        {
            "external_id": "T1012",
            "source_name": "mitre-attack",
            "url": "https://attack.mitre.org/mitigations/T1012"
        },
    ],
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2018-10-17T00:14:20.652Z",
    "id": "course-of-action--0640214c-95af-4c04-a574-2a1ba6dda00b",
    "modified": "2019-07-25T11:29:14.757Z",
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_version": "1.0",
    "x_mitre_deprecated": True
}

TEST_TOOL = {
    "name": "PowerSploit",
    "description": "...",
    "id": "tool--13cd9151-83b7-410d-9f98-25d0f0d1d80d",
    "x_mitre_platforms": [
        "Windows"
    ],
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_aliases": [
        "PowerSploit"
    ],
    "type": "tool",
    "x_mitre_version": "1.1",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "labels": [
        "tool"
    ],
    "created": "2018-04-18T17:59:24.739Z",
    "modified": "2019-04-24T23:43:07.902Z",
    "external_references": [
        {
            "external_id": "S0194",
            "source_name": "mitre-attack",
            "url": "https://attack.mitre.org/software/S0194"
        }
    ]
}

TEST_MALWARE = {
    "name": "TrickBot",
    "description": "...",
    "id": "malware--00806466-754d-44ea-ad6f-0caf59cb8556",
    "external_references": [
        {
            "external_id": "S0266",
            "source_name": "mitre-attack",
            "url": "https://attack.mitre.org/software/S0266"
        }
    ],
    "x_mitre_platforms": [
        "Windows"
    ],
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_aliases": [
        "TrickBot",
        "Totbrick",
        "TSPY_TRICKLOAD"
    ],
    "type": "malware",
    "x_mitre_version": "1.1",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "x_mitre_contributors": [
        "Omkar Gudhate",
        "FS-ISAC"
    ],
    "created": "2018-10-17T00:14:20.652Z",
    "modified": "2019-06-24T19:15:06.150Z",
    "labels": [
        "malware"
    ]
}

TEST_RELATIONSHIP = {
    "type": "relationship",
    "target_ref": "attack-pattern--970cdb5c-02fb-4c38-b17e-d6327cf3c810",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2018-10-17T00:14:20.652Z",
    "id": "relationship--0040312a-e85d-4066-8203-2e66f8aa5288",
    "source_ref": "malware--8ec6e3b4-b06d-4805-b6aa-af916acc2122",
    "modified": "2019-04-24T23:55:43.191Z",
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "relationship_type": "uses"
}


class ParserTestCases(unittest.TestCase):
    def assert_object_can_be_parsed(self, data, data_class, parser):
        obj = parser(data)
        self.assertIsInstance(obj, data_class)

    def test_parse_objects(self):
        test_vectors = [
            [IDENTITY, TEST_IDENTITY, Identity],
            [MATRIX, TEST_MATRIX, Matrix],
            [TACTIC, TEST_TACTIC, Tactic],
            [ATTACK_PATTERN, TEST_ENTERPRISE_TECHNIQUE, EnterpriseTechnique],
            [ATTACK_PATTERN, TEST_MOBILE_TECHNIQUE, MobileTechnique],
            [ATTACK_PATTERN, TEST_PRE_ATTACK_TECHNIQUE, PreAttackTechnique],
            [INTRUSION_SET, TEST_GROUP, Group],
            [MALWARE, TEST_MALWARE, Malware],
            [TOOL, TEST_TOOL, Tool],
            [COURSE_OF_ACTION, TEST_MITIGATION, Mitigation],
            [RELATIONSHIP, TEST_RELATIONSHIP, Relationship],
        ]
        for object_type, data, data_class in test_vectors:
            with self.subTest(object_type):
                self.assertIsInstance(data, dict)
                result = red_raccoon.integrations.mitre_attack.parsers.parse_object(data)
                self.assertIsInstance(result, data_class, "{} ({})".format(data['id'], data_class))
