"""
This module contains classes used to represent data from the MITRE Cyber Threat Intelligence (CTI)
repository (e.g. the MITRE ATT&CK framework, or the MITRE CAPEC framework).
"""

from typing import List, Dict, Union
from dataclasses import dataclass, field
from red_raccoon.mitre_cti import MITRE_ATTACK_ENTERPRISE, MITRE_ATTACK_MOBILE, \
    MITRE_ATTACK_PRE_ATTACK, MITRE_CAPEC, MITRE_CWE, NIST_MOBILE_THREAT_CATALOGUE

import red_raccoon.stix.parsers
import red_raccoon.platforms
import hodgepodge.helpers

MATRIX = "x-mitre-matrix"
TACTIC = "x-mitre-tactic"


@dataclass(eq=False, frozen=True)
class Matrix:
    """
    This class is used to represent STIX 2.x 'x-mitre-tactic objects'.
    """
    id: str
    type: str
    name: str
    created: float
    created_by_ref: Union[str, None]
    modified: Union[float, None]
    tactic_refs: List[str]

    #: Optional string fields.
    description: str = None

    #: Optional list fields.
    object_marking_refs: List[str] = field(default_factory=list)
    external_references: List["ExternalReference"] = field(default_factory=list)

    def __eq__(self, other):
        return isinstance(other, type(self)) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)


@dataclass(frozen=True)
class ExternalReference:
    """
    This class is used to represent STIX 2.x external references.
    """
    source_name: str

    #: Optional string fields.
    url: str = None
    external_id: str = None
    description: str = None

    def has_url(self):
        """
        Checks if this external reference includes a link to an external source (e.g. a website,
        or a PDF file).

        :return: True, or False.
        """
        return bool(self.url)

    def has_external_id(self):
        """
        Checks if this external reference includes an external ID (e.g. an external ID from the
        MITRE ATT&CK framework).

        :return: True, or False.
        """
        return bool(self.external_id)

    def is_mitre(self):
        """
        Checks if this is a reference to the MITRE ATT&CK, CAPEC, or CWE frameworks.

        :return: True, or False.
        """
        return self.is_mitre_attack() or self.is_mitre_capec() or self.is_mitre_cwe()

    def is_mitre_attack(self):
        """
        Checks if this is a reference to the MITRE ATT&CK framework.

        :return: True, or False.
        """
        return \
            self.is_mitre_attack_enterprise() or \
            self.is_mitre_attack_mobile() or \
            self.is_mitre_attack_pre_attack()

    def is_mitre_attack_enterprise(self):
        """
        Checks if this is a reference to the MITRE ATT&CK Enterprise matrix.

        :return: True, or False.
        """
        return self.source_name == MITRE_ATTACK_ENTERPRISE

    def is_mitre_attack_mobile(self):
        """
        Checks if this is a reference to the MITRE ATT&CK Mobile matrix.

        :return: True, or False.
        """
        return self.source_name == MITRE_ATTACK_MOBILE

    def is_mitre_attack_pre_attack(self):
        """
        Checks if this is a reference to the MITRE ATT&CK Pre-ATT&CK matrix.

        :return: True, or False.
        """
        return self.source_name == MITRE_ATTACK_PRE_ATTACK

    def is_mitre_capec(self):
        """
        Checks if this is a reference to the MITRE CAPEC framework.

        :return: True, or False.
        """
        return self.source_name == MITRE_CAPEC

    def is_mitre_cwe(self):
        """
        Checks if this is a reference to the MITRE CWE framework.

        :return: True, or False.
        """
        return self.source_name == MITRE_CWE

    def is_nist(self):
        """
        Checks if this is a reference to a NIST framework.

        :return: True, or False.
        """
        return self.is_nist_mobile_threat_catalogue()

    def is_nist_mobile_threat_catalogue(self):
        """
        Checks if this is a reference to the NIST Mobile Threat Catalogue.

        :return: True, or False.
        """
        return self.source_name == NIST_MOBILE_THREAT_CATALOGUE

    def is_unknown_source_with_external_id(self):
        """
        Checks if this external reference has an external reference to an unknown source.

        :return: True, or False.
        """
        if self.has_external_id():
            return not (self.is_mitre() or self.is_nist())
        return False


@dataclass(frozen=True)
class KillChainPhase:
    """
    This class is used to represent STIX 2.x kill chain phases.
    """
    kill_chain_name: str
    phase_name: str

    def is_mitre_attack(self):
        """
        Checks if this is a kill chain phase from the MITRE ATT&CK framework.

        :return: True, or False.
        """
        return \
            self.is_mitre_attack_enterprise() or \
            self.is_mitre_attack_mobile() or \
            self.is_mitre_attack_pre_attack()

    def is_mitre_attack_enterprise(self):
        """
        Checks if this is a kill chain phase from the MITRE ATT&CK Enterprise matrix.

        :return: True, or False.
        """
        return self.kill_chain_name in [MITRE_ATTACK_ENTERPRISE]

    def is_mitre_attack_mobile(self):
        """
        Checks if this is a kill chain phase from the MITRE ATT&CK Mobile matrix.

        :return: True, or False.
        """
        return self.kill_chain_name in [MITRE_ATTACK_MOBILE]

    def is_mitre_attack_pre_attack(self):
        """
        Checks if this is a kill chain phase from the MITRE ATT&CK Pre-ATT&CK matrix.

        :return: True, or False.
        """
        return self.kill_chain_name in [MITRE_ATTACK_PRE_ATTACK]

    def is_unknown_kill_chain_phase(self):
        """
        Checks if this is a kill chain phase from an unknown framework, or matrix.

        :return: True, or False.
        """
        return not self.is_mitre_attack()


@dataclass(eq=False, frozen=True)
class StixObject:
    id: str
    type: str
    created: float
    created_by_ref: Union[str, None]
    modified: Union[float, None]

    @property
    def internal_id(self):
        return self.id

    @property
    def external_id(self):
        external_id = None
        for external_reference in getattr(self, "external_references", []):
            if external_reference.is_mitre_attack():
                external_id = external_reference.external_id
        return external_id

    @property
    def deprecated(self):
        return getattr(self, "x_mitre_deprecated", False)

    def is_deprecated(self):
        """
        Checks to see if this object has been deprecated.

        :return: True or False.
        """
        return self.deprecated

    def is_revoked(self):
        """
        Checks to see if this object has been revoked.

        :return: True or False.
        """
        return getattr(self, "revoked", False)

    def __eq__(self, other):
        return isinstance(other, type(self)) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)


@dataclass(eq=False, frozen=True)
class StixDomainObject(StixObject):
    """
    This class is used to represent STIX 2.x domain objects (SDOs).
    """
    def has_matching_name(self, names):
        """
        Checks to see if this object has a matching name, or alias.

        :param names: a sequence of object names or aliases.
        :return: True, or False.
        """
        patterns = hodgepodge.helpers.as_set(names)

        #: Lookup each of the names associated with this object.
        name = getattr(self, "name", None)
        if not name:
            return False

        names = {name}
        aliases = getattr(self, "aliases", getattr(self, "x_mitre_aliases", []))
        if aliases:
            names |= set(aliases)

        #: Return True if this object has a matching name, or alias and False otherwise.
        for name in names:
            if hodgepodge.helpers.string_matches_any_pattern(name, patterns, case_sensitive=False):
                return True
        return False


@dataclass(eq=False, frozen=True)
class Identity(StixDomainObject):
    """
    This class is used to represent STIX 2.x 'identity' objects.
    """
    name: str
    identity_class: str

    #: Optional list fields.
    object_marking_refs: List[str] = field(default_factory=list)

    def is_organization(self):
        """
        Checks to see if this identity object refers to an organization.

        :return: True, or False.
        """
        return self.identity_class == "organization"

    def has_unknown_identity_class(self):
        """
        Checks to see if this identity object refers to an entity with an unknown identity class.

        :return: True, or False.
        """
        return not self.is_organization()


@dataclass(eq=False, frozen=True)
class MarkingDefinition(StixDomainObject):
    """
    This class is used to represent STIX 2.x 'marking-definition' objects.
    """
    definition_type: str
    definition: Dict[str, str]

    def is_statement(self):
        """
        Checks to see if this marking definition is a statement (e.g. a copyright statement).

        :return: True, or False.
        """
        return self.definition_type == "statement"

    def is_tlp(self):
        """
        Checks to see if this marking definition refers to a Traffic Light Protocol (TLP) marking.

        :return: True, or False.
        """
        return self.definition_type == "tlp"

    def is_tlp_white(self):
        """
        Checks to see if this marking definition refers to TLP:WHITE.

        :return: True, or False.
        """
        return self.is_tlp() and self.definition[self.definition_type] == "white"

    def is_tlp_green(self):
        """
        Checks to see if this marking definition refers to TLP:GREEN.

        :return: True, or False.
        """
        return self.is_tlp() and self.definition[self.definition_type] == "green"

    def is_tlp_amber(self):
        """
        Checks to see if this marking definition refers to TLP:AMBER.

        :return: True, or False.
        """
        return self.is_tlp() and self.definition[self.definition_type] == "amber"

    def is_tlp_red(self):
        """
        Checks to see if this marking definition refers to TLP:RED.

        :return: True, or False.
        """
        return self.is_tlp() and self.definition[self.definition_type] == "red"

    def has_unknown_definition_type(self):
        """
        Checks to see if this marking definition has an unknown definition type.

        :return: True, or False.
        """
        return not (self.is_statement() or self.is_tlp())


@dataclass(eq=False, frozen=True)
class Tactic(StixDomainObject):
    """
    This class is used to represent STIX 2.x 'x-mitre-tactic' objects.
    """
    name: str
    x_mitre_shortname: str

    #: Optional boolean fields.
    revoked: bool = False
    x_mitre_deprecated: bool = False

    #: Optional string fields.
    description: str = None

    #: Optional list fields.
    object_marking_refs: List[str] = field(default_factory=list)
    external_references: List[ExternalReference] = field(default_factory=list)

    @property
    def shortname(self):
        return self.x_mitre_shortname

    @property
    def external_id(self):
        external_id = None
        for external_reference in self.external_references:
            if external_reference.is_mitre_attack():
                external_id = external_reference.external_id
                break
        return external_id

    @property
    def kill_chain_phase_name(self):
        return self.shortname


@dataclass(eq=False, frozen=True)
class _Technique(StixDomainObject):
    name: str

    #: Optional boolean fields.
    revoked: bool = False
    x_mitre_deprecated: bool = False

    #: Optional string fields.
    x_mitre_version: str = None
    description: str = None

    #: Optional list fields.
    x_mitre_platforms: List[str] = field(default_factory=list)
    x_mitre_contributors: List[str] = field(default_factory=list)
    kill_chain_phases: List[KillChainPhase] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    object_marking_refs: List[str] = field(default_factory=list)
    external_references: List[ExternalReference] = field(default_factory=list)

    @property
    def mitre_version(self):
        return self.x_mitre_version

    @property
    def contributors(self):
        return self.x_mitre_contributors

    @property
    def kill_chain_phase_names(self):
        return [p.phase_name for p in self.kill_chain_phases]

    @property
    def platforms(self):
        return self.x_mitre_platforms

    def has_matching_platform(self, platforms):
        """
        Checks to see if this object has a matching platform.

        :param platforms: a sequence of OS types, or platforms (e.g. ["macOS", "Linux", "Windows"]).
        :return: True, or False.
        """
        return red_raccoon.platforms.has_matching_platform(self.platforms, platforms)

    def applies_to_current_platform(self):
        """
        Checks to see if this object applies to the current platform (i.e. "windows", "linux", or
        "macos").

        :return: True, or False.
        """
        return red_raccoon.platforms.list_includes_current_platform(self.platforms)

    def applies_to_linux(self):
        """
        Checks to see if this object applies to Linux systems.

        :return: True, or False.
        """
        return red_raccoon.platforms.list_includes_linux(self.platforms)

    def applies_to_macos(self):
        """
        Checks to see if this object applies to macOS systems.

        :return: True, or False.
        """
        return red_raccoon.platforms.list_includes_macos(self.platforms)

    def applies_to_posix(self):
        """
        Checks to see if this object applies to Linux, or macOS systems (i.e. POSIX systems).

        :return: True, or False.
        """
        return red_raccoon.platforms.list_includes_posix(self.platforms)

    def applies_to_windows(self):
        """
        Checks to see if this object applies to Windows systems.

        :return: True, or False.
        """
        return red_raccoon.platforms.list_includes_windows(self.platforms)


@dataclass(eq=False, frozen=True)
class EnterpriseTechnique(_Technique):
    """
    This class is used to represent STIX 2.x 'attack-pattern' objects from the 'mitre-attack'
    collection from the MITRE CTI repository.
    """
    #: Optional boolean fields.
    x_mitre_remote_support: bool = False
    x_mitre_network_requirements: bool = False

    #: Optional string fields.
    x_mitre_detection: str = None

    #: Optional list fields.
    x_mitre_data_sources: List[str] = field(default_factory=list)
    x_mitre_defense_bypassed: List[str] = field(default_factory=list)
    x_mitre_effective_permissions: List[str] = field(default_factory=list)
    x_mitre_permissions_required: List[str] = field(default_factory=list)
    x_mitre_system_requirements: List[str] = field(default_factory=list)
    x_mitre_impact_type: List[str] = field(default_factory=list)

    @property
    def external_id(self):
        external_id = None
        for external_reference in self.external_references:
            if external_reference.is_mitre_attack_enterprise():
                external_id = external_reference.external_id
                break
        return external_id

    @property
    def remote_support(self):
        return self.x_mitre_remote_support

    @property
    def network_requirements(self):
        return self.x_mitre_network_requirements

    @property
    def detection(self):
        return self.x_mitre_detection

    @property
    def data_sources(self):
        return self.x_mitre_data_sources

    @property
    def defenses_bypassed(self):
        return self.x_mitre_defense_bypassed

    @property
    def effective_permissions(self):
        return self.x_mitre_effective_permissions

    @property
    def permissions_required(self):
        return self.x_mitre_permissions_required

    @property
    def system_requirements(self):
        return self.x_mitre_system_requirements

    @property
    def impact_types(self):
        return self.x_mitre_impact_type

    def is_used_for_impact(self):
        """
        Checks to see if this MITRE ATT&CK technique is used for impact.

        :return: True, or False.
        """
        for kill_chain_phase in self.kill_chain_phases:
            if kill_chain_phase.is_mitre_attack() and kill_chain_phase.phase_name == 'impact':
                return True
        return False

    def has_confidentiality_impact(self):
        """
        Checks to see if this MITRE ATT&CK technique has an impact on confidentiality.

        :return: True, or False.
        """
        return self.is_used_for_impact() and "Confidentiality" in self.impact_types

    def has_integrity_impact(self):
        """
        Checks to see if this MITRE ATT&CK technique has an impact on integrity.

        :return: True, or False.
        """
        return self.is_used_for_impact() and "Integrity" in self.impact_types

    def has_availability_impact(self):
        """
        Checks to see if this MITRE ATT&CK technique has an impact on availability.

        :return: True, or False.
        """
        return self.is_used_for_impact() and "Availability" in self.impact_types


@dataclass(eq=False, frozen=True)
class MobileTechnique(_Technique):
    """
    This class is used to represent STIX 2.x 'attack-pattern' objects from the 'mitre-mobile-attack'
    collection from the MITRE CTI repository.
    """
    #: Optional string fields.
    x_mitre_old_attack_id: str = None
    x_mitre_detection: str = None

    #: Optional list fields.
    x_mitre_tactic_type: List[str] = field(default_factory=list)

    @property
    def external_id(self):
        external_id = None
        for external_reference in self.external_references:
            if external_reference.is_mitre_attack_mobile():
                external_id = external_reference.external_id
                break
        return external_id

    @property
    def old_attack_id(self):
        return self.x_mitre_old_attack_id

    @property
    def detection(self):
        return self.x_mitre_detection

    @property
    def tactic_types(self):
        return self.x_mitre_tactic_type

    def requires_device_access(self):
        """
        Checks to see if this MITRE ATT&CK technique requires device access.

        :return: True, or False.
        """
        return 'Post-Adversary Device Access' in self.tactic_types

    def does_not_require_device_access(self):
        """
        Checks to see if this MITRE ATT&CK technique does not require device access.

        :return: True, or False.
        """
        return \
            self.requires_device_access() is False or \
            'Without Adversary Device Access' in self.tactic_types


@dataclass(eq=False, frozen=True)
class PreAttackTechnique(_Technique):
    """
    This class is used to represent STIX 2.x 'attack-pattern' objects from the 'mitre-pre-attack'
    collection from the MITRE CTI repository.
    """
    #: Optional string fields.
    x_mitre_old_attack_id: str = None
    x_mitre_detectable_by_common_defenses: str = None
    x_mitre_detectable_by_common_defenses_explanation: str = None
    x_mitre_difficulty_for_adversary: str = None
    x_mitre_difficulty_for_adversary_explanation: str = None

    @property
    def external_id(self):
        external_id = None
        for external_reference in self.external_references:
            if external_reference.is_mitre_attack_pre_attack():
                external_id = external_reference.external_id
                break
        return external_id

    @property
    def old_attack_id(self):
        return self.x_mitre_old_attack_id

    @property
    def detectable_by_common_defenses(self):
        return self.x_mitre_detectable_by_common_defenses

    @property
    def detectable_by_common_defenses_explanation(self):
        return self.x_mitre_detectable_by_common_defenses_explanation

    @property
    def difficulty_for_adversary(self):
        return self.x_mitre_difficulty_for_adversary

    @property
    def difficulty_for_adversary_explanation(self):
        return self.difficulty_for_adversary_explanation

    def is_detectable_by_common_defenses(self):
        """
        Checks to see if this MITRE ATT&CK technique is detectable by common defenses based on
        information from the MITRE ATT&CK framework.

        :return: True, or False.
        """
        return self.detectable_by_common_defenses == 'Yes'

    def is_not_detectable_by_common_defenses(self):
        """
        Checks to see if this MITRE ATT&CK technique is not detectable by common defenses based on
        information from the MITRE ATT&CK framework.

        :return: True, or False.
        """
        return self.detectable_by_common_defenses == 'No'

    def is_partially_detectable_by_common_defenses(self):
        """
        Checks to see if this MITRE ATT&CK technique is partially detectable by common defenses
        based on information from the MITRE ATT&CK framework.

        If something is partially detectable, a subset of the activity can be detected by common
        defenses, or the activity can only be observed indirectly.

        :return: True, or False.
        """
        return self.detectable_by_common_defenses == 'Partial'

    def increases_difficulty_for_adversary(self):
        """
        Checks to see if this MITRE ATT&CK technique significantly increases the technical
        complexity of an attack for an adversary.

        :return: True, or False.
        """
        return self.difficulty_for_adversary == 'Yes'

    def does_not_increase_difficulty_for_adversary(self):
        """
        Checks to see if this MITRE ATT&CK technique significantly increases the technical
        complexity of attacks for an adversary.

        :return: True, or False.
        """
        return not self.increases_difficulty_for_adversary()


@dataclass(eq=False, frozen=True)
class Mitigation(StixDomainObject):
    """
    This class is used to represent STIX 2.x 'course-of-action' objects.
    """
    name: str

    #: Optional boolean fields.
    revoked: bool = False
    x_mitre_deprecated: bool = False

    #: Optional string fields.
    description: str = None
    x_mitre_version: str = None
    x_mitre_old_attack_id: str = None

    #: Optional list fields.
    object_marking_refs: List[str] = field(default_factory=list)
    external_references: List[ExternalReference] = field(default_factory=list)

    @property
    def mitre_version(self):
        return self.x_mitre_version

    @property
    def old_attack_id(self):
        return self.x_mitre_old_attack_id


@dataclass(eq=False, frozen=True)
class Group(StixDomainObject):
    """
    This class is used to represent STIX 2.x 'intrusion-set' objects.
    """
    name: str

    #: Optional boolean fields.
    revoked: bool = False
    x_mitre_deprecated: bool = False

    #: Optional string fields.
    description: str = None
    x_mitre_version: str = None

    #: Optional list fields.
    x_mitre_contributors: List[str] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    object_marking_refs: List[str] = field(default_factory=list)
    external_references: List[ExternalReference] = field(default_factory=list)

    @property
    def mitre_version(self):
        return self.x_mitre_version

    @property
    def contributors(self):
        return self.x_mitre_contributors


@dataclass(eq=False, frozen=True)
class _Software(StixDomainObject):
    """
    This class is used as a base class for representing STIX 2.x 'tool' and 'malware objects.
    """
    name: str

    #: Optional boolean fields.
    revoked: bool = False
    x_mitre_deprecated: bool = False

    #: Optional string fields.
    description: str = None
    x_mitre_version: str = None
    x_mitre_old_attack_id: str = None

    #: Optional list fields.
    x_mitre_aliases: List[str] = field(default_factory=list)
    x_mitre_contributors: List[str] = field(default_factory=list)
    x_mitre_platforms: List[str] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    object_marking_refs: List[str] = field(default_factory=list)
    external_references: List[ExternalReference] = field(default_factory=list)

    @property
    def mitre_version(self):
        return self.x_mitre_version

    @property
    def old_attack_id(self):
        return self.x_mitre_old_attack_id

    @property
    def aliases(self):
        return self.x_mitre_aliases

    @property
    def contributors(self):
        return self.x_mitre_contributors

    @property
    def platforms(self):
        return self.x_mitre_platforms

    def has_matching_platform(self, platforms):
        """
        Checks to see if this object has a matching platform.

        :param platforms: a sequence of OS types, or platforms (e.g. ["macOS", "Linux", "Windows"]).
        :return: True, or False.
        """
        return red_raccoon.platforms.has_matching_platform(self.platforms, platforms)

    def applies_to_current_platform(self):
        """
        Checks to see if this object applies to the current platform (i.e. "windows", "linux", or
        "macos").

        :return: True, or False.
        """
        return red_raccoon.platforms.list_includes_current_platform(self.platforms)

    def applies_to_linux(self):
        """
        Checks to see if this object applies to Linux systems.

        :return: True, or False.
        """
        return red_raccoon.platforms.list_includes_linux(self.platforms)

    def applies_to_macos(self):
        """
        Checks to see if this object applies to macOS systems.

        :return: True, or False.
        """
        return red_raccoon.platforms.list_includes_macos(self.platforms)

    def applies_to_posix(self):
        """
        Checks to see if this object applies to Linux, or macOS systems (i.e. POSIX systems).

        :return: True, or False.
        """
        return red_raccoon.platforms.list_includes_posix(self.platforms)

    def applies_to_windows(self):
        """
        Checks to see if this object applies to Windows systems.

        :return: True, or False.
        """
        return red_raccoon.platforms.list_includes_windows(self.platforms)


@dataclass(eq=False, frozen=True)
class Malware(_Software):
    """
    This class is used to represent STIX 2.x 'malware' objects.
    """


@dataclass(eq=False, frozen=True)
class Tool(_Software):
    """
    This class is used to represent STIX 2.x 'tool' objects.
    """


@dataclass(eq=False, frozen=True)
class Relationship(StixObject):
    """
    This class is used to represent STIX 2.x 'relationship' objects.
    """
    relationship_type: str
    source_ref: str
    target_ref: str

    #: Optional string fields.
    description: str = None

    #: Optional list fields.
    external_references: List[ExternalReference] = field(default_factory=list)
    object_marking_refs: List[str] = field(default_factory=list)

    @property
    def src(self):
        return self.source_ref

    @property
    def src_type(self):
        return red_raccoon.stix.parsers.get_type_from_id(self.source_ref)

    @property
    def dst(self):
        return self.target_ref

    @property
    def dst_type(self):
        return red_raccoon.stix.parsers.get_type_from_id(self.target_ref)

    def is_usage(self):
        """
        Checks to see if this relationship represents a usage between one object and another.

        :return: True, or False.
        """
        return self.relationship_type == 'uses'

    def is_mitigation(self):
        """
        Checks to see if this relationship represents a mitigation between one object and another.

        :return: True, or False.
        """
        return self.relationship_type == 'mitigates'

    def is_revocation(self):
        """
        Checks to see if this relationship represents a revocation between one object and another.

        :return: True, or False.
        """
        return self.relationship_type == 'revoked-by'

    def has_unknown_relationship_type(self):
        """
        Checks to see if this relationship has an unknown relationship type.

        :return: True, or False.
        """
        return not (self.is_usage() or self.is_mitigation() or self.is_revocation())
