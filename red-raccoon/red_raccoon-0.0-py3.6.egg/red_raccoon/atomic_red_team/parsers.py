"""
The following module contains parsers for objects from the Atomic Red Team framework.
"""
import logging

from hodgepodge.helpers import ensure_type
from red_raccoon.commands import SUPPORTED_COMMAND_TYPES
from red_raccoon.atomic_red_team import DEFAULT_COMMAND_TIMEOUT
from red_raccoon.atomic_red_team.types import TestSuite, TestCase, CommandExecutor, \
    CommandExecutorArgument, TestSuiteConfiguration, TestCaseConfiguration

import hodgepodge.helpers
import red_raccoon.platforms

logger = logging.getLogger(__name__)


def parse_test_suite(data, technique_name=None, test_suite_configuration=None,
                     ignore_test_cases_with_file_dependencies=False, platforms=None):
    """
    Parse the provided test suite.

    :param data:
    :param technique_name: the name of the MITRE ATT&CK technique associated with this test suite.
    :param test_suite_configuration: an optional configuration to use when parsing this test suite.
    :param ignore_test_cases_with_file_dependencies: optionally ignore
    :param platforms: an optional sequence of required platforms.
    :return: a dataclass object.
    """
    data = ensure_type(data, dict)

    #: The Atomic Red Team technique name should be provided via the MITRE CTI API.
    technique_id = data['attack_technique']
    technique_name = technique_name or data['display_name'].strip()

    #: Read the test suite configuration.
    test_suite_configuration = test_suite_configuration or TestSuiteConfiguration(technique_id)

    #: Parse each of the test cases associated with this test suite.
    test_cases = []
    for test_case_number, test_case in enumerate(data['atomic_tests'], start=1):
        test_case = parse_test_case(
            data=test_case,
            test_case_number=test_case_number,
            technique_id=technique_id,
            technique_name=technique_name,
        )
        if test_case:

            #: Ignore blacklisted test cases.
            if test_suite_configuration.is_blacklisted_test_case(test_case):
                logger.info("Ignoring blacklisted test case: %s", test_case.full_name)

            #: Ignore non-whitelisted test cases.
            elif not test_suite_configuration.is_whitelisted_test_case(test_case):
                logger.info("Ignoring non-whitelisted test case: %s", test_case.full_name)

            #: Ignore test cases with non-matching platforms.
            elif platforms and not test_case.has_matching_platform(platforms):
                logger.info(
                    "Ignoring test case with non-matching platform: %s (expected: %s, found: %s)",
                    test_case.full_name, sorted(platforms), sorted(test_case.platforms)
                )

            #: Optionally ignore test cases with file dependencies.
            elif ignore_test_cases_with_file_dependencies and test_case.has_file_dependencies():
                logger.info("Ignoring test case with %d file dependencies: %s (%s)",
                            len(test_case.file_dependencies), test_case.full_name,
                            sorted(test_case.file_dependencies))
            else:
                test_cases.append(test_case)

    #: Only return non-empty test suites.
    if not test_cases:
        logger.debug("Ignoring empty test suite: %s: %s", technique_id, technique_name)
        return None

    data = {
        'technique_id': technique_id,
        'technique_name': technique_name,
        'test_cases': test_cases,
    }
    return hodgepodge.helpers.dict_to_dataclass(data=data, data_class=TestSuite)


def parse_test_case(data, test_case_number, technique_id, technique_name,
                    test_case_configuration=None):
    """
    Parse the provided test case.

    :param data:
    :param test_case_number: the test case number (0-indexed).
    :param technique_id: the MITRE ATT&CK technique ID associated with this test case.
    :param technique_name: the MITRE ATT&CK technique name associated with this test case.
    :param test_case_configuration: the configuration block to pass to the test case.
    :return: a dataclass object.
    """
    data = ensure_type(data, dict)

    #: Read the test case configuration.
    test_case_name = data['name'].strip()
    test_case_configuration = test_case_configuration or TestCaseConfiguration(
        technique_id=technique_id,
        test_case_name=test_case_name,
        test_case_number=test_case_number,
    )

    #: Parse the command executor block.
    command_executor = parse_command_executor(
        executor=data['executor'],
        input_arguments=data.get('input_arguments', {}),
        test_case_configuration=test_case_configuration,
    )
    if not command_executor:
        return None

    data = {
        'technique_id': technique_id,
        'technique_name': technique_name,
        'name': test_case_name,
        'description': data['description'].strip(),
        'test_case_number': test_case_number,
        'platforms': list(red_raccoon.platforms.parse_platforms(data['supported_platforms'])),
        'command_executor': command_executor,
    }
    return hodgepodge.helpers.dict_to_dataclass(data=data, data_class=TestCase)


def parse_command_executor(executor, input_arguments, test_case_configuration,
                           command_timeout=DEFAULT_COMMAND_TIMEOUT):
    """
    Parse the provided command executor.

    :param executor: a dictionary which defines which command(s) to execute.
    :param input_arguments: the set of input arguments to pass to the test case.
    :param test_case_configuration: the configuration block to pass to the test case.
    :param command_timeout: the timeout associated with the commands tied to this test case.
    :return: a dataclass object.
    """
    executor = ensure_type(executor, dict)
    input_arguments = ensure_type(input_arguments, dict)
    test_case_configuration = ensure_type(test_case_configuration, TestCaseConfiguration)

    #: Ignore any manually executed commands.
    command_type = executor['name'].strip()
    if command_type == 'manual':
        return None

    #: Ignore any test cases with unsupported command types.
    if command_type not in SUPPORTED_COMMAND_TYPES:
        logger.error(
            "Ignoring test case with unsupported command type '%s' - supported command types: %s",
            command_type, SUPPORTED_COMMAND_TYPES
        )
        return None

    #: Parse the set of command arguments.
    command_executor_arguments = []
    for name, values in input_arguments.items():
        command_executor_argument = CommandExecutorArgument(
            name=name,
            value=test_case_configuration.data.get(name, values['default']),
            type=values['type'].strip(),
            description=values['description'].strip(),
        )
        command_executor_arguments.append(command_executor_argument)

    command_template = executor['command'].strip()

    if 'cleanup_command' in executor:
        cleanup_command_template = executor['cleanup_command'].strip()
    else:
        cleanup_command_template = None

    data = {
        'command_template': command_template,
        'cleanup_command_template': cleanup_command_template,
        'command_type': command_type,
        'command_timeout': command_timeout,
        'arguments': command_executor_arguments,
        'elevation_required': executor.get('elevation_required', False),
    }
    return hodgepodge.helpers.dict_to_dataclass(data=data, data_class=CommandExecutor)
