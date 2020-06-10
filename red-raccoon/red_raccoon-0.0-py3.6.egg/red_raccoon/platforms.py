"""
The following module contains functions for performing OS type normalization (e.g. "darwin" to
"macos", or "CentOS" to "linux").
"""

import itertools
import glob

from hodgepodge import CURRENT_OS_TYPE
from hodgepodge.helpers import ensure_type

import hodgepodge.helpers

#: List of platforms (included in the Atomic Red Team Framework, and different MITRE repositories).
WINDOWS = "windows"
LINUX = "linux"
MACOS = "macos"
AWS = "aws"
AZURE = "azure"
AZURE_AD = "azure ad"
GCP = "gcp"
ANDROID = "android"
IOS = "ios"
OFFICE_365 = "office 365"
SAAS = "saas"

#: A list of all recognized plaforms.
ALL_PLATFORMS = {
    WINDOWS, LINUX, MACOS, AWS, AZURE, AZURE_AD, GCP, ANDROID, IOS, OFFICE_365, SAAS
}

_PLATFORM_NORMALIZATION_LISTS = {
    WINDOWS: ["win", "microsoft windows"],
    MACOS: ["osx", "os x", "mac", "mac os x", "darwin"],
    OFFICE_365: ["o365", "office365", "office 365"]
}

_PLATFORM_ALIAS_LISTS = {
    LINUX: ["ubuntu", "centos", "rhel", "opensuse", "suse", "fedora", "debian"],
}

_PLATFORM_ALIAS_TO_PLATFORM = dict(itertools.chain.from_iterable(
    zip(aliases, itertools.repeat(platform)) for
    (platform, aliases) in _PLATFORM_ALIAS_LISTS.items()
))

_PLATFORM_TO_NORMALIZED_PLATFORM = dict(itertools.chain.from_iterable(
    zip(aliases, itertools.repeat(platform)) for
    (platform, aliases) in _PLATFORM_NORMALIZATION_LISTS.items()
))


def parse_platform(platform):
    """
    Translates the provided platform into a normalized representation of that platform (e.g. "O365"
    would be normalized to "office 365").

    :param platform: a string representing an OS type, or platform (e.g. "Azure AD", or "Linux").
    :return: a lowercase, and normalized representation of the provided platform.
    """
    if platform:
        platform = ensure_type(platform, str)
        platform = platform.lower()
        platform = _PLATFORM_TO_NORMALIZED_PLATFORM.get(platform, platform)
    return platform


def parse_platforms(platforms):
    """
    Translates the provided list of platforms into a normalized set of platforms.

    :param platforms: a sequence of OS types, and platforms.
    :return: a lowercase, and normalized set of platforms.
    """
    return {parse_platform(o) for o in hodgepodge.helpers.as_set(platforms)}


def is_unknown_platform(platform):
    """
    Checks whether or not the provided platform is unknown.

    :param platform: a string representing an OS type, or platform (e.g. "Azure AD", or "Linux").
    :return: True or False.
    """
    return has_matching_platform(platform, ALL_PLATFORMS) is False


def has_unknown_platform(platforms):
    """
    Checks whether or not any of the provided platforms are unknown.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    for platform in hodgepodge.helpers.as_set(platforms):
        if is_unknown_platform(platform):
            return True
    return False


def get_platform_aliases(platforms):
    """
    Identifies all of the aliases associated with the provided sequence of platforms.

    :param platforms: a sequence of OS types, and platforms.
    :return: a sequence of platform aliases.
    """
    aliases = hodgepodge.helpers.as_set(platforms)
    for platform in platforms:
        alias = _PLATFORM_ALIAS_TO_PLATFORM.get(platform)
        if alias and alias not in aliases:
            aliases.add(alias)
    return aliases


def has_matching_platform(platforms, patterns):
    """

    :param platforms: a sequence of OS types, and platforms.
    :param patterns:
    :return:
    """
    platforms = set(get_platform_aliases(parse_platforms(platforms)))
    patterns = set(get_platform_aliases(parse_platforms(patterns)))

    #: Optionally perform wildcard pattern matching.
    if any(glob.has_magic(pattern) for pattern in patterns):
        matches = _has_matching_platform_with_wildcard_match(platforms, patterns)
    else:
        matches = _has_matching_platform_with_direct_match(platforms, patterns)
    return matches


def _has_matching_platform_with_direct_match(platforms, patterns):
    return not set.isdisjoint(platforms, patterns)


def _has_matching_platform_with_wildcard_match(platforms, patterns):
    for platform in platforms:
        if hodgepodge.helpers.string_matches_any_pattern(platform, patterns, case_sensitive=False):
            return True
    return False


def list_includes_current_platform(platforms):
    """
    Checks whether or not the provided sequence of platforms includes the current OS type.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {CURRENT_OS_TYPE})


def list_includes_windows(platforms):
    """
    Checks whether or not the provided sequence of platforms includes Windows.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {WINDOWS})


def list_includes_linux(platforms):
    """
    Checks whether or not the provided sequence of platforms includes Linux.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {LINUX})


def list_includes_macos(platforms):
    """
    Checks whether or not the provided sequence of platforms includes macOS.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {MACOS})


def list_includes_posix(platforms):
    """
    Checks whether or not the provided sequence of platforms includes at least one POSIX OS type
    (e.g. macOS, or Linux).

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return list_includes_linux(platforms) or list_includes_macos(platforms)


def list_includes_aws(platforms):
    """
    Checks whether or not the provided sequence of platforms includes Amazon Web Services (AWS).

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {AWS})


def list_includes_azure(platforms):
    """
    Checks whether or not the provided sequence of platforms includes Azure.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {AZURE, AZURE_AD})


def list_includes_azure_ad(platforms):
    """
    Checks whether or not the provided sequence of platforms includes Azure AD.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {AZURE_AD})


def list_includes_gcp(platforms):
    """
    Checks whether or not the provided sequence of platforms includes the Google Cloud Platform
    (GCP).

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {GCP})


def list_includes_android(platforms):
    """
    Checks whether or not the provided sequence of platforms includes Android.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {ANDROID})


def list_includes_ios(platforms):
    """
    Checks whether or not the provided sequence of platforms includes iOS.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {IOS})


def list_includes_mobile_platform(platforms):
    """
    Checks whether or not the provided sequence of platforms includes a mobile OS type such as
    Android, or iOS.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return list_includes_android(platforms) or list_includes_ios(platforms)


def list_includes_office_365(platforms):
    """
    Checks whether or not the provided sequence of platforms includes O365.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {OFFICE_365})


def list_includes_software_as_a_service(platforms):
    """
    Checks whether or not the provided sequence of platforms includes a software as a service
    (SaaS) platform.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {OFFICE_365, SAAS})


def list_includes_infrastructure_as_a_service(platforms):
    """
    Checks whether or not the provided sequence of platforms includes an infrastructure as a service
    (IaaS) platform.

    :param platforms: a sequence of OS types, and platforms.
    :return: True or False.
    """
    return has_matching_platform(platforms, {AWS, GCP, AZURE})
