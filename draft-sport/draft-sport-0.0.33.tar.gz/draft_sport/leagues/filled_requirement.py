"""
Draft Sport API
Filled Requirement Module
author: hugh@blinkybeach.com
"""
from nozomi import Immutable
from typing import List
from draft_sport.leagues.pick import Pick
from draft_sport.leagues.requirement import Requirement


class FilledRequirement:
    """
    Utility class coralling Requirement & Player data. Useful for client
    presentation purposes. There is no equivalent object in the
    Draft Sport API
    """

    def __init__(
        self,
        requirement: Requirement,
        picks: List[Pick]
    ) -> None:

        self._picks = picks
        self._requirement = requirement

        return

    picks = Immutable(lambda s: s._picks)
    position = Immutable(lambda s: s._requirement.position)
    count = Immutable(lambda s: s._requirement.count)
