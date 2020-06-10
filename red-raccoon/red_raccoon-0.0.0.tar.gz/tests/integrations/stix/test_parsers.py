from typing import List
from dataclasses import dataclass, field

import red_raccoon.integrations.stix.parsers
import stix2
import stix2.utils
import unittest


@dataclass(frozen=True)
class ExternalReference:
    source_name: str
    url: str = None
    external_id: str = None
    description: str = None


@dataclass(eq=False, frozen=True)
class Malware:
    id: str
    type: str
    created: str
    created_by_ref: str
    modified: str
    name: str
    description: str = None
    object_marking_refs: List[str] = field(default_factory=list)
    external_references: List[ExternalReference] = field(default_factory=list)

    def __eq__(self, other):
        return isinstance(other, type(self)) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)


TRICKBOT = {
    "name": "TrickBot",
    "description": "[TrickBot](https://attack.mitre.org/software/S0266) is a Trojan spyware..",
    "id": "malware--00806466-754d-44ea-ad6f-0caf59cb8556",
    "external_references": [
        {
            "external_id": "S0266",
            "source_name": "mitre-enterprise",
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

SYN_ACK = {
            "name": "SynAck",
            "id": "malware--04227b24-7817-4de1-9050-b7b1b57f5866",
            "x_mitre_platforms": [
                "Windows"
            ],
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "x_mitre_aliases": [
                "SynAck"
            ],
            "type": "malware",
            "x_mitre_version": "1.1",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "labels": [
                "malware"
            ],
            "created": "2018-10-17T00:14:20.652Z",
            "modified": "2019-07-26T23:00:55.880Z",
            "external_references": [
                {
                    "external_id": "S0242",
                    "source_name": "mitre-enterprise",
                    "url": "https://attack.mitre.org/software/S0242"
                }
            ]
        }


class ParserTestCases(unittest.TestCase):
    def test_is_internal_id(self):
        self.assertTrue(red_raccoon.integrations.stix.parsers.is_internal_id(TRICKBOT['id']))
        self.assertFalse(red_raccoon.integrations.stix.parsers.is_internal_id(TRICKBOT['type']))

    def test_get_type_from_internal_id(self):
        expected = TRICKBOT['type']
        result = red_raccoon.integrations.stix.parsers.get_type_from_internal_id(TRICKBOT['id'])
        self.assertEqual(expected, result)

    def test_get_types_from_internal_ids(self):
        vectors = {
            'enterprise-pattern--00d0b012-8a03-410e-95de-5826bf542de6',
            'enterprise-pattern--01a5a209-b94c-450b-b7f9-946497d91055',
            'intrusion-set--06a11b7e-2a36-47fe-8d3e-82c265df3258',
        }
        expected = {'enterprise-pattern', 'intrusion-set'}
        result = set(red_raccoon.integrations.stix.parsers.get_types_from_internal_ids(vectors))
        self.assertEqual(expected, result)

    def test_get_names_from_objects(self):
        expected = {'TrickBot', 'SynAck'}
        result = red_raccoon.integrations.stix.parsers.get_names_from_objects([TRICKBOT, SYN_ACK])
        self.assertEqual(expected, result)

    def test_get_types_from_objects(self):
        expected = {'malware'}
        result = red_raccoon.integrations.stix.parsers.get_types_from_objects([TRICKBOT, SYN_ACK])
        self.assertEqual(expected, result)

    def test_get_internal_ids_from_objects(self):
        expected = {
            'malware--00806466-754d-44ea-ad6f-0caf59cb8556',
            'malware--04227b24-7817-4de1-9050-b7b1b57f5866',
        }
        result = red_raccoon.integrations.stix.parsers.get_internal_ids_from_objects([TRICKBOT, SYN_ACK])
        self.assertEqual(expected, result)

    def test_get_external_ids_from_objects(self):
        expected = {'S0242', 'S0266'}
        result = red_raccoon.integrations.stix.parsers.get_external_ids_from_objects([TRICKBOT, SYN_ACK])
        self.assertEqual(expected, result)

    def test_stix2_to_dataclass(self):
        obj = stix2.Malware(**stix2.utils.remove_custom_stix(TRICKBOT))

        result = red_raccoon.integrations.stix.parsers.stix2_to_dataclass(obj, data_class=Malware)
        self.assertIsInstance(result, Malware)

    def test_stix2_to_dataclass_with_dict(self):
        result = red_raccoon.integrations.stix.parsers.stix2_to_dataclass(TRICKBOT, data_class=Malware)
        self.assertIsInstance(result, Malware)

    def test_partition_set_of_object_ids(self):
        objects = [TRICKBOT, SYN_ACK]
        object_ids = set()
        object_ids |= set(red_raccoon.integrations.stix.parsers.get_internal_ids_from_objects(objects))
        object_ids |= set(red_raccoon.integrations.stix.parsers.get_external_ids_from_objects(objects))

        expected_external_ids = {
            'S0242',
            'S0266',
        }
        expected_internal_ids = {
            'malware--00806466-754d-44ea-ad6f-0caf59cb8556',
            'malware--04227b24-7817-4de1-9050-b7b1b57f5866',
        }
        internal_ids, external_ids = red_raccoon.integrations.stix.parsers.partition_set_of_object_ids(object_ids)
        self.assertEqual(expected_external_ids, external_ids)
        self.assertEqual(expected_internal_ids, internal_ids)
