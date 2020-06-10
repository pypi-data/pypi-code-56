import logging
import yaml
import os

import hodgepodge.helpers
import hodgepodge.files
import hodgepodge.path
import red_raccoon.integrations.atomic_red_team.parsers as parsers

from hodgepodge import UTF8
from hodgepodge.helpers import ensure_type
from hodgepodge.toolkits.filesystem.search.api import FilesystemSearch
from red_raccoon.integrations.mitre_attack import DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_PATH, \
    DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_URL

from red_raccoon.integrations.mitre_attack.api import MitreAttack
from red_raccoon.integrations.atomic_red_team import DEFAULT_ATOMIC_RED_TEAM_DIRECTORY
from red_raccoon.commands import DEFAULT_COMMAND_TIMEOUT

logger = logging.getLogger(__name__)


class AtomicRedTeam:
    def __init__(self, atomic_red_team_directory=DEFAULT_ATOMIC_RED_TEAM_DIRECTORY,
                 command_timeout=DEFAULT_COMMAND_TIMEOUT, ignore_tests_with_file_dependencies=False,
                 mitre_attack_enterprise_stix_data=None,
                 mitre_attack_enterprise_stix_data_path=DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_PATH,
                 mitre_attack_enterprise_stix_data_url=DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_URL):

        #: Use the MITRE ATT&CK API to help discover and select Atomic Red Team test cases.
        self.mitre_attack_api = MitreAttack(
            enterprise_stix_data=mitre_attack_enterprise_stix_data,
            enterprise_stix_data_path=mitre_attack_enterprise_stix_data_path,
            enterprise_stix_data_url=mitre_attack_enterprise_stix_data_url,
        )

        #: The path to the 'atomic-red-team' repository.
        self.atomic_red_team_directory = hodgepodge.path.realpath(atomic_red_team_directory)

        #: Whether or not to ignore test cases which depend on external files/directories (e.g. "PathToAtomicsFolder").
        self._ignore_tests_with_file_dependencies = ensure_type(ignore_tests_with_file_dependencies, bool)

        #: How long to wait for commands to finish executing before forcefully terminating those commands.
        self._command_timeout = float(command_timeout or DEFAULT_COMMAND_TIMEOUT)

    def get_test_suite_paths(self, technique_ids=None):
        if technique_ids:
            patterns = set()
            for technique_id in hodgepodge.helpers.as_set(technique_ids, str):
                pattern = '*/{}/{}.yaml'.format(technique_id, technique_id)
                patterns.add(pattern)
        else:
            patterns = {"*/T*/T*.yaml"}

        search = FilesystemSearch(os.path.join(self.atomic_red_team_directory, 'atomics'))
        search.add_filename_filter(patterns)
        return sorted([file_object.path for file_object in search])

    def get_test_suites(self, technique_ids=None, platforms=None):
        return list(self.iter_test_suites(
            technique_ids=technique_ids,
            platforms=platforms,
        ))

    def iter_test_suites(self, technique_ids=None, platforms=None):
        platforms = hodgepodge.helpers.as_set(platforms, str)

        paths = self.get_test_suite_paths(technique_ids=technique_ids)
        for path in paths:
            test_suite = self.get_test_suite_by_path(path)
            if test_suite:

                #: Filter test suites by platform.
                if platforms and not test_suite.has_matching_platform(platforms):
                    continue

                yield test_suite

    def get_test_suite_by_technique_id(self, technique_id):
        test_suites = self.iter_test_suites(technique_ids=[technique_id])
        return next(iter(test_suites), None)

    def get_test_suite_by_path(self, path):
        data = self.get_test_suite_data_by_path(path)
        return parsers.parse_test_suite(data=data, atomic_red_team_directory=self.atomic_red_team_directory)

    def get_test_suite_data_by_technique_id(self, technique_id):
        path = next(iter(self.get_test_suite_paths(technique_ids=[technique_id])), None)
        if path:
            return self.get_test_suite_data_by_path(path)

    def get_test_suite_data_by_path(self, path):
        path = hodgepodge.path.realpath(path)
        with open(path, 'r', encoding=UTF8) as file_pointer:
            return yaml.safe_load(file_pointer)

    def get_test_cases(self, technique_ids=None, platforms=None, names=None):
        return list(self.iter_test_cases(technique_ids=technique_ids, platforms=platforms, names=names))

    def iter_test_cases(self, technique_ids=None, platforms=None, names=None):
        platforms = hodgepodge.helpers.as_set(platforms, str)
        names = hodgepodge.helpers.as_set(names, str)

        for test_suite in self.iter_test_suites(technique_ids=technique_ids, platforms=platforms):
            for test_case in test_suite:

                #: Filter test cases by platform.
                if platforms and not test_case.has_matching_platform(platforms):
                    continue

                #: Filter test cases by name.
                if names and not test_case.has_matching_name(names):
                    continue

                yield test_case
