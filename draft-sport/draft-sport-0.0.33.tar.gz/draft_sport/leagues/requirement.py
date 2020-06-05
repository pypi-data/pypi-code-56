"""
Draft Sport
Requirement Module
author: hugh@blinkybeach.com
"""
from nozomi import Immutable, Decodable
from typing import Type, TypeVar, Any

T = TypeVar('T', bound='Requirement')


class Requirement(Decodable):

    def __init__(
        self,
        count: int,
        position: str
    ) -> None:

        self._count = count
        self._position = position

        return

    count = Immutable(lambda s: s._count)
    position = Immutable(lambda s: s._position)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            count=data['count'],
            position=data['position']
        )
