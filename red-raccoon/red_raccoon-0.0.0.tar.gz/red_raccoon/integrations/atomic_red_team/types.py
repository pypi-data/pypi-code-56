from typing import List, Union
from dataclasses import dataclass, field
from red_raccoon.integrations.atomic_red_team import DEFAULT_COMMAND_TIMEOUT, \
    DEFAULT_COMMAND_TIMEOUT_FOR_DEPENDENCY_RESOLUTION

from red_raccoon.platforms import WINDOWS, LINUX, MACOS, CURRENT_OS_TYPE
from red_raccoon.commands import DEFAULT_COMMAND_TYPE, ObservedProcess

import red_raccoon.platforms
import red_raccoon.commands
import red_raccoon.helpers
import hodgepodge.helpers
import logging
import time

logger = logging.getLogger(__name__)


def get_default_platforms():
    return [WINDOWS, LINUX, MACOS]


@dataclass(frozen=True)
class InputArgument:
    name: str
    type: str
    default_value: str
    description: str

    def is_string(self):
        return self.type.lower() == 'string'

    def is_path(self):
        return self.type.lower() == 'path'

    def is_url(self):
        return self.type.lower() == 'url'


@dataclass(frozen=True)
class Dependency:
    evaluation_command_template: str
    resolution_command_template: str
    description_template: str

    def get_description(self, input_arguments=None):
        return interpolate_arguments(self.description_template, input_arguments=input_arguments)

    def get_description_template(self):
        return self.description_template

    def get_evaluation_command(self, input_arguments=None):
        return interpolate_arguments(self.evaluation_command_template, input_arguments=input_arguments)

    def get_evaluation_command_template(self):
        return self.evaluation_command_template

    def get_resolution_command(self, input_arguments=None):
        return interpolate_arguments(self.resolution_command_template, input_arguments=input_arguments)

    def get_resolution_command_template(self):
        return self.resolution_command_template

    def get_commands(self, input_arguments=None):
        return [
            self.get_evaluation_command(input_arguments),
            self.get_resolution_command(input_arguments),
        ]

    def get_command_templates(self):
        return [
            self.get_evaluation_command_template(),
            self.get_resolution_command_template(),
        ]


@dataclass(frozen=True)
class TestCase:
    id: str
    name: str
    description: str

    #: How to execute the provided command, and cleanup command associated with this test case.
    command_template: str
    cleanup_command_template: Union[str, None] = None
    command_type: str = DEFAULT_COMMAND_TYPE
    command_timeout: Union[int, float] = DEFAULT_COMMAND_TIMEOUT
    command_timeout_for_dependency_resolution: Union[int, float] = DEFAULT_COMMAND_TIMEOUT_FOR_DEPENDENCY_RESOLUTION
    elevation_required: bool = True

    #: The set of input arguments, and default values associated with this test case.
    input_arguments: List[InputArgument] = field(default_factory=list)

    #: An optional set of dependencies that have been mapped to this test case.
    dependency_resolver_command_type: Union[str, None] = None
    dependencies: List[Dependency] = field(default_factory=list)

    #: The set of OS types, or platforms that this test case applies to.
    platforms: List[str] = field(default_factory=get_default_platforms)

    #: Other fields.
    auto_generated_guid: Union[str, None] = None    #: Auto-generated GUID provided by Red Canary.

    def applies_to_current_platform(self):
        return self.has_matching_platform([CURRENT_OS_TYPE])

    def has_matching_platform(self, platforms):
        return red_raccoon.platforms.has_matching_platform(self.platforms, platforms)

    def has_matching_name(self, names):
        return hodgepodge.helpers.string_matches_any_pattern(self.name, names)

    def execute(self, input_arguments=None):
        if not self.applies_to_current_platform():
            logger.warning("Not executing test case: %s - does not apply to current platform (found: %s, required: %s)",
                           self.name, CURRENT_OS_TYPE, '|'.join(self.platforms))
            return None

        start_timestamp = time.time()

        end_timestamp = time.time()

        return TestCaseResult(
            id=red_raccoon.helpers.get_random_blake2b_hash(),
            test_case_id=self.id,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            observed_processes=[],
        )

    def get_command_templates(self):
        templates = [
            self.command_template,
        ]
        if self.has_cleanup_command():
            templates.append(self.cleanup_command_template)
        return templates

    def get_commands(self, input_arguments=None):
        commands = [
            self.get_command(input_arguments),
        ]
        if self.has_cleanup_command():
            commands.append(self.get_cleanup_command(input_arguments))
        return commands

    def get_command(self, input_arguments=None):
        return interpolate_arguments(self.command_template, input_arguments=input_arguments)

    def get_cleanup_command(self, input_arguments=None):
        return interpolate_arguments(self.cleanup_command_template, input_arguments=input_arguments)

    def has_cleanup_command(self):
        return bool(self.cleanup_command_template)

    def has_dependencies(self):
        return bool(self.dependencies)

    def has_input_arguments(self):
        return bool(self.input_arguments)

    def get_input_arguments(self, input_arguments=None):
        if not self.input_arguments:
            args = {}
        else:
            args = dict([(arg.name, arg.default_value) for arg in self.input_arguments])
            if input_arguments:
                for name, value in input_arguments.items():
                    if name in args:
                        args[name] = value
        return args

    def __call__(self, **input_arguments):
        return self.execute(**input_arguments)


@dataclass(frozen=True)
class TestSuite:
    technique_id: str
    technique_name: str
    test_cases: List[TestCase]

    @property
    def name(self):
        return '{}: {}'.format(self.technique_id, self.technique_name)

    @property
    def platforms(self):
        platforms = set()
        for test_case in self.test_cases:
            platforms |= set(test_case.platforms)
        return sorted(platforms)

    def applies_to_current_platform(self):
        return any(test_case.applies_to_current_platform() for test_case in self.test_cases)

    def has_matching_platform(self, platforms):
        return any(test_case.has_matching_platform(platforms) for test_case in self.test_cases)

    def execute(self, input_arguments):
        if not self.applies_to_current_platform():
            logger.warning("Not executing test suite: %s - does not apply to current platform (found: %s, required: %s)",
                           self.name, CURRENT_OS_TYPE, '|'.join(self.platforms))
            return None

        start_timestamp = time.time()
        test_case_results = []
        for test_case in self.test_cases:
            if test_case.applies_to_current_platform():
                result = test_case(input_arguments=input_arguments)
                if result is not None:
                    test_case_results.append(result)

        end_timestamp = time.time()

        return TestSuiteResult(
            id=red_raccoon.helpers.get_random_blake2b_hash(),
            technique_id=self.technique_id,
            technique_name=self.technique_name,
            test_case_results=test_case_results,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )

    def __iter__(self):
        for test_case in self.test_cases:
            yield test_case

    def __len__(self):
        return len(self.test_cases)

    def __call__(self, input_arguments):
        return self.execute(input_arguments=input_arguments)


@dataclass(frozen=True)
class _Result:
    start_timestamp: float
    end_timestamp: float

    @property
    def duration(self):
        return self.end_timestamp - self.start_timestamp


@dataclass(frozen=True)
class TestCaseResult(_Result):
    id: str
    test_case_id: str
    observed_processes: List[ObservedProcess]

    @property
    def test_case_result_id(self):
        return self.id


@dataclass(frozen=True)
class TestSuiteResult(_Result):
    id: str
    technique_id: str
    technique_name: str
    test_case_results: List[TestCaseResult]


def interpolate_arguments(template, input_arguments):
    if not input_arguments:
        return template

    command = template
    for key, value in input_arguments.items():
        placeholder = "#{{{}}}".format(key)
        if placeholder in template:
            command = command.replace(placeholder, str(value))
    return command
