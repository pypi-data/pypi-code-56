from red_raccoon.integrations.mitre_attack import DEFAULT_MITRE_ATTACK_MOBILE_STIX_DATA_PATH as MOBILE_STIX_DATA_PATH
from red_raccoon.integrations.mitre_attack.api import MitreAttack
from red_raccoon.integrations.mitre_attack.types import EnterpriseTechnique, MobileTechnique, PreAttackTechnique, \
    Tool, Malware, Tactic, Relationship, Mitigation, Identity, Matrix, MarkingDefinition, Group

import hodgepodge.helpers
import unittest
import logging
import os

logging.basicConfig(level=logging.INFO)

CTI_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../../../resources/mitre/cti/groups"
))


ENTERPRISE_STIX_DATA_PATH = os.path.join(CTI_DIR, 'enterprise/CopyKittens.json.gz')
PRE_ATTACK_STIX_DATA_PATH = os.path.join(CTI_DIR, 'pre_attack/Cleaver.json.gz')


class _MitreAttackTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for path in [ENTERPRISE_STIX_DATA_PATH, MOBILE_STIX_DATA_PATH, PRE_ATTACK_STIX_DATA_PATH]:
            if not os.path.exists(path):
                raise FileNotFoundError(path)

        cls.api = MitreAttack(
            enterprise_stix_data_path=ENTERPRISE_STIX_DATA_PATH,
            mobile_stix_data_path=MOBILE_STIX_DATA_PATH,
            pre_attack_stix_data_path=PRE_ATTACK_STIX_DATA_PATH,
            ignore_revoked=False,
            ignore_deprecated=False,
        )

    def assert_is_non_empty_list(self, rows):
        self.assertIsInstance(rows, list)
        self.assertGreater(len(rows), 0)

    def assert_is_non_empty_list_of_type(self, rows, types):
        types = hodgepodge.helpers.as_tuple(types)
        self.assertIsInstance(rows, list)
        self.assertGreater(len(rows), 0)
        for row in rows:
            self.assertIsInstance(row, types)

    def _get_relationships(self, func, source_object_types=None, source_object_ids=None, relationship_types=None,
                           target_object_types=None, target_object_ids=None):

        relationships = func(
            source_object_types=source_object_types,
            relationship_types=relationship_types,
            target_object_types=target_object_types,
            source_object_ids=source_object_ids,
            target_object_ids=target_object_ids,
        )

        if relationships:
            self.assert_is_non_empty_list_of_type(relationships, Relationship)
            return relationships
        else:
            raise self.skipTest("No relationships found (source types: {}, relationship types: {}, target types: {}, "
                                "source IDs: {}, target IDs: {})".format(source_object_types or None,
                                                                         relationship_types or None,
                                                                         target_object_types or None,
                                                                         source_object_ids or None,
                                                                         target_object_ids or None))


class MitreAttackTestCases(_MitreAttackTestCases):
    def get_relationships(self, source_object_types=None, source_object_ids=None, relationship_types=None,
                          target_object_types=None, target_object_ids=None):

        return self._get_relationships(
            func=self.api.get_relationships,
            source_object_types=source_object_types,
            relationship_types=relationship_types,
            target_object_types=target_object_types,
            source_object_ids=source_object_ids,
            target_object_ids=target_object_ids,
        )

    def test_get_matrices(self):
        matrices = self.api.get_matrices()
        self.assert_is_non_empty_list_of_type(matrices, Matrix)

    def test_get_identities(self):
        identities = self.api.get_identities()
        self.assert_is_non_empty_list_of_type(identities, Identity)

    def test_get_marking_definitions(self):
        marking_definitions = self.api.get_marking_definitions()
        self.assert_is_non_empty_list_of_type(marking_definitions, MarkingDefinition)

    def test_get_relationships(self):
        relationships = self.get_relationships()
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

    def test_get_tactics(self):
        tactics = self.api.get_tactics()
        self.assert_is_non_empty_list_of_type(tactics, Tactic)

    def test_get_tactics_by_tactic_id(self):
        tactic = self.api.get_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        expected = {tactic.id}

        #: Result.
        tactics = self.api.get_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        result = {t.id for t in tactics}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_tactics_by_technique_id(self):
        technique = self.api.get_object(object_types=['attack-pattern'])
        self.assertIsInstance(technique, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        #: Expected.
        tactics = self.api.get_tactics()
        expected = {t.id for t in tactics if t.kill_chain_phase_name in technique.kill_chain_phase_names}

        #: Result.
        a = self.api.get_tactics(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_tactics_by_related_techniques(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_tactics_by_software_id(self):
        relationships = self.get_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        software_id = next(r.src for r in relationships)

        #: Expected.
        tactics = self.api.get_tactics(technique_ids={r.dst for r in relationships if r.src == software_id})
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        expected = {t.id for t in tactics}

        #: Result.
        a = self.api.get_tactics(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_tactics_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_tactics_by_group_id(self):
        relationships = self.get_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        group_id = next(r.src for r in relationships)

        #: Expected.
        tactics = self.api.get_tactics(technique_ids={r.dst for r in relationships if r.src == group_id})
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        expected = {t.id for t in tactics}

        #: Result.
        a = self.api.get_tactics(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_tactics_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_tactics_by_mitigation_id(self):
        relationships = self.get_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        mitigation_id = next(r.src for r in relationships)
        technique_ids = {r.dst for r in relationships if r.src == mitigation_id}

        #: Result.
        a = self.api.get_tactics(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_tactics_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Expected.
        tactics = self.api.get_tactics(technique_ids=technique_ids)
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        expected = {t.id for t in tactics}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_techniques(self):
        techniques = self.api.get_techniques()
        self.assert_is_non_empty_list_of_type(techniques, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

    def test_get_techniques_by_tactic_id(self):
        tactic = self.api.get_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = [t for t in self.api.get_techniques() if tactic.kill_chain_phase_name in t.kill_chain_phase_names]
        self.assert_is_non_empty_list_of_type(techniques, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))
        expected = {t.id for t in techniques}

        #: Result.
        a = self.api.get_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        b = self.api.get_techniques_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_techniques_by_technique_id(self):
        technique = self.api.get_object(object_types=['attack-pattern'])
        self.assertIsInstance(technique, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        #: Expected.
        expected = {technique.id}

        #: Result.
        techniques = self.api.get_techniques(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(techniques, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))
        result = {t.id for t in techniques}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_techniques_by_software_id(self):
        relationships = self.get_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        software_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == software_id}

        #: Result.
        a = self.api.get_techniques(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        b = self.api.get_techniques_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_techniques_by_group_id(self):
        relationships = self.get_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        group_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == group_id}

        #: Result.
        a = self.api.get_techniques(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        b = self.api.get_techniques_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_techniques_by_mitigation_id(self):
        relationships = self.get_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        mitigation_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == mitigation_id}

        #: Result.
        a = self.api.get_techniques(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        b = self.api.get_techniques_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_groups(self):
        groups = self.api.get_groups()
        self.assert_is_non_empty_list_of_type(groups, Group)

    def test_get_groups_by_tactic_id(self):
        tactic = self.api.get_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = self.api.get_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(techniques, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        relationships = self.get_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
            target_object_ids=[t.id for t in techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        expected = {r.src for r in relationships}

        #: Result.
        a = self.api.get_groups(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_groups_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, Group)

        self.assertEqual(a, b)
        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_groups_by_technique_id(self):
        relationships = self.get_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        technique_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == technique_id}

        #: Result.
        a = self.api.get_groups(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_groups_by_related_techniques(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(b, Group)

        self.assertEqual(a, b)
        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_groups_by_software_id(self):
        relationships = self.get_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['malware', 'tool'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        software_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == software_id}

        #: Result.
        a = self.api.get_groups(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_groups_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, Group)

        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_groups_by_group_id(self):
        group = self.api.get_object(object_types=['intrusion-set'])
        self.assertIsInstance(group, Group)

        #: Expected.
        expected = {group.id}

        #: Result.
        groups = self.api.get_groups(group_ids=[group.id])
        self.assert_is_non_empty_list_of_type(groups, Group)
        result = {g.id for g in groups}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_groups_by_mitigation_id(self):
        relationships_between_groups_and_techniques = self.get_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_groups_and_techniques, Relationship)

        relationships_between_mitigations_and_techniques = self.get_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationships_between_groups_and_techniques]
        )
        self.assert_is_non_empty_list_of_type(relationships_between_mitigations_and_techniques, Relationship)

        mitigation_id = next(r.src for r in relationships_between_mitigations_and_techniques)

        #: Expected.
        technique_ids = {r.dst for r in relationships_between_mitigations_and_techniques if r.src == mitigation_id}
        group_ids = {r.src for r in relationships_between_groups_and_techniques if r.dst in technique_ids}
        expected = group_ids

        #: Result.
        a = self.api.get_groups(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_groups_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, Group)

        self.assertEqual(a, b)
        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_software(self):
        software = self.api.get_software()
        self.assert_is_non_empty_list_of_type(software, (Malware, Tool))

    def test_get_software_by_tactic_id(self):
        tactic = self.api.get_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = self.api.get_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(techniques, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        relationships = self.get_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
            target_object_ids=[t.id for t in techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        expected = {r.src for r in relationships}

        #: Result.
        a = self.api.get_software(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_software_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        self.assertEqual(a, b)
        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_software_by_technique_id(self):
        relationships = self.get_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        technique_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == technique_id}

        #: Result.
        a = self.api.get_software(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_software_by_related_techniques(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_software_by_software_id(self):
        software = self.api.get_object(object_types=['malware', 'tool'])
        self.assertIsInstance(software, (Malware, Tool))

        #: Expected.
        expected = {software.id}

        #: Result.
        software = self.api.get_software(software_ids=[software.id])
        self.assert_is_non_empty_list_of_type(software, (Malware, Tool))
        result = {s.id for s in software}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_software_by_group_id(self):
        relationships = self.get_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['malware', 'tool'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        group_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == group_id}

        #: Result.
        a = self.api.get_software(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_software_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_software_by_mitigation_id(self):
        relationship_between_software_and_techniques = self.get_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationship_between_software_and_techniques, Relationship)

        relationships_between_techniques_and_mitigations = self.get_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationship_between_software_and_techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_techniques_and_mitigations, Relationship)

        mitigation_id = next(r.src for r in relationships_between_techniques_and_mitigations)

        #: Expected.
        technique_ids = {r.dst for r in relationships_between_techniques_and_mitigations if r.src == mitigation_id}
        software_ids = {r.src for r in relationship_between_software_and_techniques if r.dst in technique_ids}
        expected = software_ids

        #: Result.
        a = self.api.get_software(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_software_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_malware(self):
        software = self.api.get_malware()
        self.assert_is_non_empty_list_of_type(software, Malware)

    def test_get_tools(self):
        software = self.api.get_tools()
        self.assert_is_non_empty_list_of_type(software, Tool)

    def test_get_mitigations(self):
        mitigations = self.api.get_mitigations()
        self.assert_is_non_empty_list_of_type(mitigations, Mitigation)

    def test_get_mitigations_by_tactic_id(self):
        tactic = self.api.get_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = self.api.get_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(techniques, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

        relationships = self.get_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[t.id for t in techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        expected = {r.src for r in relationships}

        #: Result.
        a = self.api.get_mitigations(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_mitigations_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        self.assertEqual(a, b)
        result = {m.id for m in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mitigations_by_technique_id(self):
        relationships = self.get_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        technique_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == technique_id}

        #: Result.
        a = self.api.get_mitigations(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_mitigations_by_related_techniques(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        self.assertEqual(a, b)
        result = {m.id for m in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mitigations_by_software_id(self):
        relationship_between_software_and_techniques = self.get_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationship_between_software_and_techniques, Relationship)

        relationships_between_techniques_and_mitigations = self.get_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationship_between_software_and_techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_techniques_and_mitigations, Relationship)

        software_id = next(r.src for r in relationship_between_software_and_techniques)

        #: Expected.
        technique_ids = {r.dst for r in relationship_between_software_and_techniques if r.src == software_id}
        mitigation_ids = {r.src for r in relationships_between_techniques_and_mitigations if r.dst in technique_ids}
        expected = mitigation_ids

        #: Result.
        a = self.api.get_mitigations(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_mitigations_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        self.assertEqual(a, b)
        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mitigations_by_group_id(self):
        relationship_between_groups_and_techniques = self.get_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationship_between_groups_and_techniques, Relationship)

        relationships_between_techniques_and_mitigations = self.get_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationship_between_groups_and_techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_techniques_and_mitigations, Relationship)

        group_id = next(r.src for r in relationship_between_groups_and_techniques)

        #: Expected.
        technique_ids = {r.dst for r in relationship_between_groups_and_techniques if r.src == group_id}
        mitigation_ids = {r.src for r in relationships_between_techniques_and_mitigations if r.dst in technique_ids}
        expected = mitigation_ids

        #: Result.
        a = self.api.get_mitigations(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_mitigations_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mitigations_by_mitigation_id(self):
        mitigation = self.api.get_object(object_types=['course-of-action'])
        self.assertIsInstance(mitigation, Mitigation)

        #: Expected.
        mitigations = self.api.get_mitigations(mitigation_ids=[mitigation.id])
        self.assert_is_non_empty_list_of_type(mitigations, Mitigation)
        expected = {mitigation.id}

        #: Result.
        result = {m.id for m in mitigations}

        #: Verify.
        self.assertEqual(expected, result)


class MitreAttackEnterpriseTestCases(_MitreAttackTestCases):
    def get_enterprise_relationships(self, source_object_types=None, source_object_ids=None, relationship_types=None,
                                     target_object_types=None, target_object_ids=None):

        return self._get_relationships(
            func=self.api.get_enterprise_relationships,
            source_object_types=source_object_types,
            relationship_types=relationship_types,
            target_object_types=target_object_types,
            source_object_ids=source_object_ids,
            target_object_ids=target_object_ids,
        )

    def test_get_enterprise_matrices(self):
        matrices = self.api.get_enterprise_matrices()
        self.assert_is_non_empty_list_of_type(matrices, Matrix)

    def test_get_enterprise_identities(self):
        identities = self.api.get_enterprise_identities()
        self.assert_is_non_empty_list_of_type(identities, Identity)

    def test_get_enterprise_marking_definitions(self):
        marking_definitions = self.api.get_enterprise_marking_definitions()
        self.assert_is_non_empty_list_of_type(marking_definitions, MarkingDefinition)

    def test_get_enterprise_relationships(self):
        relationships = self.get_enterprise_relationships()
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

    def test_get_enterprise_tactics(self):
        tactics = self.api.get_enterprise_tactics()
        self.assert_is_non_empty_list_of_type(tactics, Tactic)

    def test_get_enterprise_tactics_by_tactic_id(self):
        tactic = self.api.get_enterprise_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        expected = {tactic.id}

        #: Result.
        tactics = self.api.get_enterprise_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        result = {t.id for t in tactics}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_tactics_by_technique_id(self):
        technique = self.api.get_enterprise_object(object_types=['attack-pattern'])
        self.assertIsInstance(technique, EnterpriseTechnique)

        #: Expected.
        tactics = self.api.get_enterprise_tactics()
        expected = {t.id for t in tactics if t.kill_chain_phase_name in technique.kill_chain_phase_names}

        #: Result.
        a = self.api.get_enterprise_tactics(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_enterprise_tactics_by_related_techniques(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_tactics_by_software_id(self):
        relationships = self.get_enterprise_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        software_id = next(r.src for r in relationships)

        #: Expected.
        tactics = self.api.get_enterprise_tactics(technique_ids={r.dst for r in relationships if r.src == software_id})
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        expected = {t.id for t in tactics}

        #: Result.
        a = self.api.get_enterprise_tactics(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_enterprise_tactics_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_tactics_by_group_id(self):
        relationships = self.get_enterprise_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        group_id = next(r.src for r in relationships)

        #: Expected.
        tactics = self.api.get_enterprise_tactics(technique_ids={r.dst for r in relationships if r.src == group_id})
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        expected = {t.id for t in tactics}

        #: Result.
        a = self.api.get_enterprise_tactics(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_enterprise_tactics_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_tactics_by_mitigation_id(self):
        relationships = self.get_enterprise_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        mitigation_id = next(r.src for r in relationships)
        technique_ids = {r.dst for r in relationships if r.src == mitigation_id}

        #: Result.
        a = self.api.get_enterprise_tactics(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_enterprise_tactics_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Expected.
        tactics = self.api.get_enterprise_tactics(technique_ids=technique_ids)
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        expected = {t.id for t in tactics}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_techniques(self):
        techniques = self.api.get_enterprise_techniques()
        self.assert_is_non_empty_list_of_type(techniques, EnterpriseTechnique)

    def test_get_enterprise_techniques_by_tactic_id(self):
        tactic = self.api.get_enterprise_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = [
            t for t in self.api.get_enterprise_techniques() if tactic.kill_chain_phase_name in t.kill_chain_phase_names
        ]
        self.assert_is_non_empty_list_of_type(techniques, EnterpriseTechnique)
        expected = {t.id for t in techniques}

        #: Result.
        a = self.api.get_enterprise_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, EnterpriseTechnique)

        b = self.api.get_enterprise_techniques_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, EnterpriseTechnique)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_techniques_by_technique_id(self):
        technique = self.api.get_enterprise_object(object_types=['attack-pattern'])
        self.assertIsInstance(technique, EnterpriseTechnique)

        #: Expected.
        expected = {technique.id}

        #: Result.
        techniques = self.api.get_enterprise_techniques(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(techniques, EnterpriseTechnique)
        result = {t.id for t in techniques}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_techniques_by_software_id(self):
        relationships = self.get_enterprise_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        software_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == software_id}

        #: Result.
        a = self.api.get_enterprise_techniques(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, EnterpriseTechnique)

        b = self.api.get_enterprise_techniques_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, EnterpriseTechnique)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_techniques_by_group_id(self):
        relationships = self.get_enterprise_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        group_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == group_id}

        #: Result.
        a = self.api.get_enterprise_techniques(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, EnterpriseTechnique)

        b = self.api.get_enterprise_techniques_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, EnterpriseTechnique)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_techniques_by_mitigation_id(self):
        relationships = self.get_enterprise_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        mitigation_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == mitigation_id}

        #: Result.
        a = self.api.get_enterprise_techniques(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, EnterpriseTechnique)

        b = self.api.get_enterprise_techniques_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, EnterpriseTechnique)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_groups(self):
        groups = self.api.get_enterprise_groups()
        self.assert_is_non_empty_list_of_type(groups, Group)

    def test_get_enterprise_groups_by_tactic_id(self):
        tactic = self.api.get_enterprise_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = self.api.get_enterprise_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(techniques, EnterpriseTechnique)

        relationships = self.get_enterprise_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
            target_object_ids=[t.id for t in techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        expected = {r.src for r in relationships}

        #: Result.
        a = self.api.get_enterprise_groups(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_enterprise_groups_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, Group)

        self.assertEqual(a, b)
        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_groups_by_technique_id(self):
        relationships = self.get_enterprise_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        technique_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == technique_id}

        #: Result.
        a = self.api.get_enterprise_groups(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_enterprise_groups_by_related_techniques(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(b, Group)

        self.assertEqual(a, b)
        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_groups_by_software_id(self):
        relationships = self.get_enterprise_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['malware', 'tool'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        software_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == software_id}

        #: Result.
        a = self.api.get_enterprise_groups(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_enterprise_groups_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, Group)

        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_groups_by_group_id(self):
        group = self.api.get_enterprise_object(object_types=['intrusion-set'])
        self.assertIsInstance(group, Group)

        #: Expected.
        expected = {group.id}

        #: Result.
        groups = self.api.get_enterprise_groups(group_ids=[group.id])
        self.assert_is_non_empty_list_of_type(groups, Group)
        result = {g.id for g in groups}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_groups_by_mitigation_id(self):
        relationships_between_groups_and_techniques = self.get_enterprise_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_groups_and_techniques, Relationship)

        relationships_between_mitigations_and_techniques = self.get_enterprise_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationships_between_groups_and_techniques]
        )
        self.assert_is_non_empty_list_of_type(relationships_between_mitigations_and_techniques, Relationship)

        mitigation_id = next(r.src for r in relationships_between_mitigations_and_techniques)

        #: Expected.
        technique_ids = {r.dst for r in relationships_between_mitigations_and_techniques if r.src == mitigation_id}
        group_ids = {r.src for r in relationships_between_groups_and_techniques if r.dst in technique_ids}
        expected = group_ids

        #: Result.
        a = self.api.get_enterprise_groups(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_enterprise_groups_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, Group)

        self.assertEqual(a, b)
        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_software(self):
        software = self.api.get_enterprise_software()
        self.assert_is_non_empty_list_of_type(software, (Malware, Tool))

    def test_get_enterprise_software_by_tactic_id(self):
        tactic = self.api.get_enterprise_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = self.api.get_enterprise_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(techniques, EnterpriseTechnique)

        relationships = self.get_enterprise_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
            target_object_ids=[t.id for t in techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        expected = {r.src for r in relationships}

        #: Result.
        a = self.api.get_enterprise_software(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_enterprise_software_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        self.assertEqual(a, b)
        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_software_by_technique_id(self):
        relationships = self.get_enterprise_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        technique_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == technique_id}

        #: Result.
        a = self.api.get_enterprise_software(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_enterprise_software_by_related_techniques(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_software_by_software_id(self):
        software = self.api.get_enterprise_object(object_types=['malware', 'tool'])
        self.assertIsInstance(software, (Malware, Tool))

        #: Expected.
        expected = {software.id}

        #: Result.
        software = self.api.get_enterprise_software(software_ids=[software.id])
        self.assert_is_non_empty_list_of_type(software, (Malware, Tool))
        result = {s.id for s in software}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_software_by_group_id(self):
        relationships = self.get_enterprise_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['malware', 'tool'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        group_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == group_id}

        #: Result.
        a = self.api.get_enterprise_software(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_enterprise_software_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_software_by_mitigation_id(self):
        relationship_between_software_and_techniques = self.get_enterprise_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationship_between_software_and_techniques, Relationship)

        relationships_between_techniques_and_mitigations = self.get_enterprise_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationship_between_software_and_techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_techniques_and_mitigations, Relationship)

        mitigation_id = next(r.src for r in relationships_between_techniques_and_mitigations)

        #: Expected.
        technique_ids = {r.dst for r in relationships_between_techniques_and_mitigations if r.src == mitigation_id}
        software_ids = {r.src for r in relationship_between_software_and_techniques if r.dst in technique_ids}
        expected = software_ids

        #: Result.
        a = self.api.get_enterprise_software(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_enterprise_software_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_malware(self):
        software = self.api.get_enterprise_malware()
        self.assert_is_non_empty_list_of_type(software, Malware)

    def test_get_enterprise_tools(self):
        software = self.api.get_enterprise_tools()
        self.assert_is_non_empty_list_of_type(software, Tool)

    def test_get_enterprise_mitigations(self):
        mitigations = self.api.get_enterprise_mitigations()
        self.assert_is_non_empty_list_of_type(mitigations, Mitigation)

    def test_get_enterprise_mitigations_by_tactic_id(self):
        tactic = self.api.get_enterprise_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = self.api.get_enterprise_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(techniques, EnterpriseTechnique)

        relationships = self.get_enterprise_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[t.id for t in techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        expected = {r.src for r in relationships}

        #: Result.
        a = self.api.get_enterprise_mitigations(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_enterprise_mitigations_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        self.assertEqual(a, b)
        result = {m.id for m in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_mitigations_by_technique_id(self):
        relationships = self.get_enterprise_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        technique_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == technique_id}

        #: Result.
        a = self.api.get_enterprise_mitigations(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_enterprise_mitigations_by_related_techniques(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        self.assertEqual(a, b)
        result = {m.id for m in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_mitigations_by_software_id(self):
        relationship_between_software_and_techniques = self.get_enterprise_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationship_between_software_and_techniques, Relationship)

        relationships_between_techniques_and_mitigations = self.get_enterprise_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationship_between_software_and_techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_techniques_and_mitigations, Relationship)

        software_id = next(r.src for r in relationship_between_software_and_techniques)

        #: Expected.
        technique_ids = {r.dst for r in relationship_between_software_and_techniques if r.src == software_id}
        mitigation_ids = {r.src for r in relationships_between_techniques_and_mitigations if r.dst in technique_ids}
        expected = mitigation_ids

        #: Result.
        a = self.api.get_enterprise_mitigations(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_enterprise_mitigations_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        self.assertEqual(a, b)
        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_mitigations_by_group_id(self):
        relationship_between_groups_and_techniques = self.get_enterprise_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationship_between_groups_and_techniques, Relationship)

        relationships_between_techniques_and_mitigations = self.get_enterprise_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationship_between_groups_and_techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_techniques_and_mitigations, Relationship)

        group_id = next(r.src for r in relationship_between_groups_and_techniques)

        #: Expected.
        technique_ids = {r.dst for r in relationship_between_groups_and_techniques if r.src == group_id}
        mitigation_ids = {r.src for r in relationships_between_techniques_and_mitigations if r.dst in technique_ids}
        expected = mitigation_ids

        #: Result.
        a = self.api.get_enterprise_mitigations(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_enterprise_mitigations_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_enterprise_mitigations_by_mitigation_id(self):
        mitigation = self.api.get_enterprise_object(object_types=['course-of-action'])
        self.assertIsInstance(mitigation, Mitigation)

        #: Expected.
        mitigations = self.api.get_enterprise_mitigations(mitigation_ids=[mitigation.id])
        self.assert_is_non_empty_list_of_type(mitigations, Mitigation)
        expected = {mitigation.id}

        #: Result.
        result = {m.id for m in mitigations}

        #: Verify.
        self.assertEqual(expected, result)


class MitreAttackMobileTestCases(_MitreAttackTestCases):
    def get_mobile_relationships(self, source_object_types=None, source_object_ids=None, relationship_types=None,
                                 target_object_types=None, target_object_ids=None):

        return self._get_relationships(
            func=self.api.get_mobile_relationships,
            source_object_types=source_object_types,
            relationship_types=relationship_types,
            target_object_types=target_object_types,
            source_object_ids=source_object_ids,
            target_object_ids=target_object_ids,
        )

    def test_get_mobile_matrices(self):
        matrices = self.api.get_mobile_matrices()
        self.assert_is_non_empty_list_of_type(matrices, Matrix)

    def test_get_mobile_identities(self):
        identities = self.api.get_mobile_identities()
        self.assert_is_non_empty_list_of_type(identities, Identity)

    def test_get_mobile_marking_definitions(self):
        marking_definitions = self.api.get_mobile_marking_definitions()
        self.assert_is_non_empty_list_of_type(marking_definitions, MarkingDefinition)

    def test_get_mobile_relationships(self):
        relationships = self.get_mobile_relationships()
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

    def test_get_mobile_tactics(self):
        tactics = self.api.get_mobile_tactics()
        self.assert_is_non_empty_list_of_type(tactics, Tactic)

    def test_get_mobile_tactics_by_tactic_id(self):
        tactic = self.api.get_mobile_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        expected = {tactic.id}

        #: Result.
        tactics = self.api.get_mobile_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        result = {t.id for t in tactics}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_tactics_by_technique_id(self):
        technique = self.api.get_mobile_object(object_types=['attack-pattern'])
        self.assertIsInstance(technique, MobileTechnique)

        #: Expected.
        tactics = self.api.get_mobile_tactics()
        expected = {t.id for t in tactics if t.kill_chain_phase_name in technique.kill_chain_phase_names}

        #: Result.
        a = self.api.get_mobile_tactics(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_mobile_tactics_by_related_techniques(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_tactics_by_software_id(self):
        relationships = self.get_mobile_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        software_id = next(r.src for r in relationships)

        #: Expected.
        tactics = self.api.get_mobile_tactics(technique_ids={r.dst for r in relationships if r.src == software_id})
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        expected = {t.id for t in tactics}

        #: Result.
        a = self.api.get_mobile_tactics(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_mobile_tactics_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_tactics_by_group_id(self):
        relationships = self.get_mobile_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        group_id = next(r.src for r in relationships)

        #: Expected.
        tactics = self.api.get_mobile_tactics(technique_ids={r.dst for r in relationships if r.src == group_id})
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        expected = {t.id for t in tactics}

        #: Result.
        a = self.api.get_mobile_tactics(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_mobile_tactics_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_tactics_by_mitigation_id(self):
        relationships = self.get_mobile_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        mitigation_id = next(r.src for r in relationships)
        technique_ids = {r.dst for r in relationships if r.src == mitigation_id}

        #: Result.
        a = self.api.get_mobile_tactics(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_mobile_tactics_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Expected.
        tactics = self.api.get_mobile_tactics(technique_ids=technique_ids)
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        expected = {t.id for t in tactics}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_techniques(self):
        techniques = self.api.get_mobile_techniques()
        self.assert_is_non_empty_list_of_type(techniques, MobileTechnique)

    def test_get_mobile_techniques_by_tactic_id(self):
        tactic = self.api.get_mobile_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = [
            t for t in self.api.get_mobile_techniques() if tactic.kill_chain_phase_name in t.kill_chain_phase_names
        ]
        self.assert_is_non_empty_list_of_type(techniques, MobileTechnique)
        expected = {t.id for t in techniques}

        #: Result.
        a = self.api.get_mobile_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, MobileTechnique)

        b = self.api.get_mobile_techniques_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, MobileTechnique)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_techniques_by_technique_id(self):
        technique = self.api.get_mobile_object(object_types=['attack-pattern'])
        self.assertIsInstance(technique, MobileTechnique)

        #: Expected.
        expected = {technique.id}

        #: Result.
        techniques = self.api.get_mobile_techniques(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(techniques, MobileTechnique)
        result = {t.id for t in techniques}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_techniques_by_software_id(self):
        relationships = self.get_mobile_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        software_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == software_id}

        #: Result.
        a = self.api.get_mobile_techniques(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, MobileTechnique)

        b = self.api.get_mobile_techniques_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, MobileTechnique)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_techniques_by_group_id(self):
        relationships = self.get_mobile_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        group_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == group_id}

        #: Result.
        a = self.api.get_mobile_techniques(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, MobileTechnique)

        b = self.api.get_mobile_techniques_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, MobileTechnique)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_techniques_by_mitigation_id(self):
        relationships = self.get_mobile_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        mitigation_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == mitigation_id}

        #: Result.
        a = self.api.get_mobile_techniques(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, MobileTechnique)

        b = self.api.get_mobile_techniques_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, MobileTechnique)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_groups(self):
        groups = self.api.get_mobile_groups()
        self.assert_is_non_empty_list_of_type(groups, Group)

    def test_get_mobile_groups_by_tactic_id(self):
        tactic = self.api.get_mobile_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = self.api.get_mobile_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(techniques, MobileTechnique)

        relationships = self.get_mobile_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
            target_object_ids=[t.id for t in techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        expected = {r.src for r in relationships}

        #: Result.
        a = self.api.get_mobile_groups(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_mobile_groups_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, Group)

        self.assertEqual(a, b)
        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_groups_by_technique_id(self):
        relationships = self.get_mobile_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        technique_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == technique_id}

        #: Result.
        a = self.api.get_mobile_groups(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_mobile_groups_by_related_techniques(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(b, Group)

        self.assertEqual(a, b)
        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_groups_by_software_id(self):
        relationships = self.get_mobile_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['malware', 'tool'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        software_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == software_id}

        #: Result.
        a = self.api.get_mobile_groups(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_mobile_groups_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, Group)

        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_groups_by_group_id(self):
        group = self.api.get_mobile_object(object_types=['intrusion-set'])
        self.assertIsInstance(group, Group)

        #: Expected.
        expected = {group.id}

        #: Result.
        groups = self.api.get_mobile_groups(group_ids=[group.id])
        self.assert_is_non_empty_list_of_type(groups, Group)
        result = {g.id for g in groups}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_groups_by_mitigation_id(self):
        relationships_between_groups_and_techniques = self.get_mobile_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_groups_and_techniques, Relationship)

        relationships_between_mitigations_and_techniques = self.get_mobile_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationships_between_groups_and_techniques]
        )
        self.assert_is_non_empty_list_of_type(relationships_between_mitigations_and_techniques, Relationship)

        mitigation_id = next(r.src for r in relationships_between_mitigations_and_techniques)

        #: Expected.
        technique_ids = {r.dst for r in relationships_between_mitigations_and_techniques if r.src == mitigation_id}
        group_ids = {r.src for r in relationships_between_groups_and_techniques if r.dst in technique_ids}
        expected = group_ids

        #: Result.
        a = self.api.get_mobile_groups(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_mobile_groups_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, Group)

        self.assertEqual(a, b)
        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_software(self):
        software = self.api.get_mobile_software()
        self.assert_is_non_empty_list_of_type(software, (Malware, Tool))

    def test_get_mobile_software_by_tactic_id(self):
        tactic = self.api.get_mobile_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = self.api.get_mobile_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(techniques, MobileTechnique)

        relationships = self.get_mobile_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
            target_object_ids=[t.id for t in techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        expected = {r.src for r in relationships}

        #: Result.
        a = self.api.get_mobile_software(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_mobile_software_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        self.assertEqual(a, b)
        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_software_by_technique_id(self):
        relationships = self.get_mobile_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        technique_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == technique_id}

        #: Result.
        a = self.api.get_mobile_software(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_mobile_software_by_related_techniques(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_software_by_software_id(self):
        software = self.api.get_mobile_object(object_types=['malware', 'tool'])
        self.assertIsInstance(software, (Malware, Tool))

        #: Expected.
        expected = {software.id}

        #: Result.
        software = self.api.get_mobile_software(software_ids=[software.id])
        self.assert_is_non_empty_list_of_type(software, (Malware, Tool))
        result = {s.id for s in software}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_software_by_group_id(self):
        relationships = self.get_mobile_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['malware', 'tool'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        group_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == group_id}

        #: Result.
        a = self.api.get_mobile_software(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_mobile_software_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_software_by_mitigation_id(self):
        relationship_between_software_and_techniques = self.get_mobile_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationship_between_software_and_techniques, Relationship)

        relationships_between_techniques_and_mitigations = self.get_mobile_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationship_between_software_and_techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_techniques_and_mitigations, Relationship)

        mitigation_id = next(r.src for r in relationships_between_techniques_and_mitigations)

        #: Expected.
        technique_ids = {r.dst for r in relationships_between_techniques_and_mitigations if r.src == mitigation_id}
        software_ids = {r.src for r in relationship_between_software_and_techniques if r.dst in technique_ids}
        expected = software_ids

        #: Result.
        a = self.api.get_mobile_software(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(a, (Malware, Tool))

        b = self.api.get_mobile_software_by_related_mitigations(mitigation_ids=[mitigation_id])
        self.assert_is_non_empty_list_of_type(b, (Malware, Tool))

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_malware(self):
        software = self.api.get_mobile_malware()
        self.assert_is_non_empty_list_of_type(software, Malware)

    def test_get_mobile_tools(self):
        software = self.api.get_mobile_tools()
        self.assert_is_non_empty_list_of_type(software, Tool)

    def test_get_mobile_mitigations(self):
        mitigations = self.api.get_mobile_mitigations()
        self.assert_is_non_empty_list_of_type(mitigations, Mitigation)

    def test_get_mobile_mitigations_by_tactic_id(self):
        tactic = self.api.get_mobile_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = self.api.get_mobile_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(techniques, MobileTechnique)

        relationships = self.get_mobile_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[t.id for t in techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        expected = {r.src for r in relationships}

        #: Result.
        a = self.api.get_mobile_mitigations(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_mobile_mitigations_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        self.assertEqual(a, b)
        result = {m.id for m in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_mitigations_by_technique_id(self):
        relationships = self.get_mobile_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        technique_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == technique_id}

        #: Result.
        a = self.api.get_mobile_mitigations(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_mobile_mitigations_by_related_techniques(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        self.assertEqual(a, b)
        result = {m.id for m in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_mitigations_by_software_id(self):
        relationship_between_software_and_techniques = self.get_mobile_relationships(
            source_object_types=['malware', 'tool'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationship_between_software_and_techniques, Relationship)

        relationships_between_techniques_and_mitigations = self.get_mobile_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationship_between_software_and_techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_techniques_and_mitigations, Relationship)

        software_id = next(r.src for r in relationship_between_software_and_techniques)

        #: Expected.
        technique_ids = {r.dst for r in relationship_between_software_and_techniques if r.src == software_id}
        mitigation_ids = {r.src for r in relationships_between_techniques_and_mitigations if r.dst in technique_ids}
        expected = mitigation_ids

        #: Result.
        a = self.api.get_mobile_mitigations(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_mobile_mitigations_by_related_software(software_ids=[software_id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        self.assertEqual(a, b)
        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_mitigations_by_group_id(self):
        relationship_between_groups_and_techniques = self.get_mobile_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationship_between_groups_and_techniques, Relationship)

        relationships_between_techniques_and_mitigations = self.get_mobile_relationships(
            source_object_types=['course-of-action'],
            relationship_types=['mitigates'],
            target_object_types=['attack-pattern'],
            target_object_ids=[r.dst for r in relationship_between_groups_and_techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships_between_techniques_and_mitigations, Relationship)

        group_id = next(r.src for r in relationship_between_groups_and_techniques)

        #: Expected.
        technique_ids = {r.dst for r in relationship_between_groups_and_techniques if r.src == group_id}
        mitigation_ids = {r.src for r in relationships_between_techniques_and_mitigations if r.dst in technique_ids}
        expected = mitigation_ids

        #: Result.
        a = self.api.get_mobile_mitigations(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, Mitigation)

        b = self.api.get_mobile_mitigations_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, Mitigation)

        result = {s.id for s in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_mobile_mitigations_by_mitigation_id(self):
        mitigation = self.api.get_mobile_object(object_types=['course-of-action'])
        self.assertIsInstance(mitigation, Mitigation)

        #: Expected.
        mitigations = self.api.get_mobile_mitigations(mitigation_ids=[mitigation.id])
        self.assert_is_non_empty_list_of_type(mitigations, Mitigation)
        expected = {mitigation.id}

        #: Result.
        result = {m.id for m in mitigations}

        #: Verify.
        self.assertEqual(expected, result)


class MitreAttackPreAttackTestCases(_MitreAttackTestCases):
    def get_pre_attack_relationships(self, source_object_types=None, source_object_ids=None, relationship_types=None,
                                     target_object_types=None, target_object_ids=None):

        return self._get_relationships(
            func=self.api.get_pre_attack_relationships,
            source_object_types=source_object_types,
            relationship_types=relationship_types,
            target_object_types=target_object_types,
            source_object_ids=source_object_ids,
            target_object_ids=target_object_ids,
        )

    def test_get_pre_attack_matrices(self):
        matrices = self.api.get_pre_attack_matrices()
        self.assert_is_non_empty_list_of_type(matrices, Matrix)

    def test_get_pre_attack_identities(self):
        identities = self.api.get_pre_attack_identities()
        self.assert_is_non_empty_list_of_type(identities, Identity)

    def test_get_pre_attack_marking_definitions(self):
        marking_definitions = self.api.get_pre_attack_marking_definitions()
        self.assert_is_non_empty_list_of_type(marking_definitions, MarkingDefinition)

    def test_get_pre_attack_relationships(self):
        relationships = self.get_pre_attack_relationships()
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

    def test_get_pre_attack_tactics(self):
        tactics = self.api.get_pre_attack_tactics()
        self.assert_is_non_empty_list_of_type(tactics, Tactic)

    def test_get_pre_attack_tactics_by_tactic_id(self):
        tactic = self.api.get_pre_attack_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        expected = {tactic.id}

        #: Result.
        tactics = self.api.get_pre_attack_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        result = {t.id for t in tactics}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_pre_attack_tactics_by_technique_id(self):
        technique = self.api.get_pre_attack_object(object_types=['attack-pattern'])
        self.assertIsInstance(technique, PreAttackTechnique)

        #: Expected.
        tactics = self.api.get_pre_attack_tactics()
        expected = {t.id for t in tactics if t.kill_chain_phase_name in technique.kill_chain_phase_names}

        #: Result.
        a = self.api.get_pre_attack_tactics(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_pre_attack_tactics_by_related_techniques(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_pre_attack_tactics_by_group_id(self):
        relationships = self.get_pre_attack_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        group_id = next(r.src for r in relationships)

        #: Expected.
        tactics = self.api.get_pre_attack_tactics(technique_ids={r.dst for r in relationships if r.src == group_id})
        self.assert_is_non_empty_list_of_type(tactics, Tactic)
        expected = {t.id for t in tactics}

        #: Result.
        a = self.api.get_pre_attack_tactics(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, Tactic)

        b = self.api.get_pre_attack_tactics_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, Tactic)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_pre_attack_techniques(self):
        techniques = self.api.get_pre_attack_techniques()
        self.assert_is_non_empty_list_of_type(techniques, PreAttackTechnique)

    def test_get_pre_attack_techniques_by_tactic_id(self):
        tactic = self.api.get_pre_attack_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = [
            t for t in self.api.get_pre_attack_techniques() if tactic.kill_chain_phase_name in t.kill_chain_phase_names
        ]
        self.assert_is_non_empty_list_of_type(techniques, PreAttackTechnique)
        expected = {t.id for t in techniques}

        #: Result.
        a = self.api.get_pre_attack_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, PreAttackTechnique)

        b = self.api.get_pre_attack_techniques_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, PreAttackTechnique)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_pre_attack_techniques_by_technique_id(self):
        technique = self.api.get_pre_attack_object(object_types=['attack-pattern'])
        self.assertIsInstance(technique, PreAttackTechnique)

        #: Expected.
        expected = {technique.id}

        #: Result.
        techniques = self.api.get_pre_attack_techniques(technique_ids=[technique.id])
        self.assert_is_non_empty_list_of_type(techniques, PreAttackTechnique)
        result = {t.id for t in techniques}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_pre_attack_techniques_by_group_id(self):
        relationships = self.get_pre_attack_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        group_id = next(r.src for r in relationships)

        #: Expected.
        expected = {r.dst for r in relationships if r.src == group_id}

        #: Result.
        a = self.api.get_pre_attack_techniques(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(a, PreAttackTechnique)

        b = self.api.get_pre_attack_techniques_by_related_groups(group_ids=[group_id])
        self.assert_is_non_empty_list_of_type(b, PreAttackTechnique)

        self.assertEqual(a, b)
        result = {t.id for t in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_pre_attack_groups(self):
        groups = self.api.get_pre_attack_groups()
        self.assert_is_non_empty_list_of_type(groups, Group)

    def test_get_pre_attack_groups_by_tactic_id(self):
        tactic = self.api.get_pre_attack_object(object_types=['x-mitre-tactic'])
        self.assertIsInstance(tactic, Tactic)

        #: Expected.
        techniques = self.api.get_pre_attack_techniques(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(techniques, PreAttackTechnique)

        relationships = self.get_pre_attack_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
            target_object_ids=[t.id for t in techniques],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        expected = {r.src for r in relationships}

        #: Result.
        a = self.api.get_pre_attack_groups(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_pre_attack_groups_by_related_tactics(tactic_ids=[tactic.id])
        self.assert_is_non_empty_list_of_type(b, Group)

        self.assertEqual(a, b)
        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_pre_attack_groups_by_technique_id(self):
        relationships = self.get_pre_attack_relationships(
            source_object_types=['intrusion-set'],
            relationship_types=['uses'],
            target_object_types=['attack-pattern'],
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)
        technique_id = next(r.dst for r in relationships)

        #: Expected.
        expected = {r.src for r in relationships if r.dst == technique_id}

        #: Result.
        a = self.api.get_pre_attack_groups(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(a, Group)

        b = self.api.get_pre_attack_groups_by_related_techniques(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(b, Group)

        self.assertEqual(a, b)
        result = {g.id for g in a}

        #: Verify.
        self.assertEqual(expected, result)

    def test_get_pre_attack_groups_by_group_id(self):
        group = self.api.get_pre_attack_object(object_types=['intrusion-set'])
        self.assertIsInstance(group, Group)

        #: Expected.
        expected = {group.id}

        #: Result.
        groups = self.api.get_pre_attack_groups(group_ids=[group.id])
        self.assert_is_non_empty_list_of_type(groups, Group)
        result = {g.id for g in groups}

        #: Verify.
        self.assertEqual(expected, result)
