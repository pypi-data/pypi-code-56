from red_raccoon.api.atomic_red_team import AtomicRedTeam
from red_raccoon.atomic_red_team.types import TestSuite, TestSuiteConfiguration

import itertools
import unittest


class AtomicRedTeamTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = AtomicRedTeam()

    def assert_is_non_empty_list_of_type(self, rows, expected_types):
        self.assertIsInstance(rows, list)
        self.assertGreater(len(rows), 0)
        for row in rows:
            self.assertIsInstance(row, expected_types)

    def test_get_test_suite_paths(self):
        paths = self.api.get_test_suite_paths()
        self.assert_is_non_empty_list_of_type(paths, str)

    def test_get_test_suite_paths_by_technique_id(self):
        paths = self.api.get_test_suite_paths(technique_ids=['T1003'])
        self.assert_is_non_empty_list_of_type(paths, str)

    def test_get_test_suite_by_technique_id(self):
        technique_id = "T1003"
        test_suite = self.api.get_test_suite_by_technique_id(technique_id)
        self.assertIsInstance(test_suite, TestSuite)
        self.assertEqual(technique_id, test_suite.technique_id)

    def test_get_test_suites(self):
        test_suites = self.api.get_test_suites()
        self.assert_is_non_empty_list_of_type(test_suites, TestSuite)

    def test_get_test_suites_by_technique_id(self):
        technique_id = "T1003"
        test_suites = self.api.get_test_suites(technique_ids=[technique_id])
        self.assert_is_non_empty_list_of_type(test_suites, TestSuite)
        self.assertEqual(len(test_suites), 1)

        for test_suite in test_suites:
            self.assertEqual(technique_id, test_suite.technique_id)

    def test_get_test_suites_with_blacklisted_test_case_number_filter(self):
        technique_id = 'T1003'
        test_suite_configuration = TestSuiteConfiguration(technique_id, blacklisted_test_case_numbers=[0, 2])
        test_suites = self.api.get_test_suites(
            technique_ids=[technique_id],
            test_suite_configurations=[test_suite_configuration],
        )
        self.assert_is_non_empty_list_of_type(test_suites, TestSuite)

        #: Ensure that there are at least 3 test cases.
        test_cases = list(itertools.chain.from_iterable(t.test_cases for t in test_suites))
        self.assertGreater(len(test_cases), 2)

        #: Ensure that the 1st and 3rd test case was ignored.
        result = set(t.test_case_id for t in test_cases)
        self.assertNotIn(0, result)
        self.assertNotIn(2, result)

    def test_get_test_suites_with_whitelisted_test_case_number_filter(self):
        technique_id = 'T1003'
        test_suite_configuration = TestSuiteConfiguration(technique_id, whitelisted_test_case_numbers=[1])
        test_suites = self.api.get_test_suites(
            technique_ids=[technique_id],
            test_suite_configurations=[test_suite_configuration],
        )
        self.assert_is_non_empty_list_of_type(test_suites, TestSuite)

        #: Ensure that only the whitelisted test case was returned.
        test_cases = list(itertools.chain.from_iterable(t.test_cases for t in test_suites))
        expected = {1}
        result = set(t.test_case_number for t in test_cases)
        self.assertEqual(expected, result)

    def test_get_test_suites_with_non_overlapping_blacklisted_and_whitelisted_test_case_number_filters(self):
        technique_id = 'T1003'
        test_suite_configuration = TestSuiteConfiguration(
            technique_id=technique_id,
            blacklisted_test_case_numbers=[0],
            whitelisted_test_case_numbers=[1],
        )
        test_suites = self.api.get_test_suites(
            technique_ids=[technique_id],
            test_suite_configurations=[test_suite_configuration],
        )
        self.assert_is_non_empty_list_of_type(test_suites, TestSuite)

        #: Ensure that only the whitelisted test case was returned.
        test_cases = list(itertools.chain.from_iterable(t.test_cases for t in test_suites))
        expected = {1}
        result = set(t.test_case_number for t in test_cases)
        self.assertEqual(expected, result)

    def test_get_test_suites_with_overlapping_blacklisted_and_whitelisted_test_case_number_filters(self):
        technique_id = 'T1003'
        test_suite_configuration = TestSuiteConfiguration(
            technique_id=technique_id,
            blacklisted_test_case_numbers=[0, 1],
            whitelisted_test_case_numbers=[1],
        )
        test_suites = self.api.get_test_suites(
            technique_ids=[technique_id],
            test_suite_configurations=[test_suite_configuration],
        )
        self.assertEqual(len(test_suites), 0)

    def test_get_test_suites_with_whitelisted_test_case_name_filter(self):
        technique_id = "T1003"
        test_suite_configuration = TestSuiteConfiguration(
            technique_id=technique_id,
            whitelisted_test_case_names=[
                "Registry dump of SAM, creds, and secrets",
                "Dump LSASS.exe Memory using ProcDump",
            ]
        )
        test_suites = self.api.get_test_suites(
            technique_ids=[technique_id],
            test_suite_configurations=[test_suite_configuration],
        )
        expected = set(test_suite_configuration.whitelisted_test_case_names)
        result = {t.name for t in itertools.chain.from_iterable(t.test_cases for t in test_suites)}
        self.assertEqual(expected, result)

    def test_get_test_suites_with_blacklisted_test_case_name_filter(self):
        technique_id = "T1003"
        test_suite_configuration = TestSuiteConfiguration(
            technique_id=technique_id,
            blacklisted_test_case_names=["Dump LSASS.exe Memory using ProcDump"]
        )
        test_suites = self.api.get_test_suites(
            technique_ids=[technique_id],
            test_suite_configurations=[test_suite_configuration],
        )
        test_case_names = {t.name for t in itertools.chain.from_iterable(t.test_cases for t in test_suites)}
        self.assertNotIn("Dump LSASS.exe Memory using ProcDump", test_case_names)

    def test_get_test_suites_with_platform_filter(self):
        pass

    def test_get_test_suites_with_custom_test_case_configurations(self):
        pass
