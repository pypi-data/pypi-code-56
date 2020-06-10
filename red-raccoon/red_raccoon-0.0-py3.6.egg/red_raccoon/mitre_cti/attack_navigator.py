"""
The following module contains helper functions which can be used to generate MITRE ATT&CK Navigator
layers.
"""

from dataclasses import dataclass, field
from typing import List, Union

import logging
import dataclasses
import json

import hodgepodge.helpers

from hodgepodge.helpers import ensure_type

logger = logging.getLogger(__name__)

#: The set of supported MITRE ATT&CK matrices.
MITRE_MOBILE = "mitre-mobile"
MITRE_ENTERPRISE = "mitre-enterprise"

#: Defaults to use when creating MITRE ATT&CK Navigator layers.
DEFAULT_LAYER_NAME = "layer"
DEFAULT_LAYER_DESCRIPTION = ""
DEFAULT_LAYER_DOMAIN = MITRE_ENTERPRISE
DEFAULT_LAYER_VERSION = "2.2"

#: Example colours.
BLUE = "#0074D9"
RED = "#FF4136"
YELLOW = "#FFDC00"
GREEN = "#2ECC40"
OLIVE = "#3D9970"
GRAY = "#AAAAAA"
AQUA = "#7FDBFF"
TEAL = "#39CCCC"
LIME = "#01FF70"
ORANGE = "#FF851B"
MAROON = "#85144b"
FUCHSIA = "#F012BE"
PURPLE = "#B10DC9"
SILVER = "#DDDDDD"
NAVY = "#001F3F"
DEFAULT_COLOR = BLUE


@dataclass(frozen=True)
class Layer:
    """
    A class for representing MITRE ATT&CK Navigator layers.
    """
    name: str = DEFAULT_LAYER_NAME
    description: str = field(repr=False, default=DEFAULT_LAYER_DESCRIPTION)
    domain: str = DEFAULT_LAYER_DOMAIN
    version: str = field(repr=False, default=DEFAULT_LAYER_VERSION)
    hide_disabled: bool = field(repr=False, default=False)
    gradient: Union["Gradient", None] = field(repr=False, default=None)
    techniques: List["Technique"] = field(repr=False, default_factory=list)

    @property
    def technique_ids(self):
        technique_ids = []
        for technique in self.techniques:
            if technique.technique_id not in technique_ids:
                technique_ids.append(technique.technique_id)
        return technique_ids

    def add_technique(self, technique_id, color=DEFAULT_COLOR, enabled=True, comment=None):
        """
        Adds a MITRE ATT&CK technique ID to this layer.

        :param technique_id: the technique ID (e.g. "T1003" for "T1003: Credential Dumping").
        :param color: a string representation of the hex colour code to use (e.g. "#0074D9").
        :param enabled: True or False.
        :param comment: an optional comment to add - this comment will show up in the MITRE ATT&CK
            Navigator UI on hover.
        """
        technique_id = ensure_type(technique_id, str)
        technique = Technique(
            technique_id=technique_id,
            enabled=enabled,
            color=color,
            comment=comment,
        )
        self.techniques.append(technique)

    def add_techniques(self, technique_ids, color=DEFAULT_COLOR, enabled=True):
        """
        Adds a sequence of MITRE ATT&CK technique IDs to this layer.

        :param technique_ids: a sequence of technique IDs (e.g. ["T1003"]).
        :param color: a string representation of the hex colour code to use (e.g. "#0074D9").
        :param enabled: True or False.
        """
        for technique_id in hodgepodge.helpers.as_unique_list(technique_ids):
            technique = Technique(
                technique_id=technique_id,
                enabled=enabled,
                color=color,
            )
            if technique not in self.techniques:
                self.techniques.append(technique)

    def __len__(self):
        return len(self.techniques)

    def __iter__(self):
        for technique in self.techniques:
            yield technique


@dataclass
class Gradient:
    """
    Used to represent a colour gradient for use within a given MITRE ATT&CK Navigator layer.
    """
    colors: List[str]
    min_value: int
    max_value: int


@dataclass
class Technique:
    """
    Used to represent a MITRE ATT&CK technique for use within a given MITRE ATT&CK Navigator layer.
    """
    technique_id: str
    enabled: bool = True
    color: str = None
    comment: Union[str, None] = None
    score: Union[int, None] = None


def techniques_ids_to_layer(technique_ids, color=DEFAULT_COLOR, layer_name=DEFAULT_LAYER_NAME,
                            layer_domain=DEFAULT_LAYER_DOMAIN, layer_version=DEFAULT_LAYER_VERSION,
                            layer_description=DEFAULT_LAYER_DESCRIPTION):
    """
    Packs the provided sequence of MITRE ATT&CK technique IDs into a MITRE ATT&CK Navigator layer.

    :param technique_ids: a sequence of MITRE ATT&CK technique IDs.
    :param color: the hex colour code to assign to each of the technique IDs.
    :param layer_name: the name of the layer (e.g. "TTPs related to FIN7").
    :param layer_domain: the layer domain (e.g. "mitre-enterprise" or "mitre-mobile").
    :param layer_version: the layer version.
    :param layer_description: a description of the layer.
    :return: the dataclass object representing the generated MITRE ATT&CK Navigator layer.
    """
    layer = Layer(
        name=layer_name,
        domain=layer_domain,
        description=layer_description,
        version=layer_version,
    )
    for technique_id in technique_ids:
        layer.add_technique(technique_id=technique_id, color=color)
    return layer


def layer_as_dict(layer, convert_to_camelcase=True):
    """
    Translate the provided layer into a dictionary.

    :param layer: a dataclass object.
    :param convert_to_camelcase: if True, use camelCase key names - otherwise, use original values.
    :return: a dictionary.
    """
    layer = ensure_type(layer, Layer)
    layer = dataclasses.asdict(layer)

    #: camelCase key names are required by the MITRE ATT&CK Navigator.
    if convert_to_camelcase:
        layer = hodgepodge.helpers.dict_keys_to_camel_case(layer)
        techniques = []
        for technique in layer['techniques']:
            technique = hodgepodge.helpers.dict_keys_to_camel_case(technique)
            technique['techniqueID'] = technique.pop('techniqueId')
            techniques.append(technique)
        layer['techniques'] = techniques
    return layer


def layer_as_json(layer, convert_to_camelcase=True, indent=4, sort_keys=True):
    """
    Translate the provided layer into a JSON object.

    :param layer: a dataclass object.
    :param convert_to_camelcase: if True, use camelCase key names - otherwise, use original values.
    :param indent: the indentation level to use in the resulting JSON object.
    :param sort_keys: whether or not to sort keys in the resulting JSON object.
    :return: a JSON object.
    """
    data = layer_as_dict(layer, convert_to_camelcase=convert_to_camelcase)
    return json.dumps(data, indent=indent, sort_keys=sort_keys)


def compare_two_layers(lhs, rhs, output_layer_name=DEFAULT_LAYER_NAME,
                       output_layer_domain=DEFAULT_LAYER_DOMAIN,
                       output_layer_description=DEFAULT_LAYER_DESCRIPTION,
                       output_layer_version=DEFAULT_LAYER_VERSION,
                       lhs_color=OLIVE, rhs_color=BLUE, common_color=YELLOW):
    """
    Combines two MITRE ATT&CK Navigator layers.

    :param lhs: on the left-hand side (LHS), we have the first layer.
    :param rhs: on the right-hand side (RHS), we have the second layer.
    :param output_layer_name: the name of the output layer.
    :param output_layer_domain: the domain of the output layer (e.g. 'mitre-mobile').
    :param output_layer_description: the description of the output layer.
    :param output_layer_version: the version of the output layer.
    :param lhs_color: the color to assign to techniques only found on the LHS.
    :param rhs_color: the color to assign to techniques only found on the RHS.
    :param common_color: the color to assign to techniques on both LHS and RHS.
    :return: a dataclass object.
    """
    lhs_technique_ids = {t.technique_id for t in ensure_type(lhs, Layer).techniques}
    rhs_technique_ids = {t.technique_id for t in ensure_type(rhs, Layer).techniques}
    common_technique_ids = set.intersection(lhs_technique_ids, rhs_technique_ids)

    layer = Layer(
        name=output_layer_name,
        description=output_layer_description,
        domain=output_layer_domain,
        version=output_layer_version,
    )
    for collection in lhs, rhs:
        for technique in collection.techniques:
            if technique in layer.techniques:
                continue

            if technique.technique_id in common_technique_ids:
                color = common_color
            elif technique.technique_id in lhs_technique_ids:
                color = lhs_color
            else:
                color = rhs_color

            layer.add_technique(technique_id=technique.technique_id, color=color)

    return layer


def compare_multiple_layers(layers, gradient_lower_bound_color=AQUA,
                            gradient_upper_bound_color=NAVY,
                            output_layer_name=DEFAULT_LAYER_NAME,
                            output_layer_domain=DEFAULT_LAYER_DOMAIN,
                            output_layer_description=DEFAULT_LAYER_DESCRIPTION,
                            output_layer_version=DEFAULT_LAYER_VERSION):

    """
    Combines two or more MITRE ATT&CK Navigator layers.

    :param layers: the layers to compare.
    :param output_layer_name: the name of the output layer.
    :param output_layer_domain: the domain of the output layer (e.g. 'mitre-mobile').
    :param output_layer_description: the description of the output layer.
    :param output_layer_version: the version of the output layer.
    :param gradient_lower_bound_color: the minimum value to use within the colour gradient.
    :param gradient_upper_bound_color: the maximum value to use within the colour gradient.
    :return: a dataclass object.
    """
    layers = [ensure_type(o, Layer) for o in hodgepodge.helpers.as_list(layers)]
    if len(layers) < 2:
        raise ValueError("At least two layers are required.")
    logger.info("Comparing %d MITRE ATT&CK Navigator layers", len(layers))

    technique_ids = []
    for layer in layers:
        technique_ids.extend(layer.technique_ids)

    #: Score each technique based on how often it is observed across each of the layers.
    max_score = 0
    scores = {}
    for technique_id in technique_ids:
        if technique_id not in scores:
            score = technique_ids.count(technique_id) - 1
            scores[technique_id] = score
            max_score = max(score, max_score)

    #: Prepare the output layer.
    layer = Layer(
        name=output_layer_name,
        description=output_layer_description,
        domain=output_layer_domain,
        version=output_layer_version,
        gradient=Gradient(
            colors=[
                gradient_lower_bound_color,
                gradient_upper_bound_color,
            ],
            min_value=0,
            max_value=max_score
        ),
    )
    for technique_id, score in scores.items():
        technique = Technique(technique_id=technique_id, score=score)
        layer.techniques.append(technique)
    return layer
