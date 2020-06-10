from hodgepodge.toolkits.filesystem.search.api import FilesystemSearch
from red_raccoon.integrations.mitre_attack_evaluations import DEFAULT_MITRE_ATTACK_EVALUATIONS_DIRECTORY, \
    DEFAULT_MITRE_ATTACK_EVALUATIONS_SCREENSHOTS_DIRECTORY

import red_raccoon.integrations.mitre_attack_evaluations.parsers as parsers
import hodgepodge.files
import hodgepodge.path
import hodgepodge.helpers
import hodgepodge.compression
import logging
import json
import zlib

logger = logging.getLogger(__name__)


class MitreAttackEvaluations:
    def __init__(self, evaluations_directory=DEFAULT_MITRE_ATTACK_EVALUATIONS_DIRECTORY,
                 screenshots_directory=DEFAULT_MITRE_ATTACK_EVALUATIONS_SCREENSHOTS_DIRECTORY, ignore_deprecated=True):

        self.evaluations_directory = hodgepodge.path.realpath(evaluations_directory)
        self.screenshots_directory = screenshots_directory

        self.ignore_deprecated = ignore_deprecated

    def get_evaluation_paths(self, vendor_names=None, group_names=None):
        directory = self.evaluations_directory
        vendor_names = hodgepodge.helpers.as_list(vendor_names, str)
        group_names = hodgepodge.helpers.as_list(group_names, str)

        logger.info("Searching for evaluations (directory: %s, vendors: %s, groups: %s)",
                    directory, vendor_names or None, group_names or None)

        #: Search for MITRE ATT&CK Evaluations matching the provided criteria (i.e. vendor, or group name).
        search = FilesystemSearch(self.evaluations_directory)
        search.add_filename_filter([
            '*_Results.json',
            '*_Results.json.gz',
            '*_Results_new.json',
            '*_Results_new.json.gz'
        ])

        #: Filter search results by vendor name (e.g. "FireEye", or "VMware").
        if vendor_names:
            patterns = ['*{}*'.format(vendor_name) for vendor_name in vendor_names]
            search.add_filename_filter(patterns)

        #: Filter search results by group name (e.g. "APT3" or "APT29").
        if group_names:
            patterns = ['*{}*'.format(group_name) for group_name in group_names]
            search.add_filename_filter(patterns)

        #: Optionally ignore deprecated evaluations (i.e. prefer '*_Results_new.json' vs '*_Results.json').
        if not self.ignore_deprecated:
            paths = sorted(search)
        else:
            paths_by_group_and_vendor = {}
            for file_object in search:
                path = file_object.path
                vendor, group = parsers.parse_vendor_and_group_from_path(path)
                if group and vendor:
                    previous_path = paths_by_group_and_vendor.get((group, vendor))
                    if previous_path is None or 'new' not in previous_path:
                        paths_by_group_and_vendor[(group, vendor)] = path
                    else:
                        logger.debug("Ignoring deprecated evaluation of a %s product with TTPs related to %s: %s",
                                     vendor, group, path)

            paths = sorted(paths_by_group_and_vendor.values())

        if paths:
            logger.info("Identified %d evaluations (directory: %s, vendors: %s, groups: %s)",
                        len(paths), directory, vendor_names or None, group_names or None)
        else:
            logger.error("No matching evaluations found (directory: %s, vendors: %s, groups: %s)",
                         directory, vendor_names or None, group_names or None)
        return paths

    def get_raw_evaluations(self, vendor_names=None, group_names=None):
        return list(self.iter_raw_evaluations(vendor_names=vendor_names, group_names=group_names))

    def iter_raw_evaluations(self, vendor_names=None, group_names=None):
        for path in self.get_evaluation_paths(vendor_names=vendor_names, group_names=group_names):
            data = read_evaluation(path)
            yield data

    def get_raw_evaluation_by_path(self, path):
        return read_evaluation(path)

    def get_evaluation(self, vendor_names=None, group_names=None):
        evaluations = self.iter_evaluations(vendor_names=vendor_names, group_names=group_names)
        return next(evaluations, None)

    def get_evaluations(self, vendor_names=None, group_names=None):
        return list(self.iter_evaluations(vendor_names=vendor_names, group_names=group_names))

    def iter_evaluations(self, vendor_names=None, group_names=None):
        vendor_names = hodgepodge.helpers.as_set(vendor_names, str)
        group_names = hodgepodge.helpers.as_set(group_names, str)

        for path in self.get_evaluation_paths(vendor_names=vendor_names, group_names=group_names):
            evaluation = self.get_evaluation_by_path(path)
            if evaluation:
                yield evaluation

    def get_evaluation_by_path(self, path):
        path = hodgepodge.path.realpath(path)
        vendor_name, group_name = parsers.parse_vendor_and_group_from_path(path)
        if not (vendor_name and group_name):
            logger.error("Failed to parse group and vendor from path - skipping: %s", path)
            return None

        data = read_evaluation(path)
        return parsers.parse_evaluation(
            data=data,
            vendor_name=vendor_name,
            group_name=group_name,
            screenshots_directory=self.screenshots_directory,
        )

    def get_vendor_names(self, vendor_names=None, group_names=None):
        vendors = set()
        for path in self.get_evaluation_paths(vendor_names=vendor_names, group_names=group_names):
            vendor, _ = parsers.parse_vendor_and_group_from_path(path)
            if vendor and vendor not in vendors:
                vendors.add(vendor)
        return sorted(vendors)

    def get_group_names(self, vendor_names=None, group_names=None):
        groups = set()
        for path in self.get_evaluation_paths(vendor_names=vendor_names, group_names=group_names):
            _, group = parsers.parse_vendor_and_group_from_path(path)
            if group and group not in groups:
                groups.add(group)
        return sorted(groups)


def read_evaluation(path):
    path = hodgepodge.path.realpath(path)
    with open(path, 'rb') as fp:
        data = fp.read()
        try:
            data = hodgepodge.compression.decompress_gzip(data)
        except zlib.error:
            pass

    data = json.loads(data)
    return data
