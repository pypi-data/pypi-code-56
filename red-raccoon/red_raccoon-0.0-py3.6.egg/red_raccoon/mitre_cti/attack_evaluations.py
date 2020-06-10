"""
The following module contains helper functions which can be used to generate MITRE ATT&CK Navigator
layers representing the product of one, or more MITRE ATT&CK Evaluations (i.e. evaluations of how
well a particular endpoint detection & response (EDR) solution can identify, and articulate the
discovery of different MITRE ATT&CK TTPs).
"""

from typing import List, Union
from dataclasses import dataclass

import fnmatch
import json
import logging
import tabulate

import hodgepodge.helpers
import hodgepodge.path

from hodgepodge.helpers import ensure_type
from red_raccoon.mitre_cti.attack_navigator import Layer, BLUE, GREEN

logger = logging.getLogger(__name__)

#: The default table format to use when rendering text-based tables with the tabulate module.
DEFAULT_TABLE_FORMAT = "psql"


@dataclass(frozen=True)
class Evaluation:
    technique_ids: List[str]
    tests: List["Test"]
    description: Union[str, None] = None

    @property
    def detections(self):
        detections = []
        for test in self.tests:
            for step in test.steps:
                for observation in step.observations:
                    if observation.is_detection():
                        detections.append(observation)
        return detections

    @property
    def number_of_detections(self):
        length = 0
        for test in self.tests:
            for step in test.steps:
                for observation in step.observations:
                    if observation.is_detection():
                        length += 1
        return length

    @property
    def number_of_screenshots(self):
        length = 0
        for test in self.tests:
            for step in test.steps:
                if step.has_screenshots():
                    length += len(step.screenshots)
        return length

    def __iter__(self):
        for test in self.tests:
            yield test

    def __len__(self):
        return len(self.tests)


@dataclass(frozen=True)
class Test:
    technique_id: str
    technique_name: str
    tactic_name: str
    steps: List["TestStep"]

    def has_detections(self):
        """
        Checks if any detections were observed when executing this test case.

        :return: True or False.
        """
        for step in self.steps:
            for detection in step.observations:
                if detection.is_detection():
                    return True
        return False

    def has_screenshots(self):
        """
        Checks if there are any screenshots associated with this test case.

        :return: True or False.
        """
        for step in self.steps:
            if step.has_screenshots():
                return True
        return False

    def __iter__(self):
        for step in self.steps:
            yield step

    def __len__(self):
        return len(self.steps)


@dataclass(frozen=True)
class TestStep:
    step: str
    procedure: str
    screenshots: List["Screenshot"]
    observations: List["Observation"]

    @property
    def detection_categories(self):
        return sorted({o.category for o in self.observations})

    def has_detections(self):
        return any(o.is_detection() for o in self.observations)

    def has_screenshots(self):
        """
        Checks if there are any screenshots associated with this step in the execution of a given
        test case.

        :return: True or False.
        """
        return len(self.screenshots) != 0

    def __iter__(self):
        for observation in self.observations:
            yield observation

    def __len__(self):
        return len(self.observations)


@dataclass(frozen=True)
class Observation:
    category: str
    description: Union[str, None]

    def is_detection(self):
        """
        Checks if this observation was a detection (e.g. via an endpoint detection & response (EDR)
        solution such as Windows Defender ATP, or CrowdStrike Falcon).

        :return: True or False.
        """
        return self.category != 'None'


@dataclass(frozen=True)
class Screenshot:
    filename: str
    description: Union[str, None]


def parse_evaluation(data):
    """
    Parses a JSON object representing the product of a particular MITRE ATT&CK Evaluation (e.g. for
    how well CrowdStrike Falcon could detect, and articulate the detection of TTPs related to APT3).

    :param data: a JSON object.
    :return: a dataclass object.
    """
    data = ensure_type(data, dict)

    technique_ids = [key for key in data.keys() if fnmatch.fnmatch(key, "T*")]
    if not technique_ids:
        raise ValueError("MITRE ATT&CK Evaluation did not contain any MITRE ATT&CK techniques")

    tests = []
    for technique_id in technique_ids:
        test = parse_test(technique_id, data[technique_id])
        tests.append(test)

    return Evaluation(technique_ids=technique_ids, tests=tests)


def parse_test(technique_id, data):
    """
    Parses an individual test case from a given MITRE ATT&CK Evaluation.

    :param technique_id: the technique ID associated with this test case (e.g. "T1003").
    :param data: a dictionary containing the results of a particular test case.
    :return: a dataclass object.
    """
    technique_id = ensure_type(technique_id, str)
    data = ensure_type(data, dict)

    technique_name = data['TechniqueName']
    tactic_name = data['TacticGroup']

    steps = []
    for step, step_data in data['Steps'].items():
        step = parse_test_step(step, step_data)
        steps.append(step)

    return Test(
        technique_id=technique_id,
        technique_name=technique_name,
        tactic_name=tactic_name,
        steps=steps,
    )


def parse_test_step(step, step_data):
    """
    Parses a step for a given MITRE ATT&CK Evaluation test case.

    :param step: the name of the test case step.
    :param step_data: a dictionary containing the result of a particular step in a given test case.
    :return: a dataclass object.
    """
    step = ensure_type(step, str)
    step_data = ensure_type(step_data, dict)
    procedure = step_data['Procedure']

    #: A test consists of multiple steps, and detections are captured on a per-step basis.
    observations = []
    for observation in step_data['DetectionCategories']:
        for category, description in observation.items():
            if not (category or description):
                continue

            observation = Observation(category=category.strip(), description=description.strip())
            observations.append(observation)

    #: A test may include screenshots.
    screenshots = []
    for filename, description in step_data['Screenshots'].items():
        if filename or description:
            screenshot = Screenshot(
                filename=filename,
                description=description.strip() or None
            )
            screenshots.append(screenshot)

    return TestStep(
        step=step,
        procedure=procedure,
        observations=observations,
        screenshots=screenshots,
    )


def read(path):
    """
    Reads the content of a MITRE ATT&CK Evaluation at the provided path.

    :param path: the path to a file containing the output of a particular MITRE ATT&CK Evaluation.
    :return: a dataclass object which contains each of the test cases from the evaluation.
    """
    path = hodgepodge.path.realpath(path)
    with open(path) as file_pointer:
        data = json.load(file_pointer)
    return parse_evaluation(data)


def read_evaluation_as_table(path, table_format=DEFAULT_TABLE_FORMAT):
    """
    Reads the content of a MITRE ATT&CK Evaluation at the provided path, and formats the output of
    the evaluation as a table.

    :param path: the path to a file containing the output of a particular MITRE ATT&CK Evaluation.
    :param table_format: the output format to use.
    :return: a dataclass object which contains each of the test cases from the evaluation.
    """
    evaluation = read(path)
    return as_table(evaluation, table_format=table_format)


def read_evaluation_as_mitre_attack_navigator_layer(path, layer_name=None):
    """
    Reads the content of a MITRE ATT&CK Evaluation at the provided path, and formats the output of
    the evaluation as a MITRE ATT&CK Navigator layer.

    :param path: the path to a file containing the output of a particular MITRE ATT&CK Evaluation.
    :param layer_name: the name of the resulting MITRE ATT&CK Navigator layer.
    :return: a dataclass object which contains each of the test cases from the evaluation.
    """
    evaluation = read(path)
    return as_mitre_attack_navigator_layer(evaluation, layer_name=layer_name)


def as_table(evaluation, table_format=DEFAULT_TABLE_FORMAT):
    """
    Translates the output of the provided MITRE ATT&CK Evaluation into a tabular format using the
    'tabulate' module.

    :param evaluation: a dataclass object representing the output of a MITRE ATT&CK Evaluation.
    :param table_format: the output format to use.
    :return: a string representation of the provided evaluation in tabular format.
    """
    evaluation = ensure_type(evaluation, Evaluation)
    headers = ['ID', 'Name', 'Category']
    rows = []
    for test in sorted(evaluation.tests, key=lambda t: t.technique_id):
        for step in test.steps:
            for detection in step.detections:
                row = (test.technique_id, test.technique_name, detection.category)
                if row not in rows:
                    rows.append(row)

    return tabulate.tabulate(rows, headers=headers, tablefmt=table_format)


def as_mitre_attack_navigator_layer(evaluation, layer_name=None,
                                    color_for_detected_techniques=GREEN,
                                    color_for_undetected_techniques=BLUE):
    """
    Translates the output of the provided MITRE ATT&CK Evaluation into a MITRE ATT&CK Navigator
    layer.

    :param evaluation: a dataclass object representing the output of a MITRE ATT&CK Evaluation.
    :param layer_name: the name of the resulting MITRE ATT&CK Navigator layer.
    :param color_for_detected_techniques: the color to use for detected techniques.
    :param color_for_undetected_techniques: the color to use for undetected techniques.
    :return: a dataclass object which represents a MITRE ATT&CK Navigator layer.
    """
    evaluation = ensure_type(evaluation, Evaluation)

    layer = Layer(name=layer_name)
    for test in evaluation.tests:
        technique_id = test.technique_id

        #: Determine which types of detections were observed.
        categories = []
        for step in test.steps:
            for observation in step:
                if observation.is_detection() and observation.category not in categories:
                    categories.append(observation.category)

        #: If at least one detection was observed for this TTP, make note of the detection category.
        if categories:
            comment = ', '.join(sorted(categories))
        else:
            comment = None

        #: Color the MITRE ATT&CK Navigator cell for this TTP by detection status.
        if test.has_detections():
            layer.add_technique(
                technique_id=technique_id, color=color_for_detected_techniques, comment=comment
            )
        else:
            layer.add_technique(
                technique_id=technique_id, color=color_for_undetected_techniques, comment=comment
            )

    return layer
