"""
The following module contains classes for representing objects from the Atomic Red Team framework.
"""

import copy
import logging
import time

from typing import List, Union, Dict
from dataclasses import dataclass, field

import hodgepodge.helpers
import red_raccoon.platforms

from hodgepodge.helpers import ensure_type
from red_raccoon.commands import CommandBlock, ExecutedCommand, SH, BASH, POWERSHELL, COMMAND_PROMPT

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TestSuiteConfiguration:
    technique_id: str

    #: Optional list fields.
    blacklisted_test_case_numbers: List[int] = field(default_factory=list)
    blacklisted_test_case_names: List[str] = field(default_factory=list)
    whitelisted_test_case_numbers: List[int] = field(default_factory=list)
    whitelisted_test_case_names: List[str] = field(default_factory=list)
    test_case_configurations: List["TestCaseConfiguration"] = field(default_factory=list)

    def is_whitelisted_test_case(self, test_case):
        test_case = ensure_type(test_case, TestCase)
        if self.is_blacklisted_test_case(test_case):
            return False

        if not (self.whitelisted_test_case_names or self.whitelisted_test_case_numbers):
            return True

        if self.whitelisted_test_case_numbers:
            return test_case.test_case_number in self.whitelisted_test_case_numbers

        if self.whitelisted_test_case_names:
            return \
                test_case.name in self.whitelisted_test_case_names or \
                test_case.full_name in self.whitelisted_test_case_names

        return False

    def is_blacklisted_test_case(self, test_case):
        test_case = ensure_type(test_case, TestCase)
        if not (self.blacklisted_test_case_names or self.blacklisted_test_case_numbers):
            return False

        if self.blacklisted_test_case_numbers:
            return test_case.test_case_number in self.blacklisted_test_case_numbers

        if self.blacklisted_test_case_names:
            return \
                test_case.name in self.blacklisted_test_case_names or \
                test_case.full_name in self.blacklisted_test_case_names

        return False


@dataclass(frozen=True)
class TestCaseConfiguration:
    technique_id: str

    #: Optional dictionary fields.
    data: Dict[str, object] = field(default_factory=dict)

    #: Optional numeric fields.
    test_case_number: int = None

    #: Optional string fields.
    test_case_name: str = None

    def __post_init__(self):
        if self.test_case_number is None and self.test_case_name is None:
            raise ValueError("A test case name or number must be provided")


@dataclass(frozen=True)
class CommandExecutor:
    command_template: str
    cleanup_command_template: Union[str, None]
    command_type: str
    command_timeout: Union[int, float]
    arguments: List["CommandExecutorArgument"]
    elevation_required: bool = False

    @property
    def file_dependencies(self):
        return list({argument.value for argument in self.arguments if argument.is_path()})

    @property
    def commands(self):
        if self.has_cleanup_command():
            return [self.command]
        return [self.command, self.cleanup_command]

    @property
    def command(self):
        return interpolate_command_arguments(self.command_template, self.arguments)

    @property
    def cleanup_command(self):
        return interpolate_command_arguments(self.cleanup_command_template, self.arguments)

    def is_command_prompt_command(self):
        return self.command_type == COMMAND_PROMPT

    def is_powershell_command(self):
        return self.command_type == POWERSHELL

    def is_bash_command(self):
        return self.command_type == BASH

    def is_sh_command(self):
        return self.command_type == SH

    def has_cleanup_command(self):
        return bool(self.cleanup_command_template)

    def has_file_dependencies(self):
        return bool(self.file_dependencies)

    def __call__(self):
        results = []
        for command in self.commands:
            command = CommandBlock(command=command, command_type=self.command_type, timeout=self.command_timeout)
            result = command()
            if result is not None:
                results.append(result)
        return results


@dataclass(frozen=True)
class CommandExecutorArgument:
    name: str
    type: str
    value: str
    description: str

    def is_url(self):
        return self.type.lower() == 'url'

    def is_path(self):
        return self.type.lower() == 'path'


@dataclass(eq=False, frozen=True)
class TestSuite:
    technique_id: str
    technique_name: str
    test_cases: List["TestCase"]

    @property
    def id(self):
        return self.test_suite_id

    @property
    def test_suite_id(self):
        return hodgepodge.helpers.sha1("{}:{}".format(self.technique_id, self.technique_name))

    @property
    def full_name(self):
        return self.name

    @property
    def name(self):
        return "{}: {}".format(self.technique_id, self.technique_name)

    @property
    def commands(self):
        return [c.command for c in self]

    @property
    def file_dependencies(self):
        file_dependencies = set()
        for test_case in self.test_cases:
            for file_dependency in test_case.file_dependencies:
                if file_dependency not in file_dependencies:
                    file_dependencies.add(file_dependency)
        return sorted(file_dependencies)

    @property
    def platforms(self):
        platforms = set()
        for test_case in self.test_cases:
            for platform in test_case.platforms:
                if platform not in platforms:
                    platforms.add(platform)
        return sorted(platforms)

    def has_matching_platform(self, platform):
        for test_case in self.test_cases:
            if red_raccoon.platforms.has_matching_platform(platform, test_case.platforms):
                return True
        return False

    def applies_to_windows(self):
        return any(map(lambda t: t.is_windows(), self.test_cases))

    def applies_to_linux(self):
        return any(map(lambda t: t.is_linux(), self.test_cases))

    def applies_to_macos(self):
        return any(map(lambda t: t.is_macos(), self.test_cases))

    def execute(self):
        logger.info("Executing test suite: %s (%d test cases)", self.name, len(self.test_cases))
        start_timestamp = time.time()
        test_cases = self.test_cases
        test_case_results = [c() for c in test_cases]
        end_timestamp = time.time()

        return TestSuiteResult(
            test_suite_result_id=hodgepodge.helpers.get_random_uuid(),
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            test_case_results=test_case_results,
            test_suite_id=self.test_suite_id,
        )

    def __call__(self):
        return self.execute()

    def __iter__(self):
        for test_case in self.test_cases:
            yield test_case

    def __len__(self):
        return len(self.test_cases)

    def __eq__(self, other):
        return isinstance(other, TestSuite) and (self.test_suite_id == other.test_suite_id)

    def __hash__(self):
        return hash(self.test_suite_id)


@dataclass(eq=False, frozen=True)
class TestCase:
    name: str
    description: str
    technique_id: str
    technique_name: str
    test_case_number: int
    platforms: List[str]
    command_executor: CommandExecutor

    @property
    def id(self):
        return self.test_case_id

    @property
    def test_case_id(self):
        return hodgepodge.helpers.sha1("{}:{}:{}:{}:{}".format(
            self.technique_id, self.technique_name, self.name, self.test_case_number, self.command_executor.command
        ))

    @property
    def test_suite_id(self):
        return hodgepodge.helpers.sha1("{}:{}".format(self.technique_id, self.technique_name))

    @property
    def full_name(self):
        return "{}: {} - {} (#{})".format(self.technique_id, self.technique_name, self.name, self.test_case_number)

    @property
    def file_dependencies(self):
        return self.command_executor.file_dependencies

    @property
    def elevation_required(self):
        return self.command_executor.elevation_required

    @property
    def command(self):
        return self.command_executor.command

    @property
    def cleanup_command(self):
        return self.command_executor.cleanup_command

    @property
    def command_type(self):
        return self.command_executor.command_type

    @property
    def command_template(self):
        return self.command_executor.command_template

    @property
    def command_timeout(self):
        return self.command_executor.command_timeout

    def has_matching_platform(self, platforms):
        return red_raccoon.platforms.has_matching_platform(platforms, self.platforms)

    def applies_to_windows(self):
        return red_raccoon.platforms.list_includes_windows(self.platforms)

    def applies_to_linux(self):
        return red_raccoon.platforms.list_includes_linux(self.platforms)

    def applies_to_macos(self):
        return red_raccoon.platforms.list_includes_macos(self.platforms)

    def applies_to_posix(self):
        return self.applies_to_linux() or self.applies_to_macos()

    def has_cleanup_command(self):
        return self.command_executor.has_cleanup_command()

    def has_file_dependencies(self):
        return self.command_executor.has_file_dependencies()

    def execute(self):
        logger.info("Executing test case: %s: %s", self.name, self.description)
        start_timestamp = time.time()
        executed_commands = self.command_executor()
        end_timestamp = time.time()

        return TestCaseResult(
            test_suite_id=self.test_suite_id,
            test_case_id=self.test_case_id,
            test_case_result_id=hodgepodge.helpers.get_random_uuid(),
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            executed_commands=executed_commands,
        )

    def __call__(self):
        return self.execute()

    def __eq__(self, other):
        return isinstance(other, TestCase) and self.test_case_id == other.test_case_id

    def __hash__(self):
        return hash(self.test_case_id)


@dataclass(eq=False, frozen=True)
class _Result:
    start_timestamp: float
    end_timestamp: float

    @property
    def duration(self):
        return self.end_timestamp - self.start_timestamp


@dataclass(frozen=True)
class TestSuiteResult(_Result):
    test_suite_id: str
    test_suite_result_id: str
    test_case_results: List["TestCaseResult"]

    @property
    def id(self):
        return self.test_suite_result_id

    def __iter__(self):
        for test_case_result in self.test_case_results:
            yield test_case_result

    def __len__(self):
        return len(self.test_case_results)


@dataclass(frozen=True)
class TestCaseResult(_Result):
    test_suite_id: str
    test_case_id: str
    test_case_result_id: str
    executed_commands: List[ExecutedCommand]

    @property
    def id(self):
        return self.test_case_result_id

    @property
    def exit_status(self):
        executed_commands = self.executed_commands
        if not executed_commands:
            return None
        return executed_commands[0].exit_status

    @property
    def stdout(self):
        executed_commands = self.executed_commands
        if executed_commands:
            return executed_commands[0].stdout
        return None

    @property
    def stderr(self):
        executed_commands = self.executed_commands
        if executed_commands:
            return executed_commands[0].stderr
        return None


def interpolate_command_arguments(template, arguments):
    command = ensure_type(template, str)
    template = copy.copy(template)
    for argument in arguments:
        placeholder = "#{{{}}}".format(argument.name)
        if placeholder not in template:
            logger.warning(
                "Placeholder of '%s' for %s argument named '%s' not found in template: %s",
                placeholder, argument.type, argument.name, template
            )
        else:
            command = command.replace(placeholder, str(argument.value))
    return command
