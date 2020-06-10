from dataclasses import dataclass, field
from typing import List
from itertools import chain


@dataclass
class Word:
    word: str
    wordtype: str
    shortdef: List[str] = field(default_factory=list)
    synonyms: List[str] = field(default_factory=list)
    antonyms: List[str] = field(default_factory=list)
    stems: List[str] = field(default_factory=list)

    @classmethod
    def from_response(cls, r: dict) -> object:
        obj = cls.__new__(cls)
        obj.word = r["meta"]["id"]
        obj.wordtype = r["fl"]
        obj.shortdef = r["shortdef"]
        obj.synonyms = list(chain.from_iterable(r["meta"]["syns"]))
        obj.antonyms = list(chain.from_iterable(r["meta"]["ants"]))
        obj.stems = r["meta"]["stems"]
        return obj
