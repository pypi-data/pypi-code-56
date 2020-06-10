"""
This module contains functions for creating STIX 2.x pattern filters.
"""

from stix2 import Filter

import hodgepodge.helpers

from hodgepodge.helpers import ensure_type
from red_raccoon.stix import EQ, IN, RELATIONSHIP, RELATIONSHIP_TYPE, ID, TYPE, SOURCE_REF, \
    TARGET_REF, EXTERNAL_ID


def select_object_type_filter(filters):
    """
    Filters the provided sequence of filters and returns the filter which matches object types.

    :param filters: an optional sequence of filters.
    :return: the first matching filter where the left-hand side of the filter is equal to "type".
    """
    return next(filter(lambda f: f.property == 'type', filters), None)


def get_generic_filter(lhs, operand, rhs):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param lhs: the left-hand side of the pattern (e.g. "type").
    :param operand: the operand of the pattern (e.g. "=").
    :param rhs: the right-hand side of the pattern (e.g. "attack-pattern").
    :return: a STIX 2.x filter object.
    """
    lhs = ensure_type(lhs, str)
    operand = ensure_type(operand, str)

    #: The RHS of a filter must be an immutable type, or a dictionary.
    if hodgepodge.helpers.is_iterable(rhs) and not isinstance(rhs, (str, tuple)):
        rhs = hodgepodge.helpers.as_tuple(rhs)

    return Filter(lhs, operand, rhs)


def get_string_field_filter(lhs, rhs):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param lhs: the left-hand side of the pattern (e.g. "type").
    :param rhs: the right-hand side of the pattern (e.g. "attack-pattern").
    :return: a STIX 2.x filter object.
    """
    if isinstance(rhs, str):
        return get_generic_filter(lhs, EQ, rhs)

    _rhs = hodgepodge.helpers.as_unique_list(rhs)
    if len(_rhs) == 1:
        return get_generic_filter(lhs, EQ, _rhs[0])
    return get_generic_filter(lhs, IN, rhs)


def get_boolean_field_filter(lhs, rhs):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param lhs: the left-hand side of the pattern (e.g. "revoked").
    :param rhs: the right-hand side of the pattern (e.g. True).
    :return: a STIX 2.x filter object.
    """
    return get_generic_filter(lhs, EQ, ensure_type(rhs, bool))


def get_object_type_filter(object_types):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param object_types: a sequence of object types (e.g. ["attack-pattern", "intrusion-set"]).
    :return: a STIX 2.x filter object.
    """
    return get_string_field_filter(TYPE, object_types)


def get_object_internal_id_filter(object_internal_ids):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param object_internal_ids: a sequence of internal IDs (e.g.
        ["attack-pattern--00d0b012-8a03-410e-95de-5826bf542de6"]).

    :return: a STIX 2.x filter object.
    """
    return get_string_field_filter(ID, object_internal_ids)


def get_object_external_id_filter(object_external_ids):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param object_external_ids: a sequence of external IDs (e.g. ["T1066"]).

    :return: a STIX 2.x filter object.
    """
    return get_string_field_filter(EXTERNAL_ID, object_external_ids)


def get_relationship_type_filter(relationship_types):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param relationship_types: a sequence of relationship types (e.g. ["mitigates", "uses"]).

    :return: a STIX 2.x filter object.
    """
    return get_string_field_filter(RELATIONSHIP_TYPE, relationship_types)


def get_source_object_internal_id_filter(source_object_internal_ids):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param source_object_internal_ids: a sequence of source internal IDs (e.g.
        ["attack-pattern--00d0b012-8a03-410e-95de-5826bf542de6"]).

    :return: a STIX 2.x filter object.
    """
    return get_string_field_filter(SOURCE_REF, source_object_internal_ids)


def get_target_object_internal_id_filter(target_object_internal_ids):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param target_object_internal_ids: a sequence of target internal IDs (e.g.
        ["attack-pattern--00d0b012-8a03-410e-95de-5826bf542de6"]).

    :return: a STIX 2.x filter object.
    """
    return get_string_field_filter(TARGET_REF, target_object_internal_ids)


def get_filters_for_object(object_types=None, object_internal_id=None, object_external_id=None):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param object_types: a sequence of object types (e.g ["attack-pattern"]).
    :param object_internal_id: an internal ID
        (e.g. "attack-pattern--00d0b012-8a03-410e-95de-5826bf542de6").

    :param object_external_id: an external ID (e.g. "T1066").

    :return: a STIX 2.x filter object.
    """
    #: An internal, or external ID can be provided, but not both.
    if object_internal_id and object_external_id:
        hint = "internal ID: {}, external ID: {}, object_types: {}".format(
            object_types,
            object_internal_id,
            object_external_id
        )
        raise ValueError("Cannot lookup objects using both internal and external ID ({})".format(
            hint
        ))

    #: Dynamically construct the list of object filters.
    filters = []

    #: Filter by type.
    if object_types:
        filters.append(get_object_type_filter(object_types))

    #: Filter by internal ID.
    if object_internal_id:
        filters.append(get_object_internal_id_filter(object_internal_id))

    #: Filter by external ID.
    if object_external_id:
        filters.append(get_object_external_id_filter(object_external_id))

    return filters


def get_filters_for_objects(object_types=None, object_internal_ids=None, object_external_ids=None):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param object_types: a sequence of object types (e.g ["attack-pattern"]).
    :param object_internal_ids: a sequence of internal IDs
        (e.g. ["attack-pattern--00d0b012-8a03-410e-95de-5826bf542de6"]).

    :param object_external_ids: a sequence of external ID (e.g. ["T1066"]).

    :return: a STIX 2.x filter object.
    """
    filters = []

    #: Filter by type.
    if object_types:
        filters.append(get_object_type_filter(object_types))

    #: Filter by ID(s).
    if object_internal_ids:
        filters.append(get_object_internal_id_filter(object_internal_ids))

    #: Filter by external ID(s).
    if object_external_ids:
        filters.append(get_object_external_id_filter(object_external_ids))

    return filters


def get_filters_for_relationships(source_object_internal_ids=None, target_object_internal_ids=None,
                                  relationship_types=None):
    """
    Creates a STIX 2.x filter using the provided criteria.

    :param source_object_internal_ids: a sequence of source internal IDs.
    :param target_object_internal_ids: a sequence of target internal IDs.
    :param relationship_types: a sequence of relationship types.

    :return: a STIX 2.x filter object.
    """

    filters = [
        get_object_type_filter(RELATIONSHIP)
    ]

    #: Filter by source ref(s).
    if source_object_internal_ids:
        filters.append(get_source_object_internal_id_filter(source_object_internal_ids))

    #: Filter by target ref(s).
    if target_object_internal_ids:
        filters.append(get_target_object_internal_id_filter(target_object_internal_ids))

    #: Filter by relationship type(s).
    if relationship_types:
        filters.append(get_relationship_type_filter(relationship_types))

    return filters
