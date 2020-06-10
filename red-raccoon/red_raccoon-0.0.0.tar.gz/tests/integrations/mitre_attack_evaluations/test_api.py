from red_raccoon.integrations.mitre_attack_evaluations.api import MitreAttackEvaluations
from red_raccoon.integrations.mitre_attack_evaluations.types import Evaluation

import unittest
import os


EVALUATIONS_DIRECTORY = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../../test_data/mitre/attack_evaluations"
))


class MitreAttackEvaluationsTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = MitreAttackEvaluations(evaluations_directory=EVALUATIONS_DIRECTORY)

    def assert_is_non_empty_list_of_type(self, rows, expected_types):
        self.assertGreater(len(rows), 0)
        for row in rows:
            self.assertIsInstance(row, expected_types)

    def test_get_evaluation_paths(self):
        paths = self.api.get_evaluation_paths()
        self.assert_is_non_empty_list_of_type(paths, str)
        for path in paths:
            self.assertTrue(os.path.isfile(path))

    def test_get_evaluation_paths_by_vendor_name(self):
        paths = self.api.get_evaluation_paths(vendor_names=['FireEye'])
        self.assert_is_non_empty_list_of_type(paths, str)
        for path in paths:
            self.assertIn('FireEye', path)
            self.assertTrue(os.path.isfile(path))

    def test_get_evaluation_paths_by_group_name(self):
        paths = self.api.get_evaluation_paths(group_names=['APT29'])
        self.assert_is_non_empty_list_of_type(paths, str)
        for path in paths:
            self.assertIn('APT29', path)
            self.assertTrue(os.path.isfile(path))

    def test_get_evaluation_by_path(self):
        path = next(iter(self.api.get_evaluation_paths(vendor_names=['FireEye'], group_names=['APT3'])))
        self.assertTrue(os.path.isfile(path))

        evaluation = self.api.get_evaluation_by_path(path)
        self.assertIsInstance(evaluation, Evaluation)

    def test_get_evaluation_by_path_raises_filenotfounderror_if_file_not_found(self):
        path = 'ImaginaryVendor.1.ImaginaryActor.1_Results.json'
        with self.assertRaises(FileNotFoundError):
            self.api.get_evaluation_by_path(path)

    def test_get_evaluation(self):
        evaluation = self.api.get_evaluation()
        self.assertIsInstance(evaluation, Evaluation)

    def test_get_evaluation_by_vendor_name(self):
        evaluation = self.api.get_evaluation(vendor_names=['FireEye'])
        self.assertIsInstance(evaluation, Evaluation)

        expected = 'FireEye'
        result = evaluation.vendor
        self.assertEqual(expected, result)

    def test_get_evaluation_by_group_name(self):
        evaluation = self.api.get_evaluation(group_names=['APT29'])
        self.assertIsInstance(evaluation, Evaluation)

        expected = 'APT29'
        result = evaluation.group
        self.assertEqual(expected, result)

    def test_get_evaluations(self):
        evaluations = self.api.get_evaluations()
        self.assert_is_non_empty_list_of_type(evaluations, Evaluation)

    def test_get_evaluations_by_vendor_name(self):
        evaluations = self.api.get_evaluations(vendor_names=['fireeye'])
        self.assert_is_non_empty_list_of_type(evaluations, Evaluation)

        expected = {"FireEye"}
        result = {evaluation.vendor for evaluation in evaluations}
        self.assertEqual(expected, result)

    def test_get_evaluations_by_group_name(self):
        evaluations = self.api.get_evaluations(group_names=['APT3'])
        self.assert_is_non_empty_list_of_type(evaluations, Evaluation)

        expected = {"APT3"}
        result = {evaluation.group_name for evaluation in evaluations}
        self.assertEqual(expected, result)

    def test_get_vendor_names(self):
        expected = {'FireEye'}
        result = set(self.api.get_vendor_names())
        self.assertEqual(expected, result)

    def test_get_vendor_names_by_vendor_name(self):
        expected = {'FireEye'}
        result = set(self.api.get_vendor_names(vendor_names=['FireEye']))
        self.assertEqual(expected, result)

    def test_get_vendor_names_by_invalid_vendor_name(self):
        expected = []
        result = self.api.get_vendor_names(vendor_names=['ImaginaryVendor'])
        self.assertEqual(expected, result)

    def test_get_vendor_names_by_group_name(self):
        expected = {'FireEye'}
        result = set(self.api.get_vendor_names(group_names=['APT3']))
        self.assertEqual(expected, result)

    def test_get_vendor_names_by_invalid_group_name(self):
        expected = []
        result = self.api.get_vendor_names(group_names=['ImaginaryGroup'])
        self.assertEqual(expected, result)

    def test_get_group_names(self):
        expected = {'APT3', 'APT29'}
        result = set(self.api.get_group_names())
        self.assertEqual(expected, result)

    def test_get_group_names_by_vendor_name(self):
        expected = {'APT3', 'APT29'}
        result = set(self.api.get_group_names(vendor_names=['FireEye']))
        self.assertEqual(expected, result)

    def test_get_group_names_by_invalid_vendor_name(self):
        expected = []
        result = self.api.get_group_names(vendor_names=['ImaginaryVendor'])
        self.assertEqual(expected, result)

    def test_get_group_names_by_group_name(self):
        expected = {'APT3'}
        result = set(self.api.get_group_names(group_names=['APT3']))
        self.assertEqual(expected, result)

    def test_get_group_names_by_invalid_group_name(self):
        expected = []
        result = self.api.get_group_names(group_names=['ImaginaryGroup'])
        self.assertEqual(expected, result)
