import json
from .containers import Structure, List, Dict, Field
from . import fields


def __deserialise__(ser):
    def _issubclass(cls, t):
        try:
            return issubclass(cls, t)
        except TypeError:
            return False

    types = dict(str=str, int=int, float=float, bool=bool, NoneType=lambda *_: None, **{
        k: getattr(fields, k) for k in dir(fields) if _issubclass(getattr(fields, k), Field)
    })

    if isinstance(ser, str):
        ser = json.loads(ser)

    def new_structure(defs):
        fields = {}
        for k, v in defs['fields'].items():
            fields[k] = decode(v)
        return type(defs['name'], (Structure,), fields)

    def decode(item):
        if item['type'] == 'Structure':
            t = new_structure(item)
            cls = types.get(item['name'], t)
            types[item['name']] = cls
            return cls(**dict(t().__iter__()))

        if item['type'] == 'List':
            obj = List(*(decode(v) for v in item['value']), type=decode(item['element_type']).__class__)

        elif item['type'] == 'Dict':
            obj = Dict(type=decode(item['element_type']).__class__)
            obj.update(dict(((k, decode(v)) for k, v in item['value'].items())))
        else:
            obj = types[item['type']](*item['value'])

        if hasattr(obj, "__doc__"):
            obj.__doc__ = item.get("doc", "")

        if hasattr(obj, "__group__"):
            obj.__group__ = item.get("group", "")
        return obj

    return decode(ser).__class__

