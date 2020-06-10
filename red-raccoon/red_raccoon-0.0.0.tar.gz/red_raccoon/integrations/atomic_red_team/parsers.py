from red_raccoon.platforms import WINDOWS, LINUX, MACOS
from red_raccoon.integrations.atomic_red_team import DEFAULT_COMMAND_TIMEOUT, \
    DEFAULT_COMMAND_TIMEOUT_FOR_DEPENDENCY_RESOLUTION, DEFAULT_ATOMIC_RED_TEAM_DIRECTORY

from red_raccoon.integrations.atomic_red_team.types import TestSuite, TestCase, InputArgument, Dependency

import hodgepodge.helpers
import hodgepodge.hashing
import hodgepodge.path
import logging
import pathlib
import os

logger = logging.getLogger(__name__)


DEFAULT_PLATFORMS = [WINDOWS, LINUX, MACOS]


def get_test_case_id(technique_id, technique_name, command_template, cleanup_command_template):
    commands = [
        command_template.strip()
    ]
    if cleanup_command_template:
        commands.append(cleanup_command_template.strip())

    data = '{}:{}:{}'.format(technique_id.strip(), technique_name.strip(), ', '.join(commands))
    return hodgepodge.hashing.get_blake2b(data)


def parse_test_suite(data, technique_name=None, atomic_red_team_directory=DEFAULT_ATOMIC_RED_TEAM_DIRECTORY,
                     command_timeout=DEFAULT_COMMAND_TIMEOUT,
                     command_timeout_for_dependency_resolution=DEFAULT_COMMAND_TIMEOUT_FOR_DEPENDENCY_RESOLUTION):

    technique_id = data['attack_technique']
    technique_name = technique_name or data['display_name']

    test_cases = []
    for test_case in data['atomic_tests']:
        test_case = parse_test_case(
            data=test_case,
            technique_id=technique_id,
            technique_name=technique_name,
            atomic_red_team_directory=atomic_red_team_directory,
            command_timeout=command_timeout,
            command_timeout_for_dependency_resolution=command_timeout_for_dependency_resolution,
        )
        if test_case:
            test_cases.append(test_case)

    if not test_cases:
        return

    return TestSuite(
        technique_id=technique_id,
        technique_name=technique_name,
        test_cases=test_cases,
    )


def parse_test_case(data, technique_id, technique_name, atomic_red_team_directory=DEFAULT_ATOMIC_RED_TEAM_DIRECTORY,
                    command_timeout=DEFAULT_COMMAND_TIMEOUT,
                    command_timeout_for_dependency_resolution=DEFAULT_COMMAND_TIMEOUT_FOR_DEPENDENCY_RESOLUTION):

    name = data['name'].strip()
    description = data['description'].replace('\n', ' ').strip()

    #: Ignore manually executed test cases.
    executor = data['executor']
    command_type = executor['name'].strip()
    if command_type == 'manual':
        logger.debug("Ignoring manually executed command: %s - %s", name, description)
        return

    #: Which commands to execute.
    command_template = executor['command'].strip()
    cleanup_command_template = executor.get('cleanup_command')
    if cleanup_command_template:
        cleanup_command_template = cleanup_command_template.strip()

    #: The default value of any input arguments.
    input_arguments = data.get('input_arguments')
    if input_arguments:
        input_arguments = parse_input_arguments(
            data=input_arguments,
            atomic_red_team_directory=atomic_red_team_directory,
        )

    #: Any dependencies which must be resolved prior to executing those commands.
    dependency_resolver_command_type = data.get('dependency_executor_name', command_type)
    dependencies = data.get('dependencies')
    if dependencies:
        dependencies = parse_dependencies(dependencies)

    #: How to execute those commands.
    elevation_required = executor.get('elevation_required', True)

    #: A deterministic, unique ID to assign to this test case.
    test_case_id = get_test_case_id(
        technique_id=technique_id,
        technique_name=technique_name,
        command_template=command_template,
        cleanup_command_template=cleanup_command_template,
    )

    #: Other fields.
    platforms = data.get('supported_platforms', DEFAULT_PLATFORMS)
    auto_generated_guid = data.get('auto_generated_guid')

    return TestCase(
        id=test_case_id,
        name=name,
        description=description,
        command_type=command_type,
        command_template=command_template,
        cleanup_command_template=cleanup_command_template,
        command_timeout=command_timeout,
        command_timeout_for_dependency_resolution=command_timeout_for_dependency_resolution,
        dependency_resolver_command_type=dependency_resolver_command_type,
        dependencies=dependencies,
        elevation_required=elevation_required,
        input_arguments=input_arguments,
        platforms=platforms,
        auto_generated_guid=auto_generated_guid,
    )


def parse_dependencies(dependencies):
    return [parse_dependency(dependency) for dependency in dependencies]


def parse_dependency(dependency):
    return Dependency(
        evaluation_command_template=dependency['prereq_command'].strip(),
        resolution_command_template=dependency['get_prereq_command'].strip(),
        description_template=dependency['description'].strip(),
    )


def parse_input_arguments(data, atomic_red_team_directory=DEFAULT_ATOMIC_RED_TEAM_DIRECTORY):
    input_arguments = []
    for name, arg in data.items():
        name = name.strip()
        argument_type = arg['type'].strip()
        default_value = str(arg['default']).strip()
        description = arg['description'].strip()

        #: If this is a file path.
        if argument_type.lower() == 'path':
            default_value = normalize_path(default_value)

            #: If this is a reference to the atomic-red-team directory.
            if atomic_red_team_directory and 'atomic' in default_value.lower():
                default_value = normalize_path_to_atomics_folder(
                    path=default_value,
                    atomic_red_team_directory=atomic_red_team_directory,
                )

        input_argument = InputArgument(
            name=name,
            type=argument_type,
            default_value=default_value,
            description=description,
        )
        input_arguments.append(input_argument)
    return input_arguments


def normalize_path(path):
    return path.replace('\\', '/')


def normalize_path_to_atomics_folder(path, atomic_red_team_directory=DEFAULT_ATOMIC_RED_TEAM_DIRECTORY):
    old = path = normalize_path(path)

    #: If the path begins with 'PathToAtomicsFolder' (e.g. 'PathToAtomicsFolder/T1502/bin/calc.dll').
    if hodgepodge.helpers.string_matches_pattern(path, 'PathToAtomicsFolder/*'):
        atomics_folder = pathlib.Path(atomic_red_team_directory) / 'atomics'
        path = pathlib.Path(path)
        path = (atomics_folder / path.relative_to('PathToAtomicsFolder/')).as_posix()

    #: If the path begins with '*/AtomicRedTeam/atomics/*'.
    elif hodgepodge.helpers.string_matches_pattern(path, '*/AtomicRedTeam/atomics/*'):
        atomic_red_team_directory = pathlib.Path(atomic_red_team_directory)
        path = pathlib.Path(path)
        path = (atomic_red_team_directory / os.path.join(*path.parts[path.parts.index('atomics'):])).as_posix()

    if old != path:
        new = path
        logger.debug("Patched reference to Atomic Red Team framework: %s -> %s", old, new)

    return path
