from red_raccoon.atomic_red_team.types import TestSuite, TestCase

import red_raccoon.atomic_red_team.parsers
import unittest
import copy

TEST_CASE_A_1 = {
    'name': 'Compress Data for Exfiltration With PowerShell',
    'description': '...',
    'supported_platforms': ['windows'],
    'input_arguments': {
        'input_file': {
            'description': '...',
            'type': 'Path',
            'default': 'C:\\*',
        }
    },
    'executor': {
        'name': 'powershell',
        'elevation_required': False,
        'command': 'dir #{input_file} -Recurse | Compress-Archive -DestinationPath #{output_file}\n'
    }
}

TEST_CASE_A_2 = {
    'name': 'Data Compressed - nix - gzip Single File',
    'description': '...',
    'supported_platforms': ['linux', 'macos'],
    'input_arguments': {
        'input_file': {
            'description': 'Path that should be compressed',
            'type': 'Path',
            'default': '/tmp/victim-gzip.txt'
        }
    },
    'executor': {
        'name': 'sh',
        'elevation_required': False,
        'command': 'gzip -f #{input_file}\n',
    }
}

TEST_SUITE_A = {
    'attack_technique': 'T1002',
    'display_name': 'Data Compressed',
    'atomic_tests': [
        TEST_CASE_A_1,
        TEST_CASE_A_2,
    ]
}

TEST_CASE_B_1 = {
    'name': 'Shutdown System - Windows',
    'description': '...',
    'supported_platforms': ['windows'],
    'input_arguments': {
        'timeout': {
            'description': 'Timeout period before shutdown (seconds)',
            'type': 'string', 'default': 1
        }
    },
    'executor': {
        'name': 'command_prompt',
        'elevation_required': True,
        'command': 'shutdown /s /t #{timeout}\n'
    }
}

TEST_CASE_B_2 = {
    'name': 'Restart System - Windows',
    'description': '...',
    'supported_platforms': ['windows'],
    'input_arguments': {
        'timeout': {
            'description': 'Timeout period before restart (seconds)',
            'type': 'string',
            'default': 1,
        }
    },
    'executor': {
        'name': 'command_prompt',
        'elevation_required': True,
        'command': 'shutdown /r /t #{timeout}\n'
    }
}

TEST_SUITE_B = {
    'attack_technique': 'T1529',
    'display_name': 'System Shutdown/Reboot',
    'atomic_tests': [
        TEST_CASE_B_1,
        TEST_CASE_B_2,
    ]
}


class TestSuiteTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.atomic_red_team.parsers.parse_test_suite(TEST_SUITE_A)
        cls.b = red_raccoon.atomic_red_team.parsers.parse_test_suite(TEST_SUITE_B)

    def setUp(self):
        self.assertIsInstance(self.a, TestSuite)
        self.assertIsInstance(self.b, TestSuite)

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


class TestCaseTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = red_raccoon.atomic_red_team.parsers.parse_test_case(
            data=TEST_CASE_A_1,
            test_case_number=0,
            technique_id=TEST_SUITE_A['attack_technique'],
            technique_name=TEST_SUITE_A['display_name'],
        )
        cls.b = red_raccoon.atomic_red_team.parsers.parse_test_case(
            data=TEST_CASE_A_2,
            test_case_number=1,
            technique_id=TEST_SUITE_A['attack_technique'],
            technique_name=TEST_SUITE_A['display_name'],
        )

    def setUp(self):
        self.assertIsInstance(self.a, TestCase)
        self.assertIsInstance(self.b, TestCase)

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
