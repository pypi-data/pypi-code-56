from typing import List, Union
from dataclasses import dataclass, field

import hodgepodge.helpers
import itertools


@dataclass(frozen=True)
class Tactic:
    external_id: str
    name: str

    @property
    def id(self):
        return self.external_id


@dataclass(frozen=True)
class Technique:
    external_id: str
    name: str

    @property
    def id(self):
        return self.external_id


@dataclass(frozen=True)
class Screenshot:
    path: str
    caption: Union[str, None] = None

    def is_url(self):
        return self.path.startswith('http://') or \
               self.path.startswith('https://')

    def has_caption(self):
        return bool(self.caption)


@dataclass(frozen=True)
class Observation:
    note: str
    type: str
    modifiers: List[str]
    footnotes: List[str]
    screenshots: List[Screenshot]

    def is_detection(self):
        return self.was_detected()

    def was_detected(self):
        return self.type != 'None'

    def was_delayed(self):
        return 'Delayed' in self.modifiers or \
               'Delayed (Manual)' in self.modifiers or \
               'Delayed (Processing)' in self.modifiers

    def has_screenshots(self):
        return bool(self.screenshots)

    def has_modifiers(self):
        return bool(self.modifiers)

    def has_footnotes(self):
        return bool(self.footnotes)


@dataclass(frozen=True)
class Step:
    name: str
    procedure: str
    observations: List[Observation]
    criteria: Union[str, None] = None

    @property
    def detections(self):
        return self.get_detections()

    @property
    def observation_types(self):
        return sorted({observation.type for observation in self.observations})

    @property
    def observation_modifiers(self):
        return sorted(set(itertools.chain.from_iterable(observation.modifiers for observation in self.observations)))

    @property
    def screenshots(self):
        return self.get_screenshots()

    def get_screenshots(self, observation_types=None, observation_modifiers=None):
        return list(self.iter_screenshots(
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        ))

    def iter_screenshots(self, observation_types=None, observation_modifiers=None):
        observations = self.iter_observations(
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        for observation in observations:
            for screenshot in observation.screenshots:
                yield screenshot

    def get_observations(self, observation_types=None, observation_modifiers=None):
        return list(self.iter_observations(
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        ))

    def iter_observations(self, observation_types=None, observation_modifiers=None):
        types = hodgepodge.helpers.as_set(observation_types, str)
        modifiers = hodgepodge.helpers.as_set(observation_modifiers, str)

        for observation in self.observations:

            #: Filter observations by type.
            if types and not hodgepodge.helpers.string_matches_any_pattern(observation.type, types):
                continue

            #: Filter observations by modifier.
            if modifiers and not hodgepodge.helpers.any_string_matches_any_pattern(observation.modifiers, modifiers):
                continue

            yield observation

    def get_detections(self, observation_types=None, observation_modifiers=None):
        return list(self.iter_detections(
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        ))

    def iter_detections(self, observation_types=None, observation_modifiers=None):
        observations = self.iter_observations(
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        for observation in observations:
            if observation.is_detection():
                yield observation

    def has_screenshots(self):
        return bool(self.screenshots)

    def has_detections(self):
        return any(observation.is_detection() for observation in self.observations)

    def has_criteria(self):
        return bool(self.criteria)

    def __len__(self):
        return len(self.observations)

    def __iter__(self):
        for observation in self.observations:
            yield observation


@dataclass(frozen=True)
class Test:
    technique: Technique
    tactics: List[Tactic]
    steps: List[Step]

    @property
    def tactic_ids(self):
        return sorted([tactic.id for tactic in self.tactics])

    @property
    def tactic_names(self):
        return sorted([tactic.name for tactic in self.tactics])

    @property
    def technique_id(self):
        return self.technique.id

    @property
    def technique_name(self):
        return self.technique.name

    @property
    def detections(self):
        return self.get_detections()

    @property
    def observations(self):
        return self.get_observations()

    @property
    def observation_types(self):
        return sorted({observation.type for observation in self.observations})

    @property
    def observation_modifiers(self):
        return sorted(set(itertools.chain.from_iterable(observation.modifiers for observation in self.observations)))

    @property
    def screenshots(self):
        return self.get_screenshots()

    def get_screenshots(self, observation_types=None, observation_modifiers=None):
        return list(self.iter_screenshots(
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        ))

    def iter_screenshots(self, observation_types=None, observation_modifiers=None):
        for step in self.steps:
            screenshots = step.get_screenshots(
                observation_types=observation_types,
                observation_modifiers=observation_modifiers,
            )
            for screenshot in screenshots:
                yield screenshot

    def get_observations(self, observation_types=None, observation_modifiers=None):
        return list(self.iter_observations(
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        ))

    def iter_observations(self, observation_types=None, observation_modifiers=None):
        for step in self.steps:
            observations = step.iter_observations(
                observation_types=observation_types,
                observation_modifiers=observation_modifiers,
            )
            for observation in observations:
                yield observation

    def get_detections(self, observation_types=None, observation_modifiers=None):
        return list(self.iter_detections(
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        ))

    def iter_detections(self, observation_types=None, observation_modifiers=None):
        for step in self.steps:
            detections = step.iter_detections(
                observation_types=observation_types,
                observation_modifiers=observation_modifiers,
            )
            for detection in detections:
                yield detection

    def has_screenshots(self):
        for step in self.steps:
            if step.has_screenshots():
                return True
        return False

    def has_detections(self):
        for step in self.steps:
            if step.has_detections():
                return True
        return False

    def was_detected(self):
        return self.has_detections()

    def was_not_detected(self):
        return self.has_detections() is False

    def __len__(self):
        return len(self.steps)

    def __iter__(self):
        for step in self.steps:
            yield step


@dataclass(frozen=True)
class Evaluation:
    vendor: str
    group: str
    tests: List[Test] = field(repr=False)

    @property
    def group_name(self):
        return self.group

    @property
    def vendor_name(self):
        return self.vendor

    @property
    def tactics(self):
        return self.get_tactics()

    @property
    def tactic_ids(self):
        return self.get_tactic_ids()

    @property
    def tactic_names(self):
        return self.get_tactic_names()

    @property
    def detected_tactics(self):
        return self.get_detected_tactics()

    @property
    def detected_tactic_ids(self):
        return self.get_detected_tactic_ids()

    @property
    def detected_tactic_names(self):
        return self.get_detected_tactic_names()

    @property
    def undetected_tactics(self):
        return self.get_undetected_tactics()

    @property
    def undetected_tactic_ids(self):
        return self.get_undetected_tactic_ids()

    @property
    def undetected_tactic_names(self):
        return self.get_undetected_tactic_names()

    @property
    def techniques(self):
        return self.get_techniques()

    @property
    def technique_ids(self):
        return self.get_technique_ids()

    @property
    def technique_names(self):
        return self.get_technique_names()

    @property
    def detected_techniques(self):
        return self.get_detected_techniques()

    @property
    def detected_technique_ids(self):
        return self.get_detected_technique_ids()

    @property
    def detected_technique_names(self):
        return self.get_detected_technique_names()

    @property
    def undetected_techniques(self):
        return self.get_undetected_techniques()

    @property
    def undetected_technique_ids(self):
        return self.get_undetected_technique_ids()

    @property
    def undetected_technique_names(self):
        return self.get_undetected_technique_names()

    @property
    def observations(self):
        return self.get_observations()

    @property
    def observation_types(self):
        return sorted({observation.type for observation in self.get_observations()})

    @property
    def observation_modifiers(self):
        modifiers = set()
        for observation in self.observations:
            modifiers |= set(observation.modifiers)
        return sorted(modifiers)

    @property
    def detections(self):
        return self.get_detections()

    @property
    def screenshots(self):
        return self.get_screenshots()

    def get_tactics(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                    observation_types=None, observation_modifiers=None):

        tests = self.iter_tests(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        tactics = []
        for test in tests:
            for tactic in test.tactics:
                if tactic not in tactics:
                    tactics.append(tactic)
        return tactics

    def get_tactic_ids(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                       observation_types=None, observation_modifiers=None):

        tactics = self.get_tactics(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.id for t in tactics})

    def get_tactic_names(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                         observation_types=None, observation_modifiers=None):

        tactics = self.get_tactics(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.name for t in tactics})

    def get_detected_tactics(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                             observation_types=None, observation_modifiers=None):

        detected_tactics = set()
        tests = self.get_tests(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        for test in tests:
            if test.was_detected():
                for tactic in test.tactics:
                    if tactic not in detected_tactics:
                        detected_tactics.add(tactic)
        return sorted(detected_tactics, key=lambda t: t.id)

    def get_detected_tactic_ids(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                                observation_types=None, observation_modifiers=None):

        tactics = self.get_detected_tactics(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.id for t in tactics})

    def get_detected_tactic_names(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                                  observation_types=None, observation_modifiers=None):

        tactics = self.get_detected_tactics(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.name for t in tactics})

    def get_undetected_tactics(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                               observation_types=None, observation_modifiers=None):

        tactics = self.get_tactics(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        detected_tactics = self.get_detected_tactics(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        undetected_tactics = set(tactics) - set(detected_tactics)
        return sorted(undetected_tactics, key=lambda t: t.id)

    def get_undetected_tactic_ids(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                                  observation_types=None, observation_modifiers=None):

        tactics = self.get_undetected_tactics(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.id for t in tactics})

    def get_undetected_tactic_names(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                                    observation_types=None, observation_modifiers=None):

        tactics = self.get_undetected_tactics(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.name for t in tactics})

    def get_techniques(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                       observation_types=None, observation_modifiers=None):

        tests = self.iter_tests(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        techniques = []
        for test in tests:
            if test.technique not in techniques:
                techniques.append(test.technique)
        return techniques

    def get_technique_ids(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                          observation_types=None, observation_modifiers=None):

        techniques = self.get_techniques(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.id for t in techniques})

    def get_technique_names(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                            observation_types=None, observation_modifiers=None):

        techniques = self.get_techniques(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.name for t in techniques})

    def get_detected_techniques(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                                observation_types=None, observation_modifiers=None):

        tests = self.iter_tests(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        detected_techniques = {test.technique for test in tests if test.was_detected()}
        return sorted(detected_techniques, key=lambda t: t.id)

    def get_detected_technique_ids(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                                   observation_types=None, observation_modifiers=None):

        techniques = self.get_detected_techniques(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.id for t in techniques})

    def get_detected_technique_names(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                                     observation_types=None, observation_modifiers=None):

        techniques = self.get_detected_techniques(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.name for t in techniques})

    def get_undetected_techniques(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                                  observation_types=None, observation_modifiers=None):

        techniques = self.get_techniques(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        detected_techniques = self.get_detected_techniques(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        undetected_techniques = set(techniques) - set(detected_techniques)
        return sorted(undetected_techniques, key=lambda t: t.id)

    def get_undetected_technique_ids(self, tactic_ids=None, tactic_names=None, technique_ids=None,
                                     technique_names=None, observation_types=None, observation_modifiers=None):

        techniques = self.get_undetected_techniques(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.id for t in techniques})

    def get_undetected_technique_names(self, tactic_ids=None, tactic_names=None, technique_ids=None,
                                       technique_names=None, observation_types=None, observation_modifiers=None):

        techniques = self.get_undetected_techniques(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return sorted({t.name for t in techniques})

    def get_tests(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                  observation_types=None, observation_modifiers=None):

        return list(self.iter_tests(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        ))

    def iter_tests(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                   observation_types=None, observation_modifiers=None):

        tactic_ids = hodgepodge.helpers.as_set(tactic_ids, str)
        tactic_names = hodgepodge.helpers.as_set(tactic_names, str)
        technique_ids = hodgepodge.helpers.as_set(technique_ids, str)
        technique_names = hodgepodge.helpers.as_set(technique_names, str)
        observation_types = hodgepodge.helpers.as_set(observation_types, str)
        observation_modifiers = hodgepodge.helpers.as_set(observation_modifiers, str)

        for test in self.tests:

            #: Filter tests by tactic ID.
            if tactic_ids and not hodgepodge.helpers.any_string_matches_any_pattern(test.tactic_ids, tactic_ids):
                continue

            #: Filter tests by tactic name.
            if tactic_names and not hodgepodge.helpers.any_string_matches_any_pattern(test.tactic_names, tactic_names):
                continue

            #: Filter tests by technique ID.
            if technique_ids and not hodgepodge.helpers.string_matches_any_pattern(test.technique_id, technique_ids):
                continue

            #: Filter tests by technique name.
            if technique_names:
                if not hodgepodge.helpers.string_matches_any_pattern(test.technique_name, technique_names):
                    continue

            #: Filter tests by observation type.
            if observation_types:
                if not hodgepodge.helpers.any_string_matches_any_pattern(test.observation_types, observation_types):
                    continue

            #: Filter tests by observation modifier.
            if observation_modifiers:
                if not hodgepodge.helpers.any_string_matches_any_pattern(test.observation_modifiers,
                                                                         observation_modifiers):
                    continue

            yield test

    def get_screenshots(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                        observation_types=None, observation_modifiers=None):

        return list(self.iter_screenshots(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        ))

    def iter_screenshots(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                         observation_types=None, observation_modifiers=None):

        tests = self.get_tests(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )
        for test in tests:
            screenshots = test.iter_screenshots(
                observation_types=observation_types,
                observation_modifiers=observation_modifiers,
            )
            for screenshot in screenshots:
                yield screenshot

    def get_observations(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                         observation_types=None, observation_modifiers=None):

        return list(self.iter_observations(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        ))

    def iter_observations(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                          observation_types=None, observation_modifiers=None):

        tests = self.get_tests(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )
        for test in tests:
            observations = test.iter_observations(
                observation_types=observation_types,
                observation_modifiers=observation_modifiers,
            )
            for observation in observations:
                yield observation

    def get_detections(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                       observation_types=None, observation_modifiers=None):

        return list(self.iter_detections(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        ))

    def iter_detections(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                        observation_types=None, observation_modifiers=None):

        tests = self.get_tests(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )
        for test in tests:
            detections = test.iter_detections(
                observation_types=observation_types,
                observation_modifiers=observation_modifiers,
            )
            for detection in detections:
                yield detection

    def has_test(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                 observation_types=None, observation_modifiers=None):

        tests = self.iter_tests(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return bool(next(tests, 0))

    def has_screenshots(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                        observation_types=None, observation_modifiers=None):

        screenshots = self.iter_screenshots(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return bool(next(screenshots, 0))

    def has_observations(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                         observation_types=None, observation_modifiers=None):

        observations = self.iter_observations(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return bool(next(observations, 0))

    def has_detections(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                       observation_types=None, observation_modifiers=None):

        detections = self.iter_detections(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            observation_types=observation_types,
            observation_modifiers=observation_modifiers,
        )
        return bool(next(detections, 0))

    def __len__(self):
        return len(self.tests)

    def __iter__(self):
        for test in self.tests:
            yield test
