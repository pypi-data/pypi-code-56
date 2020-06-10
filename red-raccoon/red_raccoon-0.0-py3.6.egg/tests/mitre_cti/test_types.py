from red_raccoon.mitre_cti.types import ExternalReference, Tactic, EnterpriseTechnique, MobileTechnique, \
    PreAttackTechnique, Group, Malware, Tool, Mitigation, Relationship, MarkingDefinition, KillChainPhase, \
    StixDomainObject, Identity, Matrix

import red_raccoon.mitre_cti.parsers
import unittest
import copy


class ExternalReferenceTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_external_reference({
            "external_id": "G0008",
            "source_name": "mitre-attack",
            "url": "https://attack.mitre.org/groups/G0008"
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_external_reference({
            "description": "(Citation: Kaspersky Carbanak) (Citation: Fox-It Anunak Feb 2015)",
            "source_name": "Carbanak"
        })

    def setUp(self):
        self.assertIsInstance(self.a, ExternalReference)
        self.assertIsInstance(self.b, ExternalReference)

    def test_has_url(self):
        self.assertTrue(self.a.has_url())
        self.assertFalse(self.b.has_url())

    def test_has_external_id(self):
        self.assertTrue(self.a.has_external_id())
        self.assertFalse(self.b.has_external_id())

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class KillChainPhaseTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_kill_chain_phase({
            "kill_chain_name": "mitre-attack",
            "phase_name": "initial-access"
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_kill_chain_phase({
            "kill_chain_name": "mitre-attack",
            "phase_name": "execution"
        })

    def setUp(self):
        self.assertIsInstance(self.a, KillChainPhase)
        self.assertIsInstance(self.b, KillChainPhase)

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class StixDomainObjectTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_object({
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
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_object({
            "type": "identity",
            "name": "The MITRE Corporation",
            "identity_class": "organization",
            "created": "2017-06-01T00:00:00.000Z",
            "id": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "modified": "2017-06-01T00:00:00.000Z",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ]
        })

    def setUp(self):
        self.assertIsInstance(self.a, StixDomainObject)
        self.assertIsInstance(self.b, StixDomainObject)

    def test_is_revoked(self):
        self.assertFalse(self.a.is_revoked())
        self.assertFalse(self.b.is_revoked())

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class RelationshipTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_relationship({
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
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_relationship({
            "type": "relationship",
            "target_ref": "attack-pattern--6aac77c4-eaf2-4366-8c13-ce50ab951f38",
            "description": "[Cobalt Group](https://attack.mitre.org/groups/G0080) has sent spearphishing emails...",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2018-10-17T00:14:20.652Z",
            "id": "relationship--029bdc73-5054-45eb-b9d0-e4281f69d85a",
            "source_ref": "intrusion-set--dc6fe6ee-04c2-49be-ba3d-f38d2463c02a",
            "modified": "2019-07-26T23:38:33.783Z",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "external_references": [
                {
                    "source_name": "Group IB Cobalt Aug 2017",
                    "description": "Matveeva, V. (2017, August 15). Secrets of Cobalt. Retrieved October 10, 2018.",
                    "url": "https://www.group-ib.com/blog/cobalt"
                }
            ],
            "relationship_type": "uses"
        })

    def setUp(self):
        self.assertIsInstance(self.a, Relationship)
        self.assertIsInstance(self.b, Relationship)

    def test_is_revoked(self):
        self.assertFalse(self.a.is_revoked())
        self.assertFalse(self.b.is_revoked())

    def test_is_usage(self):
        self.assertTrue(self.a.is_usage())
        self.assertTrue(self.b.is_usage())

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class MarkingDefinitionTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_marking_definition({
            "type": "marking-definition",
            "definition": {
                "statement": "Copyright 2017, The MITRE Corporation"
            },
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2017-06-01T00:00:00Z",
            "id": "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168",
            "definition_type": "statement"
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_marking_definition({
            "type": "marking-definition",
            "id": "marking-definition--f88d31f6-486f-44da-b317-01333bde0b82",
            "created": "2017-01-20T00:00:00.000Z",
            "definition_type": "tlp",
            "definition": {
                "tlp": "white"
            }
        })
        cls.c = red_raccoon.mitre_cti.parsers.parse_marking_definition({
            "type": "marking-definition",
            "id": "marking-definition--f88d31f6-486f-44da-b317-01333bde0b82",
            "created": "2017-01-20T00:00:00.000Z",
            "definition_type": "tlp",
            "definition": {
                "tlp": "green"
            }
        })
        cls.d = red_raccoon.mitre_cti.parsers.parse_marking_definition({
            "type": "marking-definition",
            "id": "marking-definition--f88d31f6-486f-44da-b317-01333bde0b82",
            "created": "2017-01-20T00:00:00.000Z",
            "definition_type": "tlp",
            "definition": {
                "tlp": "amber"
            }
        })
        cls.e = red_raccoon.mitre_cti.parsers.parse_marking_definition({
            "type": "marking-definition",
            "id": "marking-definition--f88d31f6-486f-44da-b317-01333bde0b82",
            "created": "2017-01-20T00:00:00.000Z",
            "definition_type": "tlp",
            "definition": {
                "tlp": "red"
            }
        })

    def setUp(self):
        self.assertIsInstance(self.a, MarkingDefinition)
        self.assertIsInstance(self.b, MarkingDefinition)

    def test_is_revoked(self):
        self.assertFalse(self.a.is_revoked())
        self.assertFalse(self.b.is_revoked())

    def test_is_statement(self):
        for marking, expectation in (
                (self.a, True),
                (self.b, False),
                (self.c, False),
                (self.d, False),
                (self.e, False),
        ):
            self.assertEqual(marking.is_statement(), expectation)

    def test_is_tlp(self):
        for marking, expectation in (
                (self.a, False),
                (self.b, True),
                (self.c, True),
                (self.d, True),
                (self.e, True),
        ):
            self.assertEqual(marking.is_tlp(), expectation)

    def test_is_tlp_white(self):
        for tlp, expectation in (
                (self.b, True),
                (self.c, False),
                (self.d, False),
                (self.e, False),
        ):
            self.assertEqual(tlp.is_tlp_white(), expectation)

    def test_is_tlp_green(self):
        for tlp, expectation in (
                (self.b, False),
                (self.c, True),
                (self.d, False),
                (self.e, False),
        ):
            self.assertEqual(tlp.is_tlp_green(), expectation)

    def test_is_tlp_amber(self):
        for tlp, expectation in (
                (self.b, False),
                (self.c, False),
                (self.d, True),
                (self.e, False),
        ):
            self.assertEqual(tlp.is_tlp_amber(), expectation)

    def test_is_tlp_red(self):
        for tlp, expectation in (
                (self.b, False),
                (self.c, False),
                (self.d, False),
                (self.e, True),
        ):
            self.assertEqual(tlp.is_tlp_red(), expectation)

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class IdentityTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_identity({
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
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_identity({
            "type": "identity",
            "name": "The MITRE Corporation",
            "identity_class": "organization",
            "created": "2017-06-01T00:00:00.000Z",
            "id": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "modified": "2017-06-01T00:00:00.000Z",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ]
        })

    def setUp(self):
        self.assertIsInstance(self.a, Identity)
        self.assertIsInstance(self.b, Identity)

    def test_is_revoked(self):
        self.assertFalse(self.a.is_revoked())
        self.assertFalse(self.b.is_revoked())

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class MatrixTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_matrix({
            "type": "x-mitre-matrix",
            "name": "Enterprise ATT&CK",
            "description": "The full ATT&CK Matrix includes techniques spanning Windows, Mac, and Linux...",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2018-10-17T00:14:20.652Z",
            "id": "x-mitre-matrix--eafc1b4c-5e56-4965-bd4e-66a6a89c88cc",
            "modified": "2019-04-16T21:39:18.247Z",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "enterprise-attack",
                    "url": "https://attack.mitre.org/matrices/enterprise"
                }
            ],
            "tactic_refs": [
                "x-mitre-tactic--ffd5bcee-6e16-4dd2-8eca-7b3beedf33ca",
                "x-mitre-tactic--4ca45d45-df4d-4613-8980-bac22d278fa5",
                "x-mitre-tactic--5bc1d813-693e-4823-9961-abf9af4b0e92",
                "x-mitre-tactic--5e29b093-294e-49e9-a803-dab3d73b77dd",
                "x-mitre-tactic--78b23412-0651-46d7-a540-170a1ce8bd5a",
                "x-mitre-tactic--2558fd61-8c75-4730-94c4-11926db2a263",
                "x-mitre-tactic--c17c5845-175e-4421-9713-829d0573dbc9",
                "x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e",
                "x-mitre-tactic--d108ce10-2419-4cf9-a774-46161d6c6cfe",
                "x-mitre-tactic--f72804c5-f15a-449e-a5da-2eecd181f813",
                "x-mitre-tactic--9a4e74ab-5008-408c-84bf-a10dfbc53462",
                "x-mitre-tactic--5569339b-94c2-49ee-afb3-2222936582c8"
            ]
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_matrix({
            "type": "x-mitre-matrix",
            "name": "Device Access",
            "description": "The MITRE ATT&CK Matrix\u2122 provides a visual representation of the adversarial...",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2018-10-17T00:14:20.652Z",
            "id": "x-mitre-matrix--a382db5e-d009-4135-b893-0e0ff021c95b",
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
                "x-mitre-tactic--0a93fd8e-4a83-4c15-8203-db290e5f2ac6",
                "x-mitre-tactic--363bbeff-bb2a-4734-ac74-d6d37202fe54",
                "x-mitre-tactic--3e962de5-3280-43b7-bc10-334fbc1d6fa8",
                "x-mitre-tactic--987cda6d-eb77-406b-bf68-bcb5f3d2e1df",
                "x-mitre-tactic--6fcb36b8-3776-483b-8699-42215714fb10",
                "x-mitre-tactic--d418cdeb-1b9f-4a6b-a15d-2f89f549f8c1",
                "x-mitre-tactic--7be441c2-0095-4b1e-8125-fa8ffda29b0f",
                "x-mitre-tactic--6ebce653-294a-444a-bffb-14c04c8d137e",
                "x-mitre-tactic--7a0d25d3-f0c0-40bf-bf90-c743871b19ba",
                "x-mitre-tactic--10fa8d8d-1b04-4176-917e-738724239981",
                "x-mitre-tactic--3f660805-fa2e-42e8-8851-57f9e9b653e3"
            ]
        })

    def setUp(self):
        self.assertIsInstance(self.a, Matrix)
        self.assertIsInstance(self.b, Matrix)

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class TacticTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_tactic({
            "type": "x-mitre-tactic",
            "name": "Privilege Escalation",
            "description": "The adversary is trying to gain higher-level permissions.\n\nPrivilege Escalation...",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2018-10-17T00:14:20.652Z",
            "id": "x-mitre-tactic--5e29b093-294e-49e9-a803-dab3d73b77dd",
            "x_mitre_shortname": "privilege-escalation",
            "modified": "2019-07-19T17:43:00.594Z",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "TA0004",
                    "url": "https://attack.mitre.org/tactics/TA0004"
                }
            ]
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_tactic({
            "type": "x-mitre-tactic",
            "name": "Execution",
            "description": "The adversary is trying to run malicious code...",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2018-10-17T00:14:20.652Z",
            "id": "x-mitre-tactic--4ca45d45-df4d-4613-8980-bac22d278fa5",
            "x_mitre_shortname": "execution",
            "modified": "2019-07-19T17:42:06.909Z",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "TA0002",
                    "url": "https://attack.mitre.org/tactics/TA0002"
                }
            ]
        })

    def setUp(self):
        self.assertIsInstance(self.a, Tactic)
        self.assertIsInstance(self.b, Tactic)

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class EnterpriseTechniqueTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_technique({
            "x_mitre_data_sources": [
                "Process use of network",
                "Process monitoring",
                "Process command-line parameters",
                "Anti-virus",
                "Binary file metadata"
            ],
            "kill_chain_phases": [
                {
                    "kill_chain_name": "mitre-attack",
                    "phase_name": "defense-evasion"
                }
            ],
            "name": "Indicator Removal from Tools",
            "description": "If a malicious tool is detected and quarantined or otherwise curtailed, an adversary...",
            "id": "attack-pattern--00d0b012-8a03-410e-95de-5826bf542de6",
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
            "x_mitre_detection": "The first detection of a malicious tool may trigger an anti-virus or other...",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2017-05-31T21:30:54.176Z",
            "modified": "2018-10-17T00:14:20.652Z",
            "external_references": [
                {
                    "external_id": "T1066",
                    "source_name": "mitre-attack",
                    "url": "https://attack.mitre.org/techniques/T1066"
                }
            ],
            "x_mitre_defense_bypassed": [
                "Log analysis",
                "Host intrusion prevention systems",
                "Anti-virus"
            ]
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_technique({
            "x_mitre_data_sources": [
                "API monitoring",
                "Process monitoring",
                "File monitoring"
            ],
            "name": "Screen Capture",
            "description": "Adversaries may attempt to take screen captures of the desktop to gather information...",
            "id": "attack-pattern--0259baeb-9f63-4c69-bf10-eb038c390688",
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
            "x_mitre_detection": "Monitoring for screen capture behavior will depend on the method used to obtain...",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2017-05-31T21:31:25.060Z",
            "kill_chain_phases": [
                {
                    "kill_chain_name": "mitre-attack",
                    "phase_name": "collection"
                }
            ],
            "external_references": [
                {
                    "external_id": "T1113",
                    "source_name": "mitre-attack",
                    "url": "https://attack.mitre.org/techniques/T1113"
                },
                {
                    "source_name": "capec",
                    "external_id": "CAPEC-648",
                    "url": "https://capec.mitre.org/data/definitions/648.html"
                },
            ],
            "modified": "2019-06-18T13:58:28.377Z"
        })

    def setUp(self):
        self.assertIsInstance(self.a, EnterpriseTechnique)
        self.assertIsInstance(self.b, EnterpriseTechnique)

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class MobileTechniqueTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_technique({
            "x_mitre_old_attack_id": "MOB-T1077",
            "name": "Supply Chain Compromise",
            "description": "As further described in [Supply Chain Compromise](https://attack.mitre.org/techniq...",
            "id": "attack-pattern--0d95940f-9583-4e0f-824c-a42c1be47fad",
            "x_mitre_platforms": [
                "Android",
                "iOS"
            ],
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "x_mitre_version": "1.0",
            "type": "attack-pattern",
            "x_mitre_detection": "* Insecure third-party libraries could be detected by application vetting...",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2018-10-17T00:14:20.652Z",
            "x_mitre_tactic_type": [
                "Post-Adversary Device Access"
            ],
            "kill_chain_phases": [
                {
                    "kill_chain_name": "mitre-mobile-attack",
                    "phase_name": "initial-access"
                }
            ],
            "external_references": [
                {
                    "external_id": "T1474",
                    "source_name": "mitre-mobile-attack",
                    "url": "https://attack.mitre.org/techniques/T1474"
                },
                {
                    "external_id": "APP-6",
                    "source_name": "NIST Mobile Threat Catalogue",
                    "url": "https://pages.nist.gov/mobile-threat-catalogue/application-threats/APP-6.html"
                },
            ],
            "modified": "2018-10-17T00:14:20.652Z"
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_technique({
            "x_mitre_old_attack_id": "MOB-T1067",
            "name": "Jamming or Denial of Service",
            "description": "An attacker could jam radio signals (e.g. Wi-Fi, cellular, GPS) to prevent...",
            "id": "attack-pattern--d2e112dc-f6d4-488d-b8df-ecbfb57a0a2d",
            "x_mitre_platforms": [
                "Android",
                "iOS"
            ],
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "x_mitre_version": "1.1",
            "type": "attack-pattern",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2017-10-25T14:48:25.740Z",
            "x_mitre_tactic_type": [
                "Without Adversary Device Access"
            ],
            "kill_chain_phases": [
                {
                    "kill_chain_name": "mitre-mobile-attack",
                    "phase_name": "network-effects"
                }
            ],
            "external_references": [
                {
                    "external_id": "T1464",
                    "source_name": "mitre-mobile-attack",
                    "url": "https://attack.mitre.org/techniques/T1464"
                },
                {
                    "external_id": "CEL-7",
                    "source_name": "NIST Mobile Threat Catalogue",
                    "url": "https://pages.nist.gov/mobile-threat-catalogue/cellular-threats/CEL-7.html"
                }
            ],
            "modified": "2019-02-03T14:15:21.946Z"
        })

    def setUp(self):
        self.assertIsInstance(self.a, MobileTechnique)
        self.assertIsInstance(self.b, MobileTechnique)

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class PreAttackTechniqueTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_technique({
            "x_mitre_old_attack_id": "PRE-T1109",
            "x_mitre_detectable_by_common_defenses_explanation": "Defender will not know what certificates...",
            "name": "Acquire or compromise 3rd party signing certificates",
            "description": "Code signing is the process of digitally signing executables and scripts to confirm...",
            "kill_chain_phases": [
                {
                    "kill_chain_name": "mitre-pre-attack",
                    "phase_name": "establish-&-maintain-infrastructure"
                }
            ],
            "id": "attack-pattern--03f4a766-7a21-4b5e-9ccf-e0cf422ab983",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "x_mitre_version": "1.0",
            "x_mitre_difficulty_for_adversary": "No",
            "type": "attack-pattern",
            "x_mitre_difficulty_for_adversary_explanation": "It is trivial to purchase code signing certificates...",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2017-12-14T16:46:06.044Z",
            "modified": "2019-02-19T18:56:56.071Z",
            "external_references": [
                {
                    "external_id": "T1332",
                    "source_name": "mitre-pre-attack",
                    "url": "https://attack.mitre.org/techniques/T1332"
                },
            ],
            "x_mitre_detectable_by_common_defenses": "No"
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_technique({
            "x_mitre_old_attack_id": "PRE-T1163",
            "x_mitre_detectable_by_common_defenses_explanation": "Some environments have anti-spearphishing...",
            "name": "Authorized user performs requested cyber action",
            "description": "This technique has been deprecated. Please see ATT&CK's Initial Access and Execution...",
            "kill_chain_phases": [
                {
                    "kill_chain_name": "mitre-pre-attack",
                    "phase_name": "compromise"
                }
            ],
            "id": "attack-pattern--0440f60f-9056-4791-a740-8eae96eb61fa",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "x_mitre_version": "1.0",
            "x_mitre_deprecated": True,
            "type": "attack-pattern",
            "x_mitre_difficulty_for_adversary_explanation": "Users unwittingly click on spearphishing links...",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2017-12-14T16:46:06.044Z",
            "x_mitre_difficulty_for_adversary": "Yes",
            "x_mitre_detectable_by_common_defenses": "Yes",
            "external_references": [
                {
                    "external_id": "T1386",
                    "source_name": "mitre-pre-attack",
                    "url": "https://attack.mitre.org/techniques/T1386"
                },
            ],
            "modified": "2018-10-17T00:14:20.652Z"
        })

    def setUp(self):
        self.assertIsInstance(self.a, PreAttackTechnique)
        self.assertIsInstance(self.b, PreAttackTechnique)

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class MitigationTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_mitigation({
            "type": "course-of-action",
            "name": "Query Registry Mitigation",
            "description": "Identify unnecessary system utilities or potentially malicious software...",
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
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_mitigation({
            "type": "course-of-action",
            "name": "Login Item Mitigation",
            "description": "Restrict users from being able to create their own login items...",
            "external_references": [
                {
                    "external_id": "T1162",
                    "source_name": "mitre-attack",
                    "url": "https://attack.mitre.org/mitigations/T1162"
                },
            ],
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2018-10-17T00:14:20.652Z",
            "id": "course-of-action--06824aa2-94a5-474c-97f6-57c2e983d885",
            "modified": "2019-07-24T19:49:43.716Z",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "x_mitre_version": "1.0",
            "x_mitre_deprecated": True
        })

    def setUp(self):
        self.assertIsInstance(self.a, Mitigation)
        self.assertIsInstance(self.b, Mitigation)

    def test_is_revoked(self):
        self.assertFalse(self.a.is_revoked())
        self.assertFalse(self.b.is_revoked())

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class GroupTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_group({
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
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_group({
            "aliases": [
                "APT3",
                "Gothic Panda",
                "Pirpi",
                "UPS Team",
                "Buckeye",
                "Threat Group-0110",
                "TG-0110"
            ],
            "type": "intrusion-set",
            "name": "APT3",
            "description": "[APT3](https://attack.mitre.org/groups/G0022) is a China-based threat group...",
            "external_references": [
                {
                    "external_id": "G0022",
                    "source_name": "mitre-attack",
                    "url": "https://attack.mitre.org/groups/G0022"
                }
            ],
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "created": "2017-05-31T21:31:55.853Z",
            "id": "intrusion-set--0bbdf25b-30ff-4894-a1cd-49260d0dd2d9",
            "modified": "2019-10-11T19:27:52.526Z",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "x_mitre_version": "1.2"
        })

    def setUp(self):
        self.assertIsInstance(self.a, Group)
        self.assertIsInstance(self.b, Group)

    def test_is_revoked(self):
        self.assertFalse(self.a.is_revoked())
        self.assertFalse(self.b.is_revoked())

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class MalwareTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_malware({
            "name": "TrickBot",
            "description": "[TrickBot](https://attack.mitre.org/software/S0266) is a Trojan spyware program...",
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
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_malware({
            "name": "Machete",
            "description": "[Machete](https://attack.mitre.org/software/S0409) is a cyber espionage toolset...",
            "id": "malware--35cd1d01-1ede-44d2-b073-a264d727bc04",
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "external_id": "S0409",
                    "url": "https://attack.mitre.org/software/S0409"
                }
            ],
            "x_mitre_platforms": [
                "Windows"
            ],
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "x_mitre_version": "1.0",
            "type": "malware",
            "x_mitre_aliases": [
                "Machete"
            ],
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "x_mitre_contributors": [
                "Matias Nicolas Porolli, ESET"
            ],
            "created": "2019-09-13T13:17:25.718Z",
            "modified": "2019-10-15T21:19:27.277Z",
            "labels": [
                "malware"
            ]
        })

    def setUp(self):
        self.assertIsInstance(self.a, Malware)
        self.assertIsInstance(self.b, Malware)

    def test_is_revoked(self):
        self.assertFalse(self.a.is_revoked())
        self.assertFalse(self.b.is_revoked())

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)


class ToolTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.mitre_cti.parsers.parse_tool({
            "name": "PowerSploit",
            "description": "[PowerSploit](https://attack.mitre.org/software/S0194) is an open source, offensive...",
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
        })
        cls.b = red_raccoon.mitre_cti.parsers.parse_tool({
            "name": "SDelete",
            "description": "[SDelete](https://attack.mitre.org/software/S0195) is an application that securely...",
            "id": "tool--d8d19e33-94fd-4aa3-b94a-08ee801a2153",
            "x_mitre_platforms": [
                "Windows"
            ],
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "x_mitre_aliases": [
                "SDelete"
            ],
            "type": "tool",
            "x_mitre_version": "1.1",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "labels": [
                "tool"
            ],
            "created": "2018-04-18T17:59:24.739Z",
            "modified": "2019-04-24T00:37:08.653Z",
            "external_references": [
                {
                    "external_id": "S0195",
                    "source_name": "mitre-attack",
                    "url": "https://attack.mitre.org/software/S0195"
                }
            ]
        })

    def setUp(self):
        self.assertIsInstance(self.a, Tool)
        self.assertIsInstance(self.b, Tool)

    def test_is_revoked(self):
        self.assertFalse(self.a.is_revoked())
        self.assertFalse(self.b.is_revoked())

    def test__hash__(self):
        a = hash(self.a)
        b = hash(self.b)
        self.assertEqual(hash(a), hash(a))
        self.assertNotEqual(hash(a), hash(b))

    def test__eq__(self):
        a = self.a
        b = self.b
        self.assertEqual(copy.copy(a), a)
        self.assertIsNot(copy.copy(a), a)
        self.assertNotEqual(a, b)
