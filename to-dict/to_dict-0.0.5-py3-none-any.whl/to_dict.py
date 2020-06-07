from typing import Optional, Dict, Any
from enum import Enum
from copy import deepcopy

class Dictable:
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

        obj = deepcopy(obj)

        if isinstance(obj, list):
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