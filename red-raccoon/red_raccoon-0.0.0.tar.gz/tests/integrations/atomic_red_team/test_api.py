from red_raccoon.integrations.atomic_red_team.api import AtomicRedTeam
from red_raccoon.integrations.atomic_red_team.types import TestSuite, TestCase

import hodgepodge.helpers
import unittest
import os

ATOMIC_RED_TEAM_DIRECTORY = os.path.join(os.path.dirname(__file__), '../../test_data/atomic_red_team')


class AtomicRedTeamTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = AtomicRedTeam(
            atomic_red_team_directory=ATOMIC_RED_TEAM_DIRECTORY,
        )

    def assert_is_non_empty_list_of_type(self, rows, types):
        types = hodgepodge.helpers.as_tuple(types)
        self.assertIsInstance(rows, list)
        self.assertGreater(len(rows), 0)
        for row in rows:
            self.assertIsInstance(row, types)

    def test_atomic_red_team_directory(self):
        path = self.api.atomic_red_team_directory
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.path.isabs(path))

    def test_get_test_suite_paths(self):
        atomics_folder = os.path.join(self.api.atomic_red_team_directory, 'atomics')
        expected = [
            os.path.join(atomics_folder, 'T1002/T1002.yaml'),
            os.path.join(atomics_folder, 'T1003/T1003.yaml'),
            os.path.join(atomics_folder, 'T1004/T1004.yaml'),
            os.path.join(atomics_folder, 'T1005/T1005.yaml'),
            os.path.join(atomics_folder, 'T1007/T1007.yaml'),
            os.path.join(atomics_folder, 'T1009/T1009.yaml'),
        ]
        result = self.api.get_test_suite_paths()
        self.assertEqual(expected, result)

    def test_get_test_suites(self):
        test_suites = self.api.get_test_suites()
        self.assert_is_non_empty_list_of_type(test_suites, TestSuite)

        expected = {'T1002', 'T1003', 'T1004', 'T1005', 'T1007', 'T1009'}
        result = {test_suite.technique_id for test_suite in test_suites}
        self.assertEqual(expected, result)

    def test_get_test_suites_by_technique_id(self):
        test_suites = self.api.get_test_suites(technique_ids=['T1002'])
        self.assert_is_non_empty_list_of_type(test_suites, TestSuite)

        expected = {'T1002'}
        result = {test_suite.technique_id for test_suite in test_suites}
        self.assertEqual(expected, result)

    def test_get_test_suites_by_platform(self):
        for platforms, expected in [
            [['Windows'], {'T1002', 'T1007', 'T1003', 'T1004'}],
            [['windows'], {'T1002', 'T1007', 'T1003', 'T1004'}],
            [['Linux'], {'T1002', 'T1009'}],
            [['macOS'], {'T1009', 'T1005', 'T1002'}],
            [['darwin'], {'T1009', 'T1005', 'T1002'}],
        ]:
            with self.subTest(platforms):
                test_suites = self.api.get_test_suites(platforms=platforms)
                self.assert_is_non_empty_list_of_type(test_suites, TestSuite)

                result = {test_suite.technique_id for test_suite in test_suites}
                self.assertEqual(expected, result)

    def test_get_test_suite_by_technique_id(self):
        test_suite = self.api.get_test_suite_by_technique_id('T1002')
        self.assertIsInstance(test_suite, TestSuite)
        self.assertEqual('T1002', test_suite.technique_id)

    def test_get_test_suite_by_path(self):
        path = os.path.join(self.api.atomic_red_team_directory, 'atomics/T1002/T1002.yaml')
        test_suite = self.api.get_test_suite_by_path(path)
        self.assertIsInstance(test_suite, TestSuite)
        self.assertEqual('T1002', test_suite.technique_id)

    def test_get_test_cases(self):
        test_cases = self.api.get_test_cases()
        self.assert_is_non_empty_list_of_type(test_cases, TestCase)

    def test_get_test_cases_by_technique_id(self):
        test_cases = self.api.get_test_cases(technique_ids=['T1002'])
        self.assert_is_non_empty_list_of_type(test_cases, TestCase)

        expected = {
            'Compress Data for Exfiltration With PowerShell',
            'Compress Data for Exfiltration With Rar',
            'Data Compressed - nix - gzip Single File',
            'Data Compressed - nix - tar Folder or File',
            'Data Compressed - nix - zip'
        }
        result = {test_case.name for test_case in test_cases}
        self.assertEqual(expected, result)

    def test_get_test_cases_by_platform(self):
        test_cases = self.api.get_test_cases(technique_ids=['T1002'], platforms=['windows'])
        self.assert_is_non_empty_list_of_type(test_cases, TestCase)

        expected = {
            'Compress Data for Exfiltration With PowerShell',
            'Compress Data for Exfiltration With Rar',
        }
        result = {test_case.name for test_case in test_cases}
        self.assertEqual(expected, result)

    def test_get_test_cases_by_name(self):
        expected = {'Compress Data for Exfiltration With PowerShell'}
        for names in [
            ['Compress Data for Exfiltration With PowerShell'],
            ['compress data for exfiltration with powershell'],
            ['*powershell*'],
        ]:
            with self.subTest(names):
                test_cases = self.api.get_test_cases(technique_ids=['T1002'], platforms=['windows'], names=names)
                result = {test_case.name for test_case in test_cases}
                self.assertEqual(expected, result)

    def test_get_test_suite_data_by_path(self):
        path = os.path.join(self.api.atomic_red_team_directory, 'atomics/T1002/T1002.yaml')
        data = self.api.get_test_suite_data_by_path(path)
        self.assertIsInstance(data, dict)

    def test_get_test_suite_data_by_technique_id(self):
        data = self.api.get_test_suite_data_by_technique_id('T1002')
        self.assertIsInstance(data, dict)
