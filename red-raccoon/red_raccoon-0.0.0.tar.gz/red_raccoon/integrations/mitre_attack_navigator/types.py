from typing import List, Union
from dataclasses import dataclass, field

from hodgepodge.helpers import ensure_type
from red_raccoon.integrations.mitre_attack_navigator import DEFAULT_LAYER_NAME, DEFAULT_LAYER_DESCRIPTION, \
    DEFAULT_LAYER_DOMAIN, DEFAULT_LAYER_VERSION, DEFAULT_COLOR

import hodgepodge.helpers
import logging
import ujson

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Gradient:
    colors: List[str]
    min_value: int
    max_value: int

    def as_dict(self):
        return {
            'colors': sorted(self.colors),
            'minValue': self.min_value,
            'maxValue': self.max_value,
        }


@dataclass(frozen=True)
class Technique:
    technique_id: str
    tactic_name: Union[str, None] = None
    enabled: bool = True
    color: str = DEFAULT_COLOR
    comment: Union[str, None] = None
    score: Union[int, None] = None

    def as_dict(self):
        data = {
            'techniqueID': self.technique_id,
            'color': self.color,
        }

        if self.tactic_name:
            data['tactic'] = self.tactic_name.lower().replace(' ', '-')

        if self.enabled is False:
            data['enabled'] = False

        if self.comment:
            data['comment'] = self.comment

        if self.score is not None:
            data['score'] = self.score

        return data


@dataclass(frozen=True)
class Layer:
    name: str = DEFAULT_LAYER_NAME
    description: str = DEFAULT_LAYER_DESCRIPTION
    domain: str = DEFAULT_LAYER_DOMAIN
    version: str = DEFAULT_LAYER_VERSION
    hide_disabled: bool = True
    gradient: Union[Gradient, None] = None
    techniques: List[Technique] = field(default_factory=list)

    @property
    def technique_ids(self):
        technique_ids = []
        for technique in self.techniques:
            if technique.technique_id not in technique_ids:
                technique_ids.append(technique.technique_id)
        return technique_ids

    def add_technique(self, technique, overwrite=False):
        technique = ensure_type(technique, Technique)
        if technique in self.techniques:
            if overwrite:
                self.techniques.remove(technique)
                self.techniques.append(technique)
            else:
                logger.warning("Refusing to add duplicate technique: %s", technique)
        else:
            self.techniques.append(technique)

    def add_techniques(self, techniques, overwrite=False):
        for technique in hodgepodge.helpers.as_list(techniques, Technique):
            self.add_technique(technique, overwrite=overwrite)

    def as_dict(self):
        data = {
            'name': self.name,
            'version': self.version,
            'domain': self.domain,
        }

        #: Default: ''.
        if self.description:
            data['description'] = self.description

        #: Default: n/a.
        if self.techniques:
            data['techniques'] = [technique.as_dict() for technique in self.techniques]

        #: Default: n/a.
        if self.gradient is not None:
            data['gradient'] = self.gradient.as_dict()

        #: Default: false.
        if self.hide_disabled is True:
            data['hideDisabled'] = True

        return data

    def as_json(self, indent=4, sort_keys=True):
        return ujson.dumps(self.as_dict(), indent=indent, sort_keys=sort_keys)

    def __len__(self):
        return len(self.techniques)

    def __iter__(self):
        for technique in self.techniques:
            yield technique
