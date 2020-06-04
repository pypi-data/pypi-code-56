from __future__ import annotations
from typing import List
import json

from pyterum.local_fragment_desc import LocalFileDesc


class FragmenterInputMessage:
    def __init__(self, data_files:List[str], config_files:List[LocalFileDesc]):
        self.config_files = config_files
        self.data_files = data_files
    
    def __str__(self):
        return str(self.to_json())

    def to_json(self) -> dict:
        result = {}
        result["config_files"] = [f.to_json() for f in self.config_files]
        result["data_files"] = self.data_files
        return result

    @classmethod
    def from_json(cls, d:dict) -> cls:
        if not isinstance(d, dict):
            raise TypeError("Argument 'd' is not of type 'dict'")
        result = cls([], [])
        result.config_files = [LocalFileDesc.from_json(f) for f in d["config_files"]]
        result.data_files = d["data_files"]

        return result