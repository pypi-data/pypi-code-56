from red_raccoon.integrations.stix import COURSE_OF_ACTION, ATTACK_PATTERN, RELATIONSHIP, MALWARE, MITIGATES

import red_raccoon.integrations.stix.filters
import red_raccoon.integrations.stix.parsers
import red_raccoon.integrations.stix.api
import unittest

COURSE_OF_ACTION_A = {
    "type": "course-of-action",
    "id": "course-of-action--2a4f6c11-a4a7-4cb9-b0ef-6ae1bb3a718a",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2019-06-06T16:50:04.963Z",
    "modified": "2019-06-06T16:50:04.963Z",
    "name": "User Training",
    "description": "Train users to to be aware of access or manipulation attempts by an...",
    "external_references": [
        {
            "source_name": "mitre-attack",
            "url": "https://attack.mitre.org/mitigations/M1017",
            "external_id": "M1017"
        }
    ],
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_version": "1.0"
}

COURSE_OF_ACTION_B = {
    "type": "course-of-action",
    "id": "course-of-action--b5dbb4c5-b0b1-40b1-80b6-e9e84ab90067",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2019-07-19T14:40:23.529Z",
    "modified": "2019-07-19T14:57:15.656Z",
    "name": "Software Configuration",
    "description": "Implement configuration changes to software...",
    "external_references": [
        {
            "source_name": "mitre-attack",
            "url": "https://attack.mitre.org/mitigations/M1054",
            "external_id": "M1054"
        }
    ],
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_version": "1.0"
}

COURSE_OF_ACTION_C = {
    "type": "course-of-action",
    "id": "course-of-action--b045d015-6bed-4490-bd38-56b41ece59a0",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2019-06-10T20:53:36.319Z",
    "modified": "2019-06-10T20:53:36.319Z",
    "name": "Multi-factor Authentication",
    "description": "Use two or more pieces of evidence to authenticate to a system; such as...",
    "external_references": [
        {
            "source_name": "mitre-attack",
            "url": "https://attack.mitre.org/mitigations/M1032",
            "external_id": "M1032"
        }
    ],
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_version": "1.0"
}

ATTACK_PATTERN_A = {
    "type": "attack-pattern",
    "id": "attack-pattern--10ffac09-e42d-4f56-ab20-db94c67d76ff",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2019-10-08T20:04:35.508Z",
    "modified": "2019-10-22T19:59:20.282Z",
    "name": "Steal Web Session Cookie",
    "description": "An adversary may steal web application or service session cookies...",
    "kill_chain_phases": [
        {
            "kill_chain_name": "mitre-attack",
            "phase_name": "credential-access"
        }
    ],
    "external_references": [
        {
            "source_name": "mitre-attack",
            "url": "https://attack.mitre.org/techniques/T1539",
            "external_id": "T1539"
        }
    ],
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_contributors": [
        "Microsoft Threat Intelligence Center (MSTIC)",
        "Johann Rehberger"
    ],
    "x_mitre_data_sources": [
        "File monitoring",
        "API monitoring"
    ],
    "x_mitre_detection": "Monitor for attempts to access files and repositories on a local...",
    "x_mitre_permissions_required": [
        "User"
    ],
    "x_mitre_platforms": [
        "Linux",
        "macOS",
        "Windows",
        "Office 365",
        "SaaS"
    ],
    "x_mitre_version": "1.0"
}

INTRUSION_SET_A = {
    "aliases": [
        "Elderwood",
        "Elderwood Gang",
        "Beijing Group",
        "Sneaky Panda"
    ],
    "name": "Elderwood",
    "description": "[Elderwood](https://attack.mitre.org/groups/G0066) is a suspected Chinese...",
    "id": "intrusion-set--03506554-5f37-4f8f-9ce4-0e9f01a1b484",
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_version": "1.0",
    "type": "intrusion-set",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "x_mitre_contributors": [
        "Valerii Marchuk, Cybersecurity Help s.r.o."
    ],
    "created": "2018-04-18T17:59:24.739Z",
    "modified": "2019-03-22T20:15:19.117Z",
    "external_references": [
        {
            "external_id": "G0066",
            "source_name": "mitre-attack",
            "url": "https://attack.mitre.org/groups/G0066"
        }
    ]
}

MALWARE_A = {
    "name": "Olympic Destroyer",
    "description": "[Olympic Destroyer](https://attack.mitre.org/software/S0365) is malware...",
    "id": "malware--3249e92a-870b-426d-8790-ba311c1abfb4",
    "x_mitre_platforms": [
        "Windows"
    ],
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "x_mitre_aliases": [
        "Olympic Destroyer"
    ],
    "type": "malware",
    "x_mitre_version": "1.1",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "labels": [
        "malware"
    ],
    "created": "2019-03-25T14:07:22.547Z",
    "modified": "2019-10-04T21:49:25.695Z",
    "external_references": [
        {
            "source_name": "mitre-attack",
            "external_id": "S0365",
            "url": "https://attack.mitre.org/software/S0365"
        }
    ]
}

RELATIONSHIP_A = {
    "type": "relationship",
    "id": "relationship--f780f9d8-1baa-41b7-b7a1-acba717df0ab",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2019-10-14T16:25:38.695Z",
    "modified": "2019-10-22T19:59:20.675Z",
    "relationship_type": "mitigates",
    "description": "Train users to identify aspects of phishing attempts where they're asked to...",
    "source_ref": "course-of-action--2a4f6c11-a4a7-4cb9-b0ef-6ae1bb3a718a",
    "target_ref": "attack-pattern--10ffac09-e42d-4f56-ab20-db94c67d76ff",
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ]
}

RELATIONSHIP_B = {
    "type": "relationship",
    "id": "relationship--248a0d72-d9cd-43d3-985f-a33a49a79e8b",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2019-10-14T16:25:38.693Z",
    "modified": "2019-10-22T19:59:20.658Z",
    "relationship_type": "mitigates",
    "description": "Configure browsers or tasks to regularly delete persistent cookies.",
    "source_ref": "course-of-action--b5dbb4c5-b0b1-40b1-80b6-e9e84ab90067",
    "target_ref": "attack-pattern--10ffac09-e42d-4f56-ab20-db94c67d76ff",
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ]
}

RELATIONSHIP_C = {
    "type": "relationship",
    "id": "relationship--7a1cf82e-68e5-49ca-89ae-e492cd85dab4",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2019-10-14T16:25:38.680Z",
    "modified": "2019-10-22T19:59:20.647Z",
    "relationship_type": "mitigates",
    "description": "A physical second factor key that uses the target login domain as part of...",
    "source_ref": "course-of-action--b045d015-6bed-4490-bd38-56b41ece59a0",
    "target_ref": "attack-pattern--10ffac09-e42d-4f56-ab20-db94c67d76ff",
    "external_references": [
        {
            "source_name": "Evilginx 2 July 2018",
            "description": "Gretzky, K.. (2018, July 26). Evilginx 2 - Next Generation of...",
            "url": "https://breakdev.org/evilginx-2-next-generation-of-phishing-2fa-tokens/"
        }
    ],
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ]
}

RELATIONSHIP_D = {
    "type": "relationship",
    "target_ref": "attack-pattern--707399d6-ab3e-4963-9315-d9d3818cd6a0",
    "description": "[Olympic Destroyer](https://attack.mitre.org/software/S0365) uses API calls...",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "created": "2019-03-25T15:05:23.669Z",
    "id": "relationship--039364a9-2afd-4ae5-9df0-08d4e583674f",
    "source_ref": "malware--3249e92a-870b-426d-8790-ba311c1abfb4",
    "modified": "2019-06-30T23:07:54.016Z",
    "object_marking_refs": [
        "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
    ],
    "external_references": [
        {
            "source_name": "Talos Olympic Destroyer 2018",
            "description": "Mercer, W. and Rascagneres, P. (2018, February 12)...",
            "url": "https://blog.talosintelligence.com/2018/02/olympic-destroyer.html"
        }
    ],
    "relationship_type": "uses"
}

STIX_DATA = [
    COURSE_OF_ACTION_A,
    COURSE_OF_ACTION_B,
    COURSE_OF_ACTION_C,
    ATTACK_PATTERN_A,
    INTRUSION_SET_A,
    MALWARE_A,
    RELATIONSHIP_A,
    RELATIONSHIP_B,
    RELATIONSHIP_C,
    RELATIONSHIP_D,
]


class StixClientTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = red_raccoon.integrations.stix.api.get_stix_client(data=STIX_DATA)
        cls.maxDiff = None

    def test_search_for_objects_with_string(self):
        with self.assertRaises(TypeError):
            self.api.search_for_object(ATTACK_PATTERN)

    def test_search_for_objects_with_single_filter(self):
        predicate = red_raccoon.integrations.stix.filters.get_object_type_filter(object_types=MALWARE)
        expected = [MALWARE_A]
        result = list(map(
            red_raccoon.integrations.stix.parsers.stix2_to_dict, self.api.search_for_objects(filters=predicate)
        ))
        self.assertEqual({o['id'] for o in expected}, {o['id'] for o in result})

    def test_search_for_objects_with_list_of_filters(self):
        predicate = red_raccoon.integrations.stix.filters.get_object_type_filter(object_types=MALWARE)
        expected = [MALWARE_A]
        result = list(map(
            red_raccoon.integrations.stix.parsers.stix2_to_dict, self.api.search_for_objects(filters=[predicate])
        ))
        self.assertEqual({o['id'] for o in expected}, {o['id'] for o in result})

    def test_search_for_objects_without_any_filters(self):
        expected = STIX_DATA
        result = list(map(red_raccoon.integrations.stix.parsers.stix2_to_dict, self.api.search_for_objects()))
        self.assertEqual({o['id'] for o in expected}, {o['id'] for o in result})

    def test_search_for_object_with_string(self):
        with self.assertRaises(TypeError):
            self.api.search_for_object(ATTACK_PATTERN)

    def test_search_for_object_with_single_filter(self):
        predicate = red_raccoon.integrations.stix.filters.get_string_filter(
            lhs="x_mitre_contributors",
            rhs="Johann Rehberger"
        )
        expected = ATTACK_PATTERN_A
        result = self.api.search_for_object(filters=predicate)
        result = red_raccoon.integrations.stix.parsers.stix2_to_dict(result)
        self.assertEqual(expected['id'], result['id'])

    def test_search_for_object_with_list_of_filters(self):
        predicate = red_raccoon.integrations.stix.filters.get_string_filter(
            lhs="x_mitre_contributors",
            rhs="Johann Rehberger",
        )
        expected = ATTACK_PATTERN_A
        result = self.api.search_for_object(filters=[predicate])
        result = red_raccoon.integrations.stix.parsers.stix2_to_dict(result)
        self.assertEqual(expected['id'], result['id'])

    def test_search_for_object_without_any_filters(self):
        result = self.api.search_for_object()
        result = red_raccoon.integrations.stix.parsers.stix2_to_dict(result)
        self.assertIsInstance(result, dict)

    def test_get_object_by_internal_id(self):
        expected = COURSE_OF_ACTION_A
        result = self.api.get_object(object_internal_id=COURSE_OF_ACTION_A['id'])
        result = red_raccoon.integrations.stix.parsers.stix2_to_dict(result)
        self.assertEqual(expected['id'], result['id'])

    def test_get_object_by_external_id(self):
        expected = COURSE_OF_ACTION_A
        result = self.api.get_object(object_external_id='M1017')
        result = red_raccoon.integrations.stix.parsers.stix2_to_dict(result)
        self.assertEqual(expected['id'], result['id'])

    def test_get_objects(self):
        expected = set(map(lambda o: o['id'], STIX_DATA))
        result = set(map(lambda o: o['id'], self.api.get_objects()))
        self.assertEqual(expected, result)

    def test_get_objects_by_object_type(self):
        expected = set(map(
            lambda o: o['id'], filter(lambda o: o['type'] == RELATIONSHIP, STIX_DATA)
        ))
        result = set(map(lambda o: o['id'], self.api.get_objects(object_types=[RELATIONSHIP])))
        self.assertEqual(expected, result)

    def test_get_objects_by_internal_id(self):
        expected = set(map(
            lambda o: o['id'], filter(lambda o: o['id'] == COURSE_OF_ACTION_A['id'], STIX_DATA)
        ))
        result = set(map(
            lambda o: o['id'], self.api.get_objects(
                object_internal_ids=[COURSE_OF_ACTION_A['id']]
            )
        ))
        self.assertEqual(expected, result)

    def test_get_objects_by_external_id(self):
        expected = {self.api.get_object(object_external_id='M1017')['id']}
        result = set(map(
            lambda o: o['id'], self.api.get_objects(object_external_ids=['M1017'])
        ))
        self.assertEqual(expected, result)

    def test_get_object_internal_ids_by_object_type(self):
        object_types = [
            ATTACK_PATTERN, COURSE_OF_ACTION
        ]
        expected = {
            'course-of-action--b045d015-6bed-4490-bd38-56b41ece59a0',
            'course-of-action--b5dbb4c5-b0b1-40b1-80b6-e9e84ab90067',
            'course-of-action--2a4f6c11-a4a7-4cb9-b0ef-6ae1bb3a718a',
            'attack-pattern--10ffac09-e42d-4f56-ab20-db94c67d76ff',
        }
        result = set(self.api.get_object_internal_ids(object_types=object_types))
        self.assertEqual(expected, result)

    def test_get_relationships_by_source_internal_id(self):
        expected = {'relationship--f780f9d8-1baa-41b7-b7a1-acba717df0ab'}
        result = {o['id'] for o in self.api.get_relationships(
            source_object_internal_ids=[COURSE_OF_ACTION_A['id']]
        )}
        self.assertEqual(expected, result)

    def test_get_relationships_by_target_internal_id(self):
        expected = {
            'relationship--248a0d72-d9cd-43d3-985f-a33a49a79e8b',
            'relationship--7a1cf82e-68e5-49ca-89ae-e492cd85dab4',
            'relationship--f780f9d8-1baa-41b7-b7a1-acba717df0ab'
        }
        result = {o['id'] for o in self.api.get_relationships(
            target_object_internal_ids=[ATTACK_PATTERN_A['id']]
        )}
        self.assertEqual(expected, result)

    def test_get_relationships_by_source_object_type(self):
        expected = {
            'relationship--248a0d72-d9cd-43d3-985f-a33a49a79e8b',
            'relationship--7a1cf82e-68e5-49ca-89ae-e492cd85dab4',
            'relationship--f780f9d8-1baa-41b7-b7a1-acba717df0ab'
        }
        result = {o['id'] for o in self.api.get_relationships(
            source_object_types=[COURSE_OF_ACTION]
        )}
        self.assertEqual(expected, result)

    def test_get_relationships_by_target_object_type(self):
        expected = {
            'relationship--039364a9-2afd-4ae5-9df0-08d4e583674f',
            'relationship--248a0d72-d9cd-43d3-985f-a33a49a79e8b',
            'relationship--7a1cf82e-68e5-49ca-89ae-e492cd85dab4',
            'relationship--f780f9d8-1baa-41b7-b7a1-acba717df0ab'
        }
        result = {o['id'] for o in self.api.get_relationships(
            target_object_types=[ATTACK_PATTERN]
        )}
        self.assertEqual(expected, result)

    def test_get_relationships_by_relationship_type(self):
        expected = {
            'relationship--248a0d72-d9cd-43d3-985f-a33a49a79e8b',
            'relationship--7a1cf82e-68e5-49ca-89ae-e492cd85dab4',
            'relationship--f780f9d8-1baa-41b7-b7a1-acba717df0ab'
        }
        result = {o['id'] for o in self.api.get_relationships(
            relationship_types=[MITIGATES]
        )}
        self.assertEqual(expected, result)
