#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Copyright 2020 Kaede Hoshikawa
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from typing import TypeVar, AnyStr, Generic, Tuple, Union, Iterable, \
    Optional, Iterator

from ._dict import MagicDict
from ._frozen_tolerant_dict import FrozenTolerantMagicDict

import typing

__all__ = ["TolerantMagicDict"]

_V = TypeVar("_V")


class TolerantMagicDict(
    MagicDict[AnyStr, _V], FrozenTolerantMagicDict[AnyStr, _V],
        Generic[AnyStr, _V]):
    """
    `TolerantMagicDict` has exactly the same functionality as
    `MagicDict`. However, the keys are case-insensitive.
    """
    __slots__: Tuple[str, ...] = ()

    def copy(self) -> "TolerantMagicDict[AnyStr, _V]":
        return self.__class__(self)

    @classmethod
    @typing.overload
    def fromkeys(Cls, keys: Iterable[AnyStr]) -> \
            "TolerantMagicDict[AnyStr, None]":
        ...

    @classmethod
    @typing.overload
    def fromkeys(Cls, keys: Iterable[AnyStr],
                 value: _V) -> "TolerantMagicDict[AnyStr, _V]":
        ...

    @classmethod
    def fromkeys(  # type: ignore
        Cls, keys: Iterable[AnyStr], value: Optional[_V] = None) -> \
            Union["TolerantMagicDict[AnyStr, None]",
                  "TolerantMagicDict[AnyStr, _V]"]:
        def _gen() -> Iterator[Tuple[AnyStr, Optional[_V]]]:
            for k in keys:
                yield (k, value)

        return Cls(_gen())
