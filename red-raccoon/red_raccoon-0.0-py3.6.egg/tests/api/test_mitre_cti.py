from red_raccoon.api.mitre_cti import MitreCTI, TECHNIQUE, GROUP

from red_raccoon.mitre_cti.types import Matrix, Tactic, EnterpriseTechnique, MobileTechnique, \
    PreAttackTechnique, Group, Malware, Tool, Mitigation, Relationship, MarkingDefinition, Identity

import hodgepodge.helpers
import unittest
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#: MITRE ATT&CK Enterprise.
ENTERPRISE_TACTIC_ID = "TA0006"     #: Credential access.
ENTERPRISE_TECHNIQUE_ID = "T1003"   #: Credential dumping.
ENTERPRISE_GROUP_ID = "G0069"       #: MuddyWater.
ENTERPRISE_TOOL_ID = "S0002"        #: Mimikatz.
ENTERPRISE_MALWARE_ID = "S0223"     #: POWERSTATS.
ENTERPRISE_MITIGATION_ID = "M1026"  #: Privileged Account Management (PAM).

#: MITRE ATT&CK Mobile.
MOBILE_TACTIC_ID = "TA0032"         #: Discovery.
MOBILE_TECHNIQUE_ID = "T1430"       #: Location tracking.
MOBILE_GROUP_ID = "G0007"           #: APT28.
MOBILE_TOOL_ID = "S0408"            #: FlexiSpy.
MOBILE_MALWARE_ID = "S0314"         #: X-Agent for Android.
MOBILE_MITIGATION_ID = "M1005"      #: Application vetting.

#: MITRE ATT&CK Pre-ATT&CK.
PRE_ATTACK_TACTIC_ID = "TA0024"     #: Build capabilities.
PRE_ATTACK_TECHNIQUE_ID = "T1345"   #: Create custom payloads.
PRE_ATTACK_GROUP_ID = "G0003"       #: Cleaver.

#: Paths to offline copies of MITRE ATT&CK data.
_DIR = os.path.dirname(__file__)

#: Data from the MITRE ATT&CK Enterprise matrix related to G0069: MuddyWater.
ENTERPRISE_STIX_DATA_PATH = os.path.join(
    _DIR, '../test_data/stix/mitre/mitre_attack_enterprise.json'
)

#: Data from the MITRE ATT&CK Mobile matrix related to G0007: APT28.
MOBILE_STIX_DATA_PATH = os.path.join(
    _DIR, '../test_data/stix/mitre/mitre_attack_mobile.json'
)

#: Data from the MITRE ATT&CK Pre-ATT&CK matrix related to G0003: Cleaver.
PRE_ATTACK_STIX_DATA_PATH = os.path.join(
    _DIR, '../test_data/stix/mitre/mitre_attack_pre_attack.json'
)


class MitreCTITestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = MitreCTI(
            mitre_attack_enterprise_path=ENTERPRISE_STIX_DATA_PATH,
            mitre_attack_mobile_path=MOBILE_STIX_DATA_PATH,
            mitre_attack_pre_attack_path=PRE_ATTACK_STIX_DATA_PATH,
            ignore_revoked=False,
            ignore_deprecated=False,
            remove_html_tags=True,
            remove_citations=True,
            remove_markdown_links=True,
        )

    def setUp(self):
        self.assertTrue(os.path.isfile(ENTERPRISE_STIX_DATA_PATH))
        self.assertTrue(os.path.isfile(MOBILE_STIX_DATA_PATH))
        self.assertTrue(os.path.isfile(PRE_ATTACK_STIX_DATA_PATH))

    def assert_non_empty_collections_match(self, expected, result, types=None):
        expected = sorted(hodgepodge.helpers.as_list(expected))
        result = sorted(hodgepodge.helpers.as_list(result))

        #: Optionally perform type-checking.
        if types:
            self.assert_is_non_empty_list_of_type(expected, types)
            self.assert_is_non_empty_list_of_type(result, types)
        else:
            self.assert_is_non_empty_list(expected)
            self.assert_is_non_empty_list(result)

        self.assertEqual(expected, result)

    def assert_is_non_empty_list(self, rows):
        self.assertIsInstance(rows, list)
        self.assertGreater(len(rows), 0)

    def assert_is_non_empty_list_of_type(self, rows, types):
        types = hodgepodge.helpers.as_tuple(types)
        self.assertIsInstance(rows, list)
        self.assertGreater(len(rows), 0)
        for row in rows:
            self.assertIsInstance(row, types)

    def get_mitre_attack_objects(self, object_ids=None, object_types=None):
        return self.api.get_mitre_attack_objects(object_ids=object_ids, object_types=object_types)

    def test_get_mitre_attack_identities(self):
        rows = self.api.get_mitre_attack_identities()
        self.assert_is_non_empty_list_of_type(rows, Identity)

    def test_get_mitre_attack_marking_definitions(self):
        rows = self.api.get_mitre_attack_marking_definitions()
        self.assert_is_non_empty_list_of_type(rows, MarkingDefinition)

    def test_get_mitre_attack_matrices(self):
        rows = self.api.get_mitre_attack_matrices()
        self.assert_is_non_empty_list_of_type(rows, Matrix)

    def test_get_mitre_attack_directed_relationships(self):
        rows = self.api.get_mitre_attack_directed_relationships()
        self.assert_is_non_empty_list_of_type(rows, Relationship)

    def test_get_mitre_attack_directed_relationships_by_source_internal_id(self):
        group = self.api.get_mitre_attack_group_by_id(ENTERPRISE_GROUP_ID)
        self.assertIsInstance(group, Group)

        relationships = self.api.get_mitre_attack_directed_relationships(source_objects=[group.id])
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        for relationship in relationships:
            self.assertEqual(relationship.src, group.id)

    def test_get_mitre_attack_directed_relationships_by_source_external_id(self):
        group = self.api.get_mitre_attack_group_by_id(ENTERPRISE_GROUP_ID)
        self.assertIsInstance(group, Group)

        relationships = self.api.get_mitre_attack_directed_relationships(
            source_objects=[group.external_id]
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        for relationship in relationships:
            self.assertEqual(relationship.src, group.id)

    def test_get_mitre_attack_directed_relationships_by_source_object(self):
        group = self.api.get_mitre_attack_group_by_id(ENTERPRISE_GROUP_ID)
        self.assertIsInstance(group, Group)

        relationships = self.api.get_mitre_attack_directed_relationships(source_objects=[group])
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        for relationship in relationships:
            self.assertEqual(relationship.src, group.id)

    def test_get_mitre_attack_directed_relationships_by_source_object_type(self):
        relationships = self.api.get_mitre_attack_directed_relationships(
            source_object_types=[GROUP]
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        for relationship in relationships:
            self.assertEqual(relationship.src_type, GROUP)

    def test_get_mitre_attack_directed_relationships_by_target_internal_id(self):
        technique = self.api.get_mitre_attack_technique_by_id(ENTERPRISE_TECHNIQUE_ID)
        self.assertIsInstance(technique, EnterpriseTechnique)

        relationships = self.api.get_mitre_attack_directed_relationships(
            target_objects=[technique.id]
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        for relationship in relationships:
            self.assertEqual(relationship.dst, technique.id)

    def test_get_mitre_attack_directed_relationships_by_target_external_id(self):
        technique = self.api.get_mitre_attack_technique_by_id(ENTERPRISE_TECHNIQUE_ID)
        self.assertIsInstance(technique, EnterpriseTechnique)

        relationships = self.api.get_mitre_attack_directed_relationships(
            target_objects=[technique.external_id]
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        for relationship in relationships:
            self.assertEqual(relationship.dst, technique.id)

    def test_get_mitre_attack_directed_relationships_by_target_object(self):
        technique = self.api.get_mitre_attack_technique_by_id(ENTERPRISE_TECHNIQUE_ID)
        self.assertIsInstance(technique, EnterpriseTechnique)

        relationships = self.api.get_mitre_attack_directed_relationships(
            target_objects=[technique]
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        for relationship in relationships:
            self.assertEqual(relationship.dst, technique.id)

    def test_get_mitre_attack_directed_relationships_by_target_object_type(self):
        relationships = self.api.get_mitre_attack_directed_relationships(
            target_object_types=[TECHNIQUE]
        )
        self.assert_is_non_empty_list_of_type(relationships, Relationship)

        for relationship in relationships:
            self.assertEqual(relationship.dst_type, TECHNIQUE)

    def test_get_mitre_attack_tactic_by_id(self):
        for tactic_id in [ENTERPRISE_TACTIC_ID, MOBILE_TACTIC_ID, PRE_ATTACK_TACTIC_ID]:
            with self.subTest(tactic_id):
                row = self.api.get_mitre_attack_tactic_by_id(tactic_id)
                self.assertIsInstance(row, Tactic)

    def test_get_mitre_attack_technique_by_id(self):
        for technique_id in [ENTERPRISE_TECHNIQUE_ID, MOBILE_TECHNIQUE_ID, PRE_ATTACK_TECHNIQUE_ID]:
            with self.subTest(technique_id):
                row = self.api.get_mitre_attack_technique_by_id(technique_id)
                self.assertIsInstance(row, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

    def test_get_mitre_attack_group_by_id(self):
        for group_id in [ENTERPRISE_GROUP_ID, MOBILE_GROUP_ID, PRE_ATTACK_GROUP_ID]:
            with self.subTest(group_id):
                row = self.api.get_mitre_attack_group_by_id(group_id)
                self.assertIsInstance(row, Group)

    def test_get_mitre_attack_malware_by_id(self):
        for software_id in [ENTERPRISE_MALWARE_ID, MOBILE_MALWARE_ID]:
            with self.subTest(software_id):
                row = self.api.get_mitre_attack_malware_by_id(software_id)
                self.assertIsInstance(row, Malware)

    def test_get_mitre_attack_tool_by_id(self):
        for software_id in [ENTERPRISE_TOOL_ID, MOBILE_TOOL_ID]:
            with self.subTest(software_id):
                row = self.api.get_mitre_attack_tool_by_id(software_id)
                self.assertIsInstance(row, Tool)

    def test_get_mitre_attack_software_by_id(self):
        for software_id in [ENTERPRISE_MALWARE_ID, MOBILE_MALWARE_ID, MOBILE_TOOL_ID, MOBILE_MALWARE_ID]:
            with self.subTest(software_id):
                row = self.api.get_mitre_attack_software_by_id(software_id)
                self.assertIsInstance(row, (Malware, Tool))

    def test_get_mitre_attack_mitigation_by_id(self):
        for mitigation_id in [ENTERPRISE_MITIGATION_ID, MOBILE_MITIGATION_ID]:
            with self.subTest(mitigation_id):
                row = self.api.get_mitre_attack_mitigation_by_id(mitigation_id)
                self.assertIsInstance(row, Mitigation)

    def test_get_mitre_attack_tactics(self):
        rows = self.api.get_mitre_attack_tactics()
        self.assert_is_non_empty_list_of_type(rows, Tactic)

    def test_get_mitre_attack_tactics_by_tactic_id(self):
        for tactic_ids in [
            [ENTERPRISE_TACTIC_ID],
            [MOBILE_TACTIC_ID],
            [PRE_ATTACK_TACTIC_ID],
            [ENTERPRISE_TACTIC_ID, MOBILE_TACTIC_ID, PRE_ATTACK_TACTIC_ID]
        ]:
            with self.subTest('|'.join(tactic_ids)):
                rows = self.api.get_mitre_attack_tactics(tactic_ids=tactic_ids)
                self.assert_is_non_empty_list_of_type(rows, Tactic)

                expected = set(tactic_ids)
                result = {o.external_id for o in rows}
                self.assert_non_empty_collections_match(expected, result)

    def test_get_mitre_attack_tactics_by_technique_id(self):
        for technique_ids in [
            [ENTERPRISE_TECHNIQUE_ID],
            [MOBILE_TECHNIQUE_ID],
            [PRE_ATTACK_TECHNIQUE_ID],
            [ENTERPRISE_TECHNIQUE_ID, MOBILE_TECHNIQUE_ID, PRE_ATTACK_TECHNIQUE_ID]
        ]:
            with self.subTest('|'.join(technique_ids)):
                tactics = self.api.get_mitre_attack_tactics(technique_ids=technique_ids)
                self.assert_is_non_empty_list_of_type(tactics, Tactic)

    def test_get_mitre_attack_tactics_by_group_id(self):
        for group_ids in [
            [ENTERPRISE_GROUP_ID],
            [MOBILE_GROUP_ID],
            [PRE_ATTACK_GROUP_ID],
            [ENTERPRISE_GROUP_ID, MOBILE_GROUP_ID, PRE_ATTACK_GROUP_ID],
        ]:
            with self.subTest('|'.join(group_ids)):
                tactics = self.api.get_mitre_attack_tactics(group_ids=group_ids)
                self.assert_is_non_empty_list_of_type(tactics, Tactic)

    def test_get_mitre_attack_tactics_by_software_id(self):
        for software_ids in [
            [ENTERPRISE_MALWARE_ID, ENTERPRISE_TOOL_ID],
            [MOBILE_MALWARE_ID, MOBILE_TOOL_ID],
            [ENTERPRISE_MALWARE_ID, ENTERPRISE_TOOL_ID, MOBILE_MALWARE_ID, MOBILE_TOOL_ID],
        ]:
            with self.subTest('|'.join(software_ids)):
                tactics = self.api.get_mitre_attack_tactics(software_ids=software_ids)
                self.assert_is_non_empty_list_of_type(tactics, Tactic)

    def test_get_mitre_attack_tactics_by_mitigation_id(self):
        for mitigation_ids in [
            [ENTERPRISE_MITIGATION_ID],
            [MOBILE_MITIGATION_ID],
            [ENTERPRISE_MITIGATION_ID, MOBILE_MITIGATION_ID],
        ]:
            with self.subTest('|'.join(mitigation_ids)):
                tactics = self.api.get_mitre_attack_tactics(mitigation_ids=mitigation_ids)
                self.assert_is_non_empty_list_of_type(tactics, Tactic)

    def test_get_mitre_attack_techniques(self):
        rows = self.api.get_mitre_attack_techniques()
        self.assert_is_non_empty_list_of_type(rows, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

    def test_get_mitre_attack_techniques_by_tactic_id(self):
        for technique_ids in [
            [ENTERPRISE_TECHNIQUE_ID],
            [MOBILE_TECHNIQUE_ID],
            [PRE_ATTACK_TECHNIQUE_ID],
            [ENTERPRISE_TECHNIQUE_ID, MOBILE_TECHNIQUE_ID, PRE_ATTACK_TECHNIQUE_ID],
        ]:
            with self.subTest('|'.join(technique_ids)):
                tactics = self.api.get_mitre_attack_tactics(technique_ids=technique_ids)
                self.assert_is_non_empty_list_of_type(tactics, Tactic)

    def test_get_mitre_attack_techniques_by_technique_id(self):
        for technique_ids in [
            [ENTERPRISE_TECHNIQUE_ID],
            [MOBILE_TECHNIQUE_ID],
            [PRE_ATTACK_TECHNIQUE_ID],
            [ENTERPRISE_TECHNIQUE_ID, MOBILE_TECHNIQUE_ID, PRE_ATTACK_TECHNIQUE_ID],
        ]:
            with self.subTest('|'.join(technique_ids)):
                rows = self.api.get_mitre_attack_techniques(technique_ids=technique_ids)
                self.assert_is_non_empty_list_of_type(rows, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

                expected = set(technique_ids)
                result = {o.external_id for o in rows}
                self.assert_non_empty_collections_match(expected, result)

    def test_get_mitre_attack_techniques_by_group_id(self):
        for group_ids in [
            [ENTERPRISE_GROUP_ID],
            [MOBILE_GROUP_ID],
            [PRE_ATTACK_GROUP_ID],
            [ENTERPRISE_GROUP_ID, MOBILE_GROUP_ID, PRE_ATTACK_GROUP_ID],
        ]:
            with self.subTest('|'.join(group_ids)):
                techniques = self.api.get_mitre_attack_techniques(group_ids=group_ids)
                self.assert_is_non_empty_list_of_type(techniques, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

    def test_get_mitre_attack_techniques_by_software_id(self):
        for software_ids in [
            [ENTERPRISE_MALWARE_ID, ENTERPRISE_TOOL_ID],
            [MOBILE_MALWARE_ID, MOBILE_TOOL_ID],
            [ENTERPRISE_MALWARE_ID, ENTERPRISE_TOOL_ID, MOBILE_MALWARE_ID, MOBILE_TOOL_ID],
        ]:
            with self.subTest('|'.join(software_ids)):
                techniques = self.api.get_mitre_attack_techniques(software_ids=software_ids)
                self.assert_is_non_empty_list_of_type(techniques, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

    def test_get_mitre_attack_techniques_by_mitigation_id(self):
        for mitigation_ids in [
            [ENTERPRISE_MITIGATION_ID],
            [MOBILE_MITIGATION_ID],
            [ENTERPRISE_MITIGATION_ID, MOBILE_MITIGATION_ID],
        ]:
            with self.subTest('|'.join(mitigation_ids)):
                techniques = self.api.get_mitre_attack_techniques(mitigation_ids=mitigation_ids)
                self.assert_is_non_empty_list_of_type(techniques, (EnterpriseTechnique, MobileTechnique, PreAttackTechnique))

    def test_get_mitre_attack_groups(self):
        rows = self.api.get_mitre_attack_groups()
        self.assert_is_non_empty_list_of_type(rows, Group)

    def test_get_mitre_attack_groups_by_tactic_id(self):
        for tactic_ids in [
            [ENTERPRISE_TACTIC_ID],
            [MOBILE_TACTIC_ID],
            [PRE_ATTACK_TACTIC_ID],
            [ENTERPRISE_TACTIC_ID, MOBILE_TACTIC_ID, PRE_ATTACK_TACTIC_ID],
        ]:
            with self.subTest('|'.join(tactic_ids)):
                groups = self.api.get_mitre_attack_groups(tactic_ids=tactic_ids)
                self.assert_is_non_empty_list_of_type(groups, Group)

    def test_get_mitre_attack_groups_by_technique_id(self):
        for technique_ids in [
            [ENTERPRISE_TECHNIQUE_ID],
            [PRE_ATTACK_TECHNIQUE_ID],
            [ENTERPRISE_TECHNIQUE_ID, MOBILE_TECHNIQUE_ID, PRE_ATTACK_TECHNIQUE_ID],
        ]:
            with self.subTest('|'.join(technique_ids)):
                groups = self.api.get_mitre_attack_groups(technique_ids=technique_ids)
                self.assert_is_non_empty_list_of_type(groups, Group)

    def test_get_mitre_attack_groups_by_group_id(self):
        for group_ids in [
            [ENTERPRISE_GROUP_ID],
            [MOBILE_GROUP_ID],
            [PRE_ATTACK_GROUP_ID],
            [ENTERPRISE_GROUP_ID, MOBILE_GROUP_ID, PRE_ATTACK_GROUP_ID],
        ]:
            with self.subTest('|'.join(group_ids)):
                rows = self.api.get_mitre_attack_groups(group_ids=group_ids)
                self.assert_is_non_empty_list_of_type(rows, Group)

                expected = set(group_ids)
                result = {o.external_id for o in rows}
                self.assert_non_empty_collections_match(expected, result)

    def test_get_mitre_attack_groups_by_software_id(self):
        for software_ids in [
            [ENTERPRISE_MALWARE_ID],
            [MOBILE_MALWARE_ID],
            [ENTERPRISE_MALWARE_ID, MOBILE_MALWARE_ID]
        ]:
            with self.subTest('|'.join(software_ids)):
                groups = self.api.get_mitre_attack_groups(software_ids=software_ids)
                self.assert_is_non_empty_list_of_type(groups, Group)

    def test_get_mitre_attack_groups_by_mitigation_id(self):
        for mitigation_ids in [
            [ENTERPRISE_MITIGATION_ID],
        ]:
            with self.subTest('|'.join(mitigation_ids)):
                groups = self.api.get_mitre_attack_groups(mitigation_ids=mitigation_ids)
                self.assert_is_non_empty_list_of_type(groups, Group)

    def test_get_mitre_attack_malware(self):
        rows = self.api.get_mitre_attack_malware()
        self.assert_is_non_empty_list_of_type(rows, Malware)

    def test_get_mitre_attack_malware_by_tactic_id(self):
        for tactic_ids in [
            [ENTERPRISE_TACTIC_ID],
            [MOBILE_TACTIC_ID],
            [ENTERPRISE_TACTIC_ID, MOBILE_TACTIC_ID],
        ]:
            with self.subTest('|'.join(tactic_ids)):
                malware = self.api.get_mitre_attack_malware(tactic_ids=tactic_ids)
                self.assert_is_non_empty_list_of_type(malware, Malware)

    def test_get_mitre_attack_malware_by_technique_id(self):
        for technique_ids in [
            [ENTERPRISE_TECHNIQUE_ID],
            [MOBILE_TECHNIQUE_ID],
            [ENTERPRISE_TECHNIQUE_ID, MOBILE_TECHNIQUE_ID],
        ]:
            with self.subTest('|'.join(technique_ids)):
                malware = self.api.get_mitre_attack_malware(technique_ids=technique_ids)
                self.assert_is_non_empty_list_of_type(malware, Malware)

    def test_get_mitre_attack_malware_by_group_id(self):
        for group_ids in [
            [ENTERPRISE_GROUP_ID],
            [MOBILE_GROUP_ID],
            [ENTERPRISE_GROUP_ID, MOBILE_GROUP_ID],
        ]:
            with self.subTest('|'.join(group_ids)):
                malware = self.api.get_mitre_attack_malware(group_ids=ENTERPRISE_GROUP_ID)
                self.assert_is_non_empty_list_of_type(malware, Malware)

    def test_get_mitre_attack_malware_by_software_id(self):
        for software_ids in [
            [ENTERPRISE_MALWARE_ID],
            [MOBILE_MALWARE_ID],
            [ENTERPRISE_MALWARE_ID, MOBILE_MALWARE_ID]
        ]:
            with self.subTest('|'.join(software_ids)):
                rows = self.api.get_mitre_attack_malware(software_ids=software_ids)
                self.assert_is_non_empty_list_of_type(rows, Malware)

                expected = set(software_ids)
                result = {o.external_id for o in rows}
                self.assert_non_empty_collections_match(expected, result)

    def test_get_mitre_attack_malware_by_mitigation_id(self):
        for mitigation_ids in [
            [ENTERPRISE_MITIGATION_ID],
            [MOBILE_MITIGATION_ID],
            [ENTERPRISE_MITIGATION_ID, MOBILE_MITIGATION_ID]
        ]:
            with self.subTest('|'.join(mitigation_ids)):
                malware = self.api.get_mitre_attack_malware(mitigation_ids=mitigation_ids)
                self.assert_is_non_empty_list_of_type(malware, Malware)

    def test_get_mitre_attack_tools(self):
        rows = self.api.get_mitre_attack_tools()
        self.assert_is_non_empty_list_of_type(rows, Tool)

    def test_get_mitre_attack_tools_by_tactic_id(self):
        for tactic_ids in [
            [ENTERPRISE_TACTIC_ID],
            [MOBILE_TACTIC_ID],
            [ENTERPRISE_TACTIC_ID, MOBILE_TACTIC_ID],
        ]:
            with self.subTest('|'.join(tactic_ids)):
                tools = self.api.get_mitre_attack_tools(tactic_ids=tactic_ids)
                self.assert_is_non_empty_list_of_type(tools, Tool)

    def test_get_mitre_attack_tools_by_technique_id(self):
        for technique_ids in [
            [ENTERPRISE_TECHNIQUE_ID],
            [MOBILE_TECHNIQUE_ID],
            [ENTERPRISE_TECHNIQUE_ID, MOBILE_TECHNIQUE_ID],
        ]:
            with self.subTest('|'.join(technique_ids)):
                tools = self.api.get_mitre_attack_tools(technique_ids=technique_ids)
                self.assert_is_non_empty_list_of_type(tools, Tool)

    def test_get_mitre_attack_tools_by_group_id(self):
        for group_ids in [
            [ENTERPRISE_GROUP_ID],
            [MOBILE_GROUP_ID],
            [ENTERPRISE_GROUP_ID, MOBILE_GROUP_ID],
        ]:
            with self.subTest('|'.join(group_ids)):
                tools = self.api.get_mitre_attack_tools(group_ids=group_ids)
                self.assert_is_non_empty_list_of_type(tools, Tool)

    def test_get_mitre_attack_tools_by_software_id(self):
        for software_ids in [
            [ENTERPRISE_TOOL_ID],
            [MOBILE_TOOL_ID],
            [ENTERPRISE_TOOL_ID, MOBILE_TOOL_ID]
        ]:
            with self.subTest('|'.join(software_ids)):
                rows = self.api.get_mitre_attack_tools(software_ids=software_ids)
                self.assert_is_non_empty_list_of_type(rows, Tool)

                expected = set(software_ids)
                result = {o.external_id for o in rows}
                self.assert_non_empty_collections_match(expected, result)

    def test_get_mitre_attack_tools_by_mitigation_id(self):
        for mitigation_ids in [
            [ENTERPRISE_MITIGATION_ID],
            [MOBILE_MITIGATION_ID],
            [ENTERPRISE_MITIGATION_ID, MOBILE_MITIGATION_ID]
        ]:
            with self.subTest('|'.join(mitigation_ids)):
                tools = self.api.get_mitre_attack_tools(mitigation_ids=mitigation_ids)
                self.assert_is_non_empty_list_of_type(tools, Tool)

    def test_get_mitre_attack_software(self):
        rows = self.api.get_mitre_attack_software()
        self.assert_is_non_empty_list_of_type(rows, (Tool, Malware))

    def test_get_mitre_attack_software_by_tactic_id(self):
        for tactic_ids in [
            [ENTERPRISE_TACTIC_ID],
            [MOBILE_TACTIC_ID],
            [ENTERPRISE_TACTIC_ID],
        ]:
            with self.subTest('|'.join(tactic_ids)):
                software = self.api.get_mitre_attack_software(tactic_ids=tactic_ids)
                self.assert_is_non_empty_list_of_type(software, (Tool, Malware))

    def test_get_mitre_attack_software_by_technique_id(self):
        for technique_ids in [
            [ENTERPRISE_TECHNIQUE_ID],
            [MOBILE_TECHNIQUE_ID],
            [ENTERPRISE_TECHNIQUE_ID, MOBILE_TECHNIQUE_ID],
        ]:
            with self.subTest('|'.join(technique_ids)):
                software = self.api.get_mitre_attack_software(technique_ids=technique_ids)
                self.assert_is_non_empty_list_of_type(software, (Tool, Malware))

    def test_get_mitre_attack_software_by_group_id(self):
        for group_ids in [
            [ENTERPRISE_GROUP_ID],
            [MOBILE_GROUP_ID],
            [ENTERPRISE_GROUP_ID, MOBILE_GROUP_ID],
        ]:
            with self.subTest('|'.join(group_ids)):
                software = self.api.get_mitre_attack_software(group_ids=group_ids)
                self.assert_is_non_empty_list_of_type(software, (Tool, Malware))

    def test_get_mitre_attack_software_by_software_id(self):
        for software_ids in [
            [ENTERPRISE_MALWARE_ID],
            [ENTERPRISE_TOOL_ID],
            [MOBILE_MALWARE_ID],
            [MOBILE_TOOL_ID],
            [ENTERPRISE_MALWARE_ID, ENTERPRISE_TOOL_ID, MOBILE_MALWARE_ID, MOBILE_TOOL_ID]
        ]:
            with self.subTest('|'.join(software_ids)):
                rows = self.api.get_mitre_attack_software(software_ids=software_ids)
                self.assert_is_non_empty_list_of_type(rows, (Tool, Malware))

    def test_get_mitre_attack_software_by_mitigation_id(self):
        for mitigation_ids in [
            [ENTERPRISE_MITIGATION_ID],
            [MOBILE_MITIGATION_ID],
            [ENTERPRISE_MITIGATION_ID, MOBILE_MITIGATION_ID]
        ]:
            with self.subTest('|'.join(mitigation_ids)):
                software = self.api.get_mitre_attack_software(mitigation_ids=mitigation_ids)
                self.assert_is_non_empty_list_of_type(software, (Tool, Malware))

    def test_get_mitre_attack_mitigations(self):
        rows = self.api.get_mitre_attack_mitigations()
        self.assert_is_non_empty_list_of_type(rows, Mitigation)

    def test_get_mitre_attack_mitigations_by_tactic_id(self):
        for tactic_ids in [
            [ENTERPRISE_TACTIC_ID],
            [MOBILE_TACTIC_ID],
            [ENTERPRISE_TACTIC_ID, MOBILE_TACTIC_ID],
        ]:
            with self.subTest('|'.join(tactic_ids)):
                mitigations = self.api.get_mitre_attack_mitigations(tactic_ids=tactic_ids)
                self.assert_is_non_empty_list_of_type(mitigations, Mitigation)

    def test_get_mitre_attack_mitigations_by_technique_id(self):
        for technique_ids in [
            [ENTERPRISE_TECHNIQUE_ID],
            [MOBILE_TECHNIQUE_ID],
            [ENTERPRISE_TECHNIQUE_ID, MOBILE_TECHNIQUE_ID],
        ]:
            with self.subTest('|'.join(technique_ids)):
                mitigations = self.api.get_mitre_attack_mitigations(technique_ids=technique_ids)
                self.assert_is_non_empty_list_of_type(mitigations, Mitigation)

    def test_get_mitre_attack_mitigations_by_group_id(self):
        for group_ids in [
            [ENTERPRISE_GROUP_ID],
            [MOBILE_GROUP_ID],
            [PRE_ATTACK_GROUP_ID],
            [ENTERPRISE_GROUP_ID, MOBILE_GROUP_ID, PRE_ATTACK_GROUP_ID],
        ]:
            with self.subTest('|'.join(group_ids)):
                mitigations = self.api.get_mitre_attack_mitigations(group_ids=group_ids)
                self.assert_is_non_empty_list_of_type(mitigations, Mitigation)

    def test_get_mitre_attack_mitigations_by_software_id(self):
        for software_ids in [
            [ENTERPRISE_MALWARE_ID, ENTERPRISE_TOOL_ID],
            [MOBILE_MALWARE_ID, MOBILE_TOOL_ID],
            [ENTERPRISE_MALWARE_ID, ENTERPRISE_TOOL_ID, MOBILE_MALWARE_ID, MOBILE_TOOL_ID]
        ]:
            with self.subTest('|'.join(software_ids)):
                mitigations = self.api.get_mitre_attack_mitigations(software_ids=software_ids)
                self.assert_is_non_empty_list_of_type(mitigations, Mitigation)

    def test_get_mitre_attack_mitigations_by_mitigation_id(self):
        for mitigation_id in [
            [ENTERPRISE_MITIGATION_ID],
            [MOBILE_MITIGATION_ID],
            [ENTERPRISE_MITIGATION_ID, MOBILE_MITIGATION_ID]
        ]:
            with self.subTest('|'.join(mitigation_id)):
                rows = self.api.get_mitre_attack_mitigations(mitigation_ids=mitigation_id)
                self.assert_is_non_empty_list_of_type(rows, Mitigation)

                expected = set(mitigation_id)
                result = {o.external_id for o in rows}
                self.assert_non_empty_collections_match(expected, result)
