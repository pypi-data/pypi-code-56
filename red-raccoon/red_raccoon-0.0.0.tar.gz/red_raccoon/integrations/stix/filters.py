from stix2 import Filter

import hodgepodge.helpers

from hodgepodge.helpers import ensure_type
from red_raccoon.integrations.stix import EQ, IN, RELATIONSHIP, RELATIONSHIP_TYPE, ID, TYPE, SOURCE_REF, \
    TARGET_REF, EXTERNAL_ID, REVOKED, NAME, ALIASES


def select_object_type_filter(filters):
    return next(filter(lambda f: f.property == 'type', hodgepodge.helpers.as_list(filters, Filter)), None)


def get_filter(lhs, operand, rhs):
    lhs = ensure_type(lhs, str)
    operand = ensure_type(operand, str)

    #: The RHS of a filter must be an immutable type, or a dictionary.
    if hodgepodge.helpers.is_iterable(rhs) and not isinstance(rhs, (str, tuple)):
        rhs = hodgepodge.helpers.as_tuple(rhs)

    return Filter(lhs, operand, rhs)


def get_string_filter(lhs, rhs):
    if isinstance(rhs, str):
        return get_filter(lhs, EQ, rhs)

    _rhs = hodgepodge.helpers.as_unique_list(rhs)
    if len(_rhs) == 1:
        return get_filter(lhs, EQ, _rhs[0])
    return get_filter(lhs, IN, rhs)


def get_boolean_filter(lhs, rhs):
    return get_filter(lhs, EQ, ensure_type(rhs, bool))


def get_object_type_filter(object_types):
    return get_string_filter(TYPE, object_types)


def get_revoked_object_filter():
    return get_filter(REVOKED, EQ, True)


def get_object_internal_id_filter(object_internal_ids):
    return get_string_filter(ID, object_internal_ids)


def get_object_external_id_filter(object_external_ids):
    return get_string_filter(EXTERNAL_ID, object_external_ids)


def get_relationship_type_filter(relationship_types):
    return get_string_filter(RELATIONSHIP_TYPE, relationship_types)


def get_source_object_internal_id_filter(source_object_internal_ids):
    return get_string_filter(SOURCE_REF, source_object_internal_ids)


def get_target_object_internal_id_filter(target_object_internal_ids):
    return get_string_filter(TARGET_REF, target_object_internal_ids)


def get_filters_for_object(object_types=None, object_internal_id=None, object_external_id=None):
    filters = []

    if object_types:
        filters.append(get_object_type_filter(sorted(object_types)))

    if object_internal_id:
        filters.append(get_object_internal_id_filter(object_internal_id))

    if object_external_id:
        filters.append(get_object_external_id_filter(object_external_id))

    return filters


def get_filters_for_objects(object_types=None, object_internal_ids=None, object_external_ids=None):
    filters = []

    if object_types:
        filters.append(get_object_type_filter(sorted(object_types)))

    if object_internal_ids:
        filters.append(get_object_internal_id_filter(sorted(object_internal_ids)))

    if object_external_ids:
        filters.append(get_object_external_id_filter(sorted(object_external_ids)))

    return filters


def get_filters_for_relationships(source_object_internal_ids=None, target_object_internal_ids=None, 
                                  relationship_types=None):
    filters = [
        get_object_type_filter(RELATIONSHIP)
    ]

    #: Filter by source ref(s).
    if source_object_internal_ids:
        filters.append(get_source_object_internal_id_filter(sorted(source_object_internal_ids)))

    #: Filter by target ref(s).
    if target_object_internal_ids:
        filters.append(get_target_object_internal_id_filter(sorted(target_object_internal_ids)))

    #: Filter by relationship type(s).
    if relationship_types:
        filters.append(get_relationship_type_filter(sorted(relationship_types)))

    return filters


def get_list_of_properties_from_filters(filters):
    return sorted([f.property for f in hodgepodge.helpers.as_set(filters, expected_types=[Filter])])


def get_list_of_human_readable_filters(filters):
    filters = sorted(hodgepodge.helpers.as_set(filters, expected_types=[Filter]), key=lambda f: f.property)
    return ["'{} {} {}'".format(f.property, f.op, f.value) for f in filters]


def object_has_matching_external_id(obj, object_external_ids):
    external_ids = set()
    for external_reference in obj.get('external_references', []):
        external_id = external_reference.get('external_id')
        if external_id:
            external_ids.add(external_id)
    return external_ids and external_ids & hodgepodge.helpers.as_set(object_external_ids, str)


def object_has_matching_name(obj, object_names):
    name = obj.get(NAME)
    aliases = set(obj.get(ALIASES, set()))

    if not (name or aliases):
        return False

    if name and aliases:
        names = {name} | aliases
    elif name:
        names = {name}
    else:
        names = aliases

    #: Account for improperly placed spaces in the search term (e.g. "OilRig" vs "Oil Rig".
    names |= {hodgepodge.helpers.camel_case_to_snake_case(name) for name in names}
    names |= {hodgepodge.helpers.snake_case_to_camel_case(name) for name in names}
    names |= {name.replace('_', ' ') for name in names}

    return hodgepodge.helpers.any_string_matches_any_pattern(
        strings=names, patterns=object_names, case_sensitive=False,
    )


def filter_objects_by_name(objects, object_names):
    for obj in objects:
        if object_has_matching_name(obj, object_names):
            yield obj


def filter_revoked_objects(objects):
    for obj in objects:
        revoked = obj.get(REVOKED, False)
        if not revoked:
            yield obj
