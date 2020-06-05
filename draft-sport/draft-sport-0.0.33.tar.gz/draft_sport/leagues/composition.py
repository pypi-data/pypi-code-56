"""
Draft Sport Python
Composition Module
author: hugh@blinkybeach.com
"""
from nozomi import Immutable, Decodable
from typing import TypeVar, Type, Any, List
from draft_sport.leagues.requirement import Requirement

T = TypeVar('T', bound='Composition')


class Composition(Decodable):

    def __init__(
        self,
        requirements: List[Requirement]
    ) -> None:

        self._requirements = requirements

        return

    requirements = Immutable(lambda s: s._requirements)
    unique_positions: List[str] = Immutable(
        lambda s: list(set(r.position for r in s._requirements))
    )

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            requirements=Requirement.decode_many(data['requirements'])
        )
