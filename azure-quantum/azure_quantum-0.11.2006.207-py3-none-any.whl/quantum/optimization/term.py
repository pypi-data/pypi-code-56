##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

from typing import List, Union

__all__ = ['Term']

class Term:

    def __init__(self, w: Union[int, float], indices: List[int]):
        if type(w) != int and type(w) != float:
            raise RuntimeError("w must be a float or int value.")

        self.w = w
        self.ids = indices

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False