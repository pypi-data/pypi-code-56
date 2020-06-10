"""
This module contains functions for parsing STIX 2.x objects.
"""

import json
import logging

import stix2.utils

from stix2.core import _STIXBase
from hodgepodge.helpers import ensure_type

import hodgepodge.helpers

logger = logging.getLogger(__name__)


def get_type_from_id(internal_id):
    """
    Parses the object type from a STIX 2.x object ID.

    :param internal_id: a STIX 2.x object ID (e.g.
        "attack-pattern--00d0b012-8a03-410e-95de-5826bf542de6)"

    :return: a STIX 2.x object type (e.g. "attack-pattern").
    """
    internal_id = ensure_type(internal_id, str)
    return stix2.utils.get_type_from_id(internal_id)


def is_id(internal_id):
    """
    Checks whether or not the provided string is a STIX 2.x object ID.

    :param internal_id: a STIX 2.x object ID (e.g.
        "attack-pattern--00d0b012-8a03-410e-95de-5826bf542de6)"

    :return: True or False.
    """
    internal_id = ensure_type(internal_id, str)
    return internal_id and "--" in internal_id and get_type_from_id(internal_id) != internal_id


def stix2_to_dict(data, include_optional_defaults=False):
    """"
    Translates the provided STIX 2.x object into a dictionary.

    :param data: a STIX 2.x object.
    :param include_optional_defaults: whether or not to include optional defaults from the STIX 2.x
        object in the resulting dictionary.

    :return: a dictionary.
    """
    data = ensure_type(data, (dict, _STIXBase))
    if isinstance(data, _STIXBase):
        data = data.serialize(include_optional_defaults=include_optional_defaults)
        data = json.loads(data)
    return data


def stix2_to_dataclass(data, data_class, include_optional_defaults=False, ignore_revoked=False):
    """"
    Translates the provided STIX 2.x object into a dataclass object.

    :param data: a STIX 2.x object.
    :param data_class: the dataclass to translate the provided STIX 2.x object into.
    :param include_optional_defaults: whether or not to include optional defaults from the STIX 2.x
        object in the resulting dictionary.

    :param ignore_revoked: whether or not to ignore revoked objects.

    :return: a dictionary.
    """
    data = stix2_to_dict(data, include_optional_defaults=include_optional_defaults)
    data = ensure_type(data, dict)
    if ignore_revoked and data.get('revoked', False):
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, data_class)


def partition_stream_of_object_ids(object_ids):
    """
    Partitions the provided stream of object IDs into a stream of internal, and external IDs.

    :param object_ids: a sequence of internal and/or external IDs.
    :return: a tuple of the form (internal IDs, external IDs).
    """
    internal_ids = set()
    external_ids = set()
    for object_id in hodgepodge.helpers.as_set(object_ids, expected_types=[str]):
        if is_id(object_id):
            internal_ids.add(object_id)
        else:
            external_ids.add(object_id)
    return internal_ids, external_ids
