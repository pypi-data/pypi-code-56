from typing import Optional, Dict, Any

from enum import Enum

class Dictable:
    @property
    def dict(self) -> Dict:
        '''Creates, dict from object. The values, that do not conform 'Dictable' will be left as objects'''
        return self.__converted(False)

    @property
    def json(self) -> Dict:
        '''Same as .dict, but converts all values to JSONSerializable ones'''
        return self.__converted(True)

    def __converted(self, convert_all_to_json_serializable: bool, obj: Optional[object] = None) -> Dict:
        obj = obj or self
        d = {}

        for k, v in obj.__dict__.items():
            d[k] = self.__get_value(v, convert_all_to_json_serializable)

        return d

    def __get_value(self, value: Any, convert_all_to_json_serializable: bool):
        if issubclass(type(value), Dictable):
            value = value.dict
        elif issubclass(type(value), list):
            v_list = []

            for vv in value:
                v_list.append(self.__get_value(vv, convert_all_to_json_serializable))

            value = v_list
        elif issubclass(type(value), dict):
            v_dict = {}

            for k, vv in value.items():
                v_dict[k] = self.__get_value(vv, convert_all_to_json_serializable)

            value = v_dict
        elif convert_all_to_json_serializable and issubclass(type(value), Enum):
            value = value.value

        if value is not None and convert_all_to_json_serializable:
            supported_types = [str, float, int, bool, list, dict]
            is_supported_type = False

            for supported_type in supported_types:
                if issubclass(type(value), supported_type):
                    is_supported_type = True

                    break
            
            if not is_supported_type:
                value = self.__converted(convert_all_to_json_serializable, obj=value)

        return value