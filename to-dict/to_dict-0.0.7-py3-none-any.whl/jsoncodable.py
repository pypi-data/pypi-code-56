from typing import Optional, Dict, Any

class JSONCodable:
    @classmethod
    def from_json(cls, json_data: Any) -> Optional:
        try:
            from collections import namedtuple
            import json

            if not isinstance(json_data, str):
                json_data = json.dumps(json_data)

            return json.loads(json_data, object_hook=lambda d: namedtuple('JSONCodable', d.keys())(*d.values()))
        except Exception as e:
            print(e)

            return None

    @property
    def dict(self) -> Dict:
        '''Creates, dict from object.'''
        return self.to_dict(self, recursive=False)

    @property
    def json(self) -> Dict:
        '''Same as .dict, but converts all object values to JSONSerializable ones recursively'''
        return self.to_dict(self, recursive=True)

    @classmethod
    def to_dict(cls, obj: Optional[Any], recursive: bool=True) -> Optional[Dict]:
        if obj is None or type(obj) in [str, float, int, bool]:
            return obj

        from copy import deepcopy
        from enum import Enum

        obj = deepcopy(obj)

        if isinstance(obj, list) or isinstance(obj, tuple):
            v_list = []

            for vv in obj:
                v_list.append(cls.to_dict(vv, recursive=recursive))

            return v_list
        elif isinstance(obj, dict):
            v_dict = {}

            for k, vv in obj.items():
                v_dict[k] = cls.to_dict(vv, recursive=recursive)

            return v_dict
        elif issubclass(type(obj), Enum):
            return obj.value

        return obj.__dict__ if not recursive else cls.to_dict(obj.__dict__, recursive=recursive)