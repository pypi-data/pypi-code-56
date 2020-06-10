from red_raccoon.integrations.mitre_attack_evaluations.types import Tactic, Technique, Evaluation, Step, Test, \
    Observation, Screenshot

import hodgepodge.helpers
import logging
import re
import os

logger = logging.getLogger(__name__)

_RE_VENDOR_AND_GROUP = re.compile(r'([\w_-]+)\.1\.([\w_-]+)\..+')


def parse_evaluation(data, vendor_name, group_name, screenshots_directory=None):
    tests = [parse_test(test, screenshots_directory=screenshots_directory) for test in data['Techniques']]
    data = {
        'vendor': vendor_name,
        'group': group_name,
        'tests': tests,
    }
    return hodgepodge.helpers.dict_to_dataclass(data, Evaluation)


def parse_test(data, screenshots_directory=None):
    technique = parse_technique(data)
    tactics = [parse_tactic(tactic) for tactic in data['Tactics']]
    steps = [parse_step(step=step, screenshots_directory=screenshots_directory) for step in data['Steps']]

    data = {
        'technique': technique,
        'tactics': tactics,
        'steps': steps,
    }
    return hodgepodge.helpers.dict_to_dataclass(data, Test)


def parse_tactic(data):
    return Tactic(external_id=data['TacticId'], name=data['TacticName'])


def parse_technique(data):
    return Technique(external_id=data['TechniqueId'], name=data['TechniqueName'])


def parse_step(step, screenshots_directory=None):
    observations = [parse_observation(o, screenshots_directory=screenshots_directory) for o in step['Detections']]
    data = {
        'name': step['SubStep'],
        'procedure': step['Procedure'],
        'criteria': step.get('Criteria'),
        'observations': observations,
    }
    return hodgepodge.helpers.dict_to_dataclass(data, Step)


def parse_observation(data, screenshots_directory=None):
    screenshots = [
        parse_screenshot(s, screenshots_directory=screenshots_directory) for s in data.get('Screenshots', [])
    ]
    data = {
        'type': data['DetectionType'],
        'note': data['DetectionNote'],
        'footnotes': data.get('Footnotes', []),
        'modifiers': data.get('Modifiers', []),
        'screenshots': screenshots,
    }
    return hodgepodge.helpers.dict_to_dataclass(data, Observation)


def parse_screenshot(data, screenshots_directory=None):
    path = data['ScreenshotName']
    if screenshots_directory:
        path = os.path.join(screenshots_directory, path)

    data = {
        'path': path,
        'caption': data.get('ScreenshotCaption'),
    }
    return hodgepodge.helpers.dict_to_dataclass(data, Screenshot)


def parse_vendor_and_group_from_path(path):
    matches = _RE_VENDOR_AND_GROUP.match(os.path.basename(path))
    if matches:
        vendor, group_name = matches.groups()
    else:
        vendor, group_name = None, None
        logger.warning("Failed to parse group and vendor from path: %s", path)
    return vendor, group_name
