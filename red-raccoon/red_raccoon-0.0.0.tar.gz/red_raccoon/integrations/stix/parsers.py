
import stix2.utils

from stix2.base import _STIXBase
from hodgepodge.helpers import ensure_type

import hodgepodge.helpers


def is_internal_id(object_internal_id):
    object_internal_id = ensure_type(object_internal_id, str)
    if object_internal_id:
        return get_type_from_internal_id(object_internal_id) != object_internal_id
    return False


def get_type_from_internal_id(object_internal_id):
    internal_id = ensure_type(object_internal_id, str)
    return stix2.utils.get_type_from_id(internal_id)


def get_types_from_internal_ids(object_internal_ids):
    return sorted({get_type_from_internal_id(object_id) for object_id in object_internal_ids})


def get_names_from_object(obj):
    name = obj.get('name')
    aliases = obj.get('aliases', [])
    if name and name not in aliases:
        names = {name} | set(aliases)
    else:
        names = set(aliases)
    return names


def get_names_from_objects(objects):
    names = set()
    for obj in objects:
        names |= get_names_from_object(obj)
    return names


def get_type_from_object(obj):
    return obj['type']


def get_types_from_objects(objects):
    return {get_type_from_object(obj) for obj in objects}


def get_internal_id_from_object(obj):
    return obj['id']


def get_internal_ids_from_objects(objects):
    return {get_internal_id_from_object(obj) for obj in objects}


def get_external_ids_from_object(obj):
    external_ids = set()
    for external_reference in obj.get('external_references', []):
        external_id = external_reference.get('external_id')
        if external_id:
            external_ids.add(external_id)
    return external_ids


def get_external_ids_from_objects(objects):
    external_ids = set()
    for obj in objects:
        external_ids |= get_external_ids_from_object(obj)
    return external_ids


def partition_set_of_object_ids(object_ids):
    internal_ids = set()
    external_ids = set()
    object_ids = {ensure_type(object_id, str) for object_id in object_ids}
    for object_id in object_ids:
        if is_internal_id(object_id):
            internal_ids.add(object_id)
        else:
            external_ids.add(object_id)
    return internal_ids, external_ids


def stix2_to_dict(data):
    if isinstance(data, dict):
        return data

    result = {}
    for key, value in ensure_type(data, _STIXBase).items():
        if isinstance(value, (bool, str)):
            pass

        elif isinstance(value, stix2.utils.STIXdatetime):
            value = stix2.utils.format_datetime(value)

        elif isinstance(value, _STIXBase):
            value = stix2_to_dict(value)

        elif isinstance(value, list):
            value = [stix2_to_dict(e) if isinstance(e, _STIXBase) else e for e in value]

        result[key] = value
    return result


def stix2_to_dataclass(data, data_class):
    data = stix2_to_dict(data)
    return hodgepodge.helpers.dict_to_dataclass(data, data_class)
