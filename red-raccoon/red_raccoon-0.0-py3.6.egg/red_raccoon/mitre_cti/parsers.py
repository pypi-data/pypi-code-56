"""
The following module contains parsers for parsing data from different MITRE Cyber Threat
Intelligence (CTI) repositories (e.g. MITRE ATT&CK, MITRE CAPEC).
"""

import copy
import logging

import hodgepodge.helpers
import red_raccoon.helpers
import red_raccoon.stix.parsers

from hodgepodge.helpers import ensure_type
from red_raccoon.mitre_cti import MITRE_ATTACK_ENTERPRISE, MITRE_ATTACK_PRE_ATTACK, \
    MITRE_ATTACK_MOBILE, MATRIX, TACTIC

from red_raccoon.mitre_cti.types import Tactic, EnterpriseTechnique, MobileTechnique, \
    PreAttackTechnique, MarkingDefinition, Matrix, Tool, Malware, Mitigation, Relationship, \
    KillChainPhase, Group, Identity, ExternalReference

from red_raccoon.stix import ATTACK_PATTERN as TECHNIQUE, INTRUSION_SET as GROUP, \
    COURSE_OF_ACTION as MITIGATION, MARKING_DEFINITION, MALWARE, TOOL, IDENTITY, RELATIONSHIP

logger = logging.getLogger(__name__)


def _parse_base_object(data, ignore_revoked=False, ignore_deprecated=False, remove_citations=False,
                       remove_html_tags=False, remove_markdown_links=False):

    data = red_raccoon.stix.parsers.stix2_to_dict(data, include_optional_defaults=True)

    #: Lookup the ID of the object.
    object_id = data['id']

    #: Optionally ignore revoked objects.
    if ignore_revoked and data.get('revoked', False):
        logger.debug("Ignoring revoked object: %s", object_id)
        return None

    #: Optionally ignore deprecated objects.
    if ignore_deprecated and data.get('x_mitre_deprecated', data.get('deprecated', False)):
        logger.debug("Ignoring deprecated object: %s", object_id)
        return None

    #: Translate RFC 3339 object creation timestamp into an epoch timestamp.
    created = data.get('created')
    if created is not None:
        data['created'] = hodgepodge.helpers.parse_timestamp(created)

    #: Translate RFC 3339 object modification timestamp into an epoch timestamp.
    modified = data.get('modified')
    if modified is not None:
        data['modified'] = hodgepodge.helpers.parse_timestamp(modified)

    #: "Clean" all text fields.
    data = _clean_base_object_text_fields(
        data=data,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags
    )
    return data


def _clean_base_object_text_fields(data, remove_citations, remove_markdown_links, remove_html_tags):
    for key, value in copy.copy(data).items():
        if isinstance(value, str):
            data[key] = _clean_text(
                text=value,
                remove_citations=remove_citations,
                remove_markdown_links=remove_markdown_links,
                remove_html_tags=remove_html_tags,
            )
    return data


def parse_identity(data, ignore_deprecated=False, ignore_revoked=False, remove_citations=False,
                   remove_markdown_links=False, remove_html_tags=False):
    """
    Parses the provided 'identity' object.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, Identity)


def parse_marking_definition(data, ignore_deprecated=False, ignore_revoked=False,
                             remove_citations=False, remove_markdown_links=False,
                             remove_html_tags=False):
    """
    Parses the provided 'marking-definition' object.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, MarkingDefinition)


def parse_matrix(data, ignore_deprecated=False, ignore_revoked=False, remove_citations=False,
                 remove_markdown_links=False, remove_html_tags=False):
    """
    Parses the provided 'x-mitre-matrix' object.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, Matrix)


def parse_tactic(data, ignore_deprecated=False, ignore_revoked=False, remove_citations=False,
                 remove_markdown_links=False, remove_html_tags=False):
    """
    Parses the provided 'x-mitre-tactic' object.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, Tactic)


def parse_technique(data, ignore_deprecated=False, ignore_revoked=False, remove_citations=False,
                    remove_markdown_links=False, remove_html_tags=False):
    """
    Parses the provided 'attack-pattern' object.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None

    #: Use the set of external references associated with this object to determine its matrix.
    external_references = parse_external_references(data['external_references'])
    source_name = next(e.source_name for e in external_references if e.is_mitre_attack())

    #: If this is a MITRE ATT&CK Enterprise technique.
    if source_name == MITRE_ATTACK_ENTERPRISE:
        data = parse_enterprise_technique(data)

    #: If this is a MITRE ATT&CK Mobile technique.
    elif source_name == MITRE_ATTACK_MOBILE:
        data = parse_mobile_technique(data)

    #: If this is a MITRE ATT&CK Pre-ATT&CK technique.
    elif source_name == MITRE_ATTACK_PRE_ATTACK:
        data = parse_pre_attack_technique(data)

    #: Otherwise.
    else:
        logger.error("Failed to parse attack-pattern object with unknown type: %s", data['id'])
        data = None
    return data


def parse_enterprise_technique(data, ignore_deprecated=False, ignore_revoked=False,
                               remove_citations=False, remove_markdown_links=False,
                               remove_html_tags=False):
    """
    Parses the provided 'attack-pattern' object from the MITRE ATT&CK Enterprise matrix.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, EnterpriseTechnique)


def parse_mobile_technique(data, ignore_deprecated=False, ignore_revoked=False,
                           remove_citations=False, remove_markdown_links=False,
                           remove_html_tags=False):
    """
    Parses the provided 'attack-pattern' object from the MITRE ATT&CK Mobile matrix.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, MobileTechnique)


def parse_pre_attack_technique(data, ignore_deprecated=False, ignore_revoked=False,
                               remove_citations=False, remove_markdown_links=False,
                               remove_html_tags=False):
    """
    Parses the provided 'attack-pattern' object from the MITRE ATT&CK Pre-ATT&CK matrix.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, PreAttackTechnique)


def parse_group(data, ignore_deprecated=False, ignore_revoked=False, remove_citations=False,
                remove_markdown_links=False, remove_html_tags=False):
    """
    Parses the provided 'intrusion-set' object.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, Group)


def parse_tool(data, ignore_deprecated=False, ignore_revoked=False, remove_citations=False,
               remove_markdown_links=False, remove_html_tags=False):
    """
    Parses the provided 'tool' object.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, Tool)


def parse_malware(data, ignore_deprecated=False, ignore_revoked=False, remove_citations=False,
                  remove_markdown_links=False, remove_html_tags=False):
    """
    Parses the provided 'malware' object.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, Malware)


def parse_mitigation(data, ignore_deprecated=False, ignore_revoked=False, remove_citations=False,
                     remove_markdown_links=False, remove_html_tags=False):
    """
    Parses the provided 'course-of-action' object.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, Mitigation)


def parse_relationship(data, ignore_deprecated=False, ignore_revoked=False, remove_citations=False,
                       remove_markdown_links=False, remove_html_tags=False):
    """
    Parses the provided 'relationship' object.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    data = _parse_base_object(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    if not data:
        return None
    return hodgepodge.helpers.dict_to_dataclass(data, Relationship)


def parse_external_reference(data):
    """
    Parses the provided external reference.

    :param data: a dictionary representing an external reference.
    :return: a dataclass object.
    """
    data = ensure_type(data, dict)
    return red_raccoon.stix.parsers.stix2_to_dataclass(data=data, data_class=ExternalReference)


def parse_external_references(data):
    """
    Parses the provided sequence of external references.

    :param data: a list of dictionaries representing a sequence of external references.
    :return: a list of dataclass objects.
    """
    external_references = []
    for external_reference in data:
        external_references.append(parse_external_reference(external_reference))
    return external_references


def parse_kill_chain_phase(data):
    """
    Parses the provided kill chain phase.

    :param data: a dictionary representing a kill chain phase.
    :return: a dataclass object.
    """
    data = ensure_type(data, dict)
    return red_raccoon.stix.parsers.stix2_to_dataclass(data=data, data_class=KillChainPhase)


def parse_kill_chain_phases(data):
    """
    Parses the provided sequence of kill chain phases.

    :param data: a list of dictionaries representing a sequence of kill chain phases.
    :return: a dataclass object.
    """
    kill_chain_phases = []
    for kill_chain_phase in data:
        kill_chain_phases.append(parse_kill_chain_phase(kill_chain_phase))
    return kill_chain_phases


_PARSER_MAP = {
    IDENTITY: parse_identity,
    MARKING_DEFINITION: parse_marking_definition,
    MATRIX: parse_matrix,
    TACTIC: parse_tactic,
    TECHNIQUE: parse_technique,
    MITIGATION: parse_mitigation,
    GROUP: parse_group,
    MALWARE: parse_malware,
    TOOL: parse_tool,
    RELATIONSHIP: parse_relationship,
}


def parse_object(data, ignore_deprecated=False, ignore_revoked=False, remove_citations=False,
                 remove_markdown_links=False, remove_html_tags=False):

    """
    Parses the provided object.

    :param data: a dictionary.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    parser = _PARSER_MAP.get(data['type'])
    if not parser:
        logger.error("No parser available for '%s' objects - skipping", data['type'])
        return None

    data = parser(
        data=data,
        ignore_deprecated=ignore_deprecated,
        ignore_revoked=ignore_revoked,
        remove_citations=remove_citations,
        remove_markdown_links=remove_markdown_links,
        remove_html_tags=remove_html_tags,
    )
    return data


def parse_object_stream(stream, ignore_deprecated=False, ignore_revoked=False,
                        remove_citations=False, remove_markdown_links=False,
                        remove_html_tags=False):
    """
    Parses the provided sequence of objects.

    :param stream: a sequence of dictionaries.
    :param ignore_deprecated: whether or not to ignore objects where 'x_mitre_deprecated' is True.
    :param ignore_revoked: whether or not to ignore objects where 'revoked' is True.
    :param remove_citations: whether or not to remove citations in text fields.
    :param remove_markdown_links: whether or not to remove markdown links in text fields.
    :param remove_html_tags: whether or not to remove HTML tags from text fields.
    :return: a dataclass object.
    """
    for data in stream:
        data = parse_object(
            data=data,
            ignore_deprecated=ignore_deprecated,
            ignore_revoked=ignore_revoked,
            remove_citations=remove_citations,
            remove_markdown_links=remove_markdown_links,
            remove_html_tags=remove_html_tags,
        )
        if data:
            yield data


def _clean_text(text, remove_citations, remove_markdown_links, remove_html_tags):
    if text:

        #: Optionally remove citations.
        if remove_citations:
            text = red_raccoon.helpers.remove_citations(text)

        #: Optionally remove markdown links.
        if remove_markdown_links:
            text = red_raccoon.helpers.remove_markdown_links(text)

        #: Optionally remove HTML tags.
        if remove_html_tags:
            text = red_raccoon.helpers.remove_html_tags(text)

        #: Replace non-ASCII characters.
        text = text.replace('\xa0', '')     #: Non-breaking space.

        #: Remove trailing/leading whitespace.
        text = text.strip()

        #: Remove double whitespace (i.e. replace "  " with " ").
        if '  ' in text:
            text = ' '.join(text.split())

    return text
