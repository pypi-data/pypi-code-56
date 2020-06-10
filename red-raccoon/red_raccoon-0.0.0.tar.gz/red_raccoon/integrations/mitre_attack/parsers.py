import logging

import hodgepodge.helpers
import red_raccoon.helpers
import red_raccoon.integrations.stix.parsers

from hodgepodge.helpers import ensure_type

from red_raccoon.integrations.mitre_attack import MITRE_ATTACK_ENTERPRISE, MITRE_ATTACK_PRE_ATTACK, \
    MITRE_ATTACK_MOBILE, MATRIX, TACTIC

from red_raccoon.integrations.mitre_attack.types import Tactic, EnterpriseTechnique, MobileTechnique, \
    PreAttackTechnique, MarkingDefinition, Matrix, Tool, Malware, Mitigation, Relationship, KillChainPhase, Group, \
    Identity, ExternalReference

from red_raccoon.integrations.stix import ATTACK_PATTERN as TECHNIQUE, INTRUSION_SET as GROUP, \
    COURSE_OF_ACTION as MITIGATION, MARKING_DEFINITION, MALWARE, TOOL, IDENTITY, RELATIONSHIP

import dateutil.parser
import re

logger = logging.getLogger(__name__)

_RE_MARKDOWN_LINK = re.compile(r'\[(.+?)]\((https*:\/\/.*?)\)')
_RE_CITATION = re.compile(r'(\([cC]itation: .*?\))')


def clean_text_field(text):
    if text:
        text = text.replace('\n\n', ' ').strip()
        text = remove_citations(text)
        text = remove_markdown_links(text)
        text = remove_html_tags(text)
    return text


def remove_markdown_links(text):
    if text:
        text = ensure_type(text, str)
        matches = re.findall(_RE_MARKDOWN_LINK, text)
        for title, url in matches:
            markdown_link = "[{}]({})".format(title, url)
            text = text.replace(markdown_link, title)
    return text


def remove_citations(text):
    if text and "Citation" in text:
        for citation in re.findall(_RE_CITATION, text):
            text = text.replace(citation, "")
    return text


def remove_html_tags(text):
    if text:
        tags = [
            ("<code>", "</code>")
        ]
        for opening_tag, closing_tag in tags:
            if opening_tag in text and closing_tag in text:
                text = text.replace(opening_tag, "")
                text = text.replace(closing_tag, "")
    return text


def parse_object(data):
    data = red_raccoon.integrations.stix.parsers.stix2_to_dict(data)

    #: Translate timestamps from STIX 2.x format into epoch timestamps.
    for key in ('created', 'modified'):
        if key in data:
            value = data.get(key)
            if value is not None and isinstance(value, str):
                data[key] = dateutil.parser.isoparse(data[key]).timestamp()

    #: Lookup the appropriate parser.
    object_type = data['type']
    try:
        parser = _PARSER_MAP.get(object_type)
    except KeyError:
        logger.warning("No parser available for '%s' objects - skipping: %s", object_type, data)
        data = None
    else:
        data = parser(data)
    return data


def _parse_identity(data):
    return hodgepodge.helpers.dict_to_dataclass(data, Identity)


def _parse_marking_definition(data):
    return hodgepodge.helpers.dict_to_dataclass(data, MarkingDefinition)


def _parse_matrix(data):
    return hodgepodge.helpers.dict_to_dataclass(data, Matrix)


def _parse_tactic(data):
    return hodgepodge.helpers.dict_to_dataclass(data, Tactic)


def _parse_technique(data):
    external_references = _parse_external_references(data['external_references'])
    source_name = next(e.source_name for e in external_references if e.is_mitre_attack())

    if source_name == MITRE_ATTACK_ENTERPRISE:
        data = _parse_enterprise_technique(data)

    elif source_name == MITRE_ATTACK_MOBILE:
        data = _parse_mobile_technique(data)

    elif source_name == MITRE_ATTACK_PRE_ATTACK:
        data = _parse_pre_attack_technique(data)
    else:
        raise ValueError("Failed to parse attack-pattern object: {}".format(data['id']))
    return data


def _parse_enterprise_technique(data):
    return hodgepodge.helpers.dict_to_dataclass(data, EnterpriseTechnique)


def _parse_mobile_technique(data):
    return hodgepodge.helpers.dict_to_dataclass(data, MobileTechnique)


def _parse_pre_attack_technique(data):
    return hodgepodge.helpers.dict_to_dataclass(data, PreAttackTechnique)


def _parse_group(data):
    return hodgepodge.helpers.dict_to_dataclass(data, Group)


def _parse_tool(data):
    return hodgepodge.helpers.dict_to_dataclass(data, Tool)


def _parse_malware(data):
    return hodgepodge.helpers.dict_to_dataclass(data, Malware)


def _parse_mitigation(data):
    return hodgepodge.helpers.dict_to_dataclass(data, Mitigation)


def _parse_relationship(data):
    return hodgepodge.helpers.dict_to_dataclass(data, Relationship)


def _parse_external_reference(data):
    return red_raccoon.integrations.stix.parsers.stix2_to_dataclass(data=data, data_class=ExternalReference)


def _parse_external_references(data):
    external_references = []
    for external_reference in data:
        external_references.append(_parse_external_reference(external_reference))
    return external_references


def _parse_kill_chain_phase(data):
    return red_raccoon.integrations.stix.parsers.stix2_to_dataclass(data=data, data_class=KillChainPhase)


def _parse_kill_chain_phases(data):
    kill_chain_phases = []
    for kill_chain_phase in data:
        kill_chain_phases.append(_parse_kill_chain_phase(kill_chain_phase))
    return kill_chain_phases


_PARSER_MAP = {
    IDENTITY: _parse_identity,
    MARKING_DEFINITION: _parse_marking_definition,
    MATRIX: _parse_matrix,
    TACTIC: _parse_tactic,
    TECHNIQUE: _parse_technique,
    MITIGATION: _parse_mitigation,
    GROUP: _parse_group,
    MALWARE: _parse_malware,
    TOOL: _parse_tool,
    RELATIONSHIP: _parse_relationship,
}
