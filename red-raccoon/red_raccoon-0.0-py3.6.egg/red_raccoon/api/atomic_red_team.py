"""
The following module contains functionality for working with the Atomic Red Team framework.
"""

import logging
import yaml

import hodgepodge.helpers
import hodgepodge.path
import red_raccoon.atomic_red_team.parsers
import red_raccoon.platforms

from hodgepodge import UTF8, CURRENT_OS_TYPE
from hodgepodge.toolkits.filesystem.search import FilesystemSearch, FilenamePatternMatchingFunction
from red_raccoon.mitre_cti import MITRE_ATTACK_ENTERPRISE
from red_raccoon.api.mitre_cti import MitreCTI
from red_raccoon.atomic_red_team import DEFAULT_ATOMIC_RED_TEAM_DIRECTORY
from red_raccoon.atomic_red_team.types import TestSuiteConfiguration
from red_raccoon.commands import DEFAULT_COMMAND_TIMEOUT

logger = logging.getLogger(__name__)


class AtomicRedTeam:
    def __init__(self, atomic_red_team_directory=DEFAULT_ATOMIC_RED_TEAM_DIRECTORY,
                 command_timeout=DEFAULT_COMMAND_TIMEOUT,
                 prefer_offline_mitre_cti_repositories=True):

        #: Use the MITRE ATT&CK API to help discover, and select Atomic Red Team test cases.
        self.mitre_cti_api = MitreCTI(
            prefer_offline_repositories=prefer_offline_mitre_cti_repositories
        )
        self._mitre_attack_techniques_by_id = {}

        #: Atomic Red Team directory.
        self.atomic_red_team_directory = hodgepodge.path.realpath(atomic_red_team_directory)

        #: How long to wait for commands to finish executing.
        self.command_timeout = float(command_timeout or DEFAULT_COMMAND_TIMEOUT)

    def get_test_suite_paths(self, technique_ids=None, technique_names=None, tactic_ids=None,
                             tactic_names=None, group_ids=None, group_names=None,
                             mitigation_ids=None, mitigation_names=None, platforms=None):

        return sorted(self.iter_test_suite_paths(
            technique_ids=technique_ids,
            technique_names=technique_names,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            group_ids=group_ids,
            group_names=group_names,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
            platforms=platforms,
        ))

    def iter_test_suite_paths(self, technique_ids=None, technique_names=None, tactic_ids=None,
                              tactic_names=None, group_ids=None, group_names=None,
                              mitigation_ids=None, mitigation_names=None, platforms=None):

        atomic_red_team_directory = self.atomic_red_team_directory

        #: Lookup techniques.
        techniques = self.mitre_cti_api.get_mitre_attack_techniques(
            technique_ids=technique_ids,
            technique_names=technique_names,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            group_ids=group_ids,
            group_names=group_names,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
            platforms=platforms,
            collections=[MITRE_ATTACK_ENTERPRISE],
        )
        if not techniques:
            return

        #: Determine which paths to search for.
        patterns = set()
        for technique in techniques:
            external_id = technique.external_id
            pattern = "{}/atomics/{}/{}.yaml".format(
                atomic_red_team_directory, external_id, external_id
            )
            patterns.add(pattern)

            #: Keep track of techniques by ID.
            self._mitre_attack_techniques_by_id[external_id] = technique

        #: Search for those paths.
        logger.info(
            "Searching for test suites associated with %d techniques in: %s",
            len(techniques), atomic_red_team_directory
        )
        search = FilesystemSearch(roots=self.atomic_red_team_directory)
        for pattern in patterns:
            search.add_evaluator_function(FilenamePatternMatchingFunction(pattern=pattern))

        number_of_paths = 0
        for file_object in search:
            number_of_paths += 1
            yield file_object.path

        logger.info(
            "Identified %d Atomic Red Team test suites associated with %d techniques in: %s",
            number_of_paths, len(techniques), atomic_red_team_directory,
        )

    def get_test_suite_by_technique_id(self, technique_id, test_suite_configuration=None,
                                       platforms=None,
                                       ignore_test_cases_not_matching_current_platform=None,
                                       ignore_test_cases_with_file_dependencies=False):

        test_suite_configuration = test_suite_configuration or TestSuiteConfiguration(technique_id)
        logger.info(
            "Searching for test suite (technique ID: %s, platforms: %s)",
            technique_id, platforms
        )
        test_suites = self.iter_test_suites(
            technique_ids=[technique_id],
            platforms=platforms,
            test_suite_configurations=[test_suite_configuration],
            ignore_test_cases_not_matching_current_platform=ignore_test_cases_not_matching_current_platform,
            ignore_test_cases_with_file_dependencies=ignore_test_cases_with_file_dependencies,
        )
        matching_test_suite = None
        for test_suite in test_suites:
            if test_suite.technique_id == technique_id:
                matching_test_suite = test_suite
                break

        if matching_test_suite is None:
            logger.error(
                "No matching test suite (technique ID: %s, platforms: %s)",
                technique_id, platforms
            )
        return matching_test_suite

    def get_test_suites(self, technique_ids=None, technique_names=None, tactic_ids=None,
                        tactic_names=None, group_ids=None, group_names=None, mitigation_ids=None,
                        mitigation_names=None, platforms=None, test_suite_configurations=None,
                        ignore_test_cases_not_matching_current_platform=False,
                        ignore_test_cases_with_file_dependencies=False):

        test_suites = self.iter_test_suites(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            group_ids=group_ids,
            group_names=group_names,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
            platforms=platforms,
            test_suite_configurations=test_suite_configurations,
            ignore_test_cases_not_matching_current_platform=ignore_test_cases_not_matching_current_platform,
            ignore_test_cases_with_file_dependencies=ignore_test_cases_with_file_dependencies,
        )
        return sorted(test_suites, key=lambda t: t.technique_id)

    def iter_test_suites(self, technique_ids=None, technique_names=None, tactic_ids=None,
                         tactic_names=None, group_ids=None, group_names=None, mitigation_ids=None,
                         mitigation_names=None, platforms=None, test_suite_configurations=None,
                         ignore_test_cases_not_matching_current_platform=None,
                         ignore_test_cases_with_file_dependencies=False):

        #: Pack the list of test suite configurations into a dictionary.
        test_suite_configurations_by_technique_id = {}
        for config in hodgepodge.helpers.as_list(test_suite_configurations):
            test_suite_configurations_by_technique_id[config.technique_id] = config

        #: Update the set of platforms.
        platforms = hodgepodge.helpers.as_set(platforms)
        if ignore_test_cases_not_matching_current_platform:
            platforms |= {CURRENT_OS_TYPE}

        #: Lookup the path to different test suites.
        test_suite_paths = sorted(self.get_test_suite_paths(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            group_ids=group_ids,
            group_names=group_names,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
            platforms=platforms,
        ))

        #: Load each test suite.
        for path in test_suite_paths:
            with open(path, 'r', encoding=UTF8) as file_pointer:
                logger.debug("Loading test suite: %s", path)
                data = yaml.safe_load(file_pointer)

                #: Parse the test suite.
                technique_id = data['attack_technique']
                test_suite_configuration = test_suite_configurations_by_technique_id.get(technique_id)
                test_suite = red_raccoon.atomic_red_team.parsers.parse_test_suite(
                    data=data,
                    platforms=platforms,
                    test_suite_configuration=test_suite_configuration,
                    ignore_test_cases_with_file_dependencies=ignore_test_cases_with_file_dependencies,
                )
                if test_suite:
                    yield test_suite

    def get_test_cases(self, technique_ids=None, technique_names=None, tactic_ids=None,
                       tactic_names=None, group_ids=None, group_names=None, mitigation_ids=None,
                       mitigation_names=None, platforms=None, test_suite_configurations=None,
                       ignore_test_cases_not_matching_current_platform=None,
                       ignore_test_cases_with_file_dependencies=False):

        return list(self.iter_test_cases(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            group_ids=group_ids,
            group_names=group_names,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
            platforms=platforms,
            test_suite_configurations=test_suite_configurations,
            ignore_test_cases_not_matching_current_platform=ignore_test_cases_not_matching_current_platform,
            ignore_test_cases_with_file_dependencies=ignore_test_cases_with_file_dependencies,
        ))

    def iter_test_cases(self, technique_ids=None, technique_names=None, tactic_ids=None,
                        tactic_names=None, group_ids=None, group_names=None, mitigation_ids=None,
                        mitigation_names=None, platforms=None, test_suite_configurations=None,
                        ignore_test_cases_not_matching_current_platform=None,
                        ignore_test_cases_with_file_dependencies=False):

        test_suites = self.iter_test_suites(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            group_ids=group_ids,
            group_names=group_names,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
            platforms=platforms,
            test_suite_configurations=test_suite_configurations,
            ignore_test_cases_not_matching_current_platform=ignore_test_cases_not_matching_current_platform,
            ignore_test_cases_with_file_dependencies=ignore_test_cases_with_file_dependencies,
        )
        for test_suite in test_suites:
            for test_case in test_suite:
                yield test_case
