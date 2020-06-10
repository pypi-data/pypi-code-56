from typing import List
from dataclasses import dataclass, field

import red_raccoon.stix.parsers
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


MALWARE = {
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
}


class ParserTestCases(unittest.TestCase):
    def test_get_type_from_id(self):
        expected = MALWARE['type']
        result = red_raccoon.stix.parsers.get_type_from_id(MALWARE['id'])
        self.assertEqual(expected, result)

    def test_is_id(self):
        self.assertTrue(red_raccoon.stix.parsers.is_id(MALWARE['id']))
        self.assertFalse(red_raccoon.stix.parsers.is_id(MALWARE['type']))

    def test_stix2_to_dict_with_optional_defaults(self):
        obj = stix2.Malware(**stix2.utils.remove_custom_stix(MALWARE))
        obj = red_raccoon.stix.parsers.stix2_to_dict(obj, include_optional_defaults=True)
        self.assertIsInstance(obj, dict)

    def test_stix2_to_dataclass(self):
        obj = stix2.Malware(**stix2.utils.remove_custom_stix(MALWARE))

        result = red_raccoon.stix.parsers.stix2_to_dataclass(obj, data_class=Malware)
        self.assertIsInstance(result, Malware)

    def test_stix2_to_dataclass_with_dict(self):
        result = red_raccoon.stix.parsers.stix2_to_dataclass(MALWARE, data_class=Malware)
        self.assertIsInstance(result, Malware)
