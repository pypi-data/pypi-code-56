from typing import List, Dict, Union
from dataclasses import dataclass, field
from red_raccoon.integrations.mitre_attack import MITRE_ATTACK_ENTERPRISE, MITRE_ATTACK_MOBILE, \
    MITRE_ATTACK_PRE_ATTACK, MITRE_CAPEC, MITRE_CWE, NIST_MOBILE_THREAT_CATALOGUE

import red_raccoon.integrations.stix.parsers
import red_raccoon.platforms
import hodgepodge.helpers

MATRIX = "x-mitre-matrix"
TACTIC = "x-mitre-tactic"


@dataclass(frozen=True)
class ExternalReference:
    source_name: str

    #: Optional string fields.
    url: str = None
    external_id: str = None
    description: str = field(repr=False, default=None)

    def has_url(self):
        return bool(self.url)

    def has_external_id(self):
        return bool(self.external_id)

    def is_mitre(self):
        return self.is_mitre_attack() or self.is_mitre_capec() or self.is_mitre_cwe()

    def is_mitre_attack(self):
        return \
            self.is_mitre_attack_enterprise() or \
            self.is_mitre_attack_mobile() or \
            self.is_mitre_attack_pre_attack()

    def is_mitre_attack_enterprise(self):
        return self.source_name == MITRE_ATTACK_ENTERPRISE

    def is_mitre_attack_mobile(self):
        return self.source_name == MITRE_ATTACK_MOBILE

    def is_mitre_attack_pre_attack(self):
        return self.source_name == MITRE_ATTACK_PRE_ATTACK

    def is_mitre_capec(self):
        return self.source_name == MITRE_CAPEC

    def is_mitre_cwe(self):
        return self.source_name == MITRE_CWE

    def is_nist(self):
        return self.is_nist_mobile_threat_catalogue()

    def is_nist_mobile_threat_catalogue(self):
        return self.source_name == NIST_MOBILE_THREAT_CATALOGUE

    def is_unknown_source_with_external_id(self):
        if self.has_external_id():
            return not (self.is_mitre() or self.is_nist())
        return False


@dataclass(frozen=True)
class KillChainPhase:
    kill_chain_name: str
    phase_name: str

    @property
    def name(self):
        return self.phase_name

    def is_mitre(self):
        return self.is_mitre_attack()

    def is_mitre_attack(self):
        return \
            self.is_mitre_attack_enterprise() or \
            self.is_mitre_attack_mobile() or \
            self.is_mitre_attack_pre_attack()

    def is_mitre_attack_enterprise(self):
        return self.kill_chain_name in [MITRE_ATTACK_ENTERPRISE]

    def is_mitre_attack_mobile(self):
        return self.kill_chain_name in [MITRE_ATTACK_MOBILE]

    def is_mitre_attack_pre_attack(self):
        return self.kill_chain_name in [MITRE_ATTACK_PRE_ATTACK]

    def is_unknown_kill_chain_phase(self):
        return not self.is_mitre()


@dataclass(eq=False, frozen=True)
class StixObject:
    id: str
    type: str
    created_by_ref: Union[str, None]
    created: float
    modified: Union[float, None]

    @property
    def internal_id(self):
        return self.id

    @property
    def external_id(self):
        external_id = None
        for external_reference in getattr(self, "external_references", []):
            if external_reference.is_mitre():
                external_id = external_reference.external_id
        return external_id

    @property
    def last_modified(self):
        return self.modified

    @property
    def deprecated(self):
        return getattr(self, "x_mitre_deprecated", False)

    def is_deprecated(self):
        return self.deprecated

    def is_revoked(self):
        return getattr(self, "revoked", False)

    def __eq__(self, other):
        return isinstance(other, type(self)) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)


@dataclass(eq=False, frozen=True)
class StixDomainObject(StixObject):
    def has_matching_name(self, names):
        patterns = hodgepodge.helpers.as_set(names, expected_types=[str])
        patterns |= {hodgepodge.helpers.camel_case_to_snake_case(pattern) for pattern in patterns}
        patterns |= {hodgepodge.helpers.snake_case_to_camel_case(pattern) for pattern in patterns}
        patterns |= {pattern.replace('_', ' ') for pattern in patterns}

        #: Lookup each of the names associated with this object.
        names = set()
        name = getattr(self, "name", None)
        if name:
            names.add(name)

        #: Lookup each of the aliases associated with this object.
        aliases = getattr(self, "aliases", getattr(self, "x_mitre_aliases", None))
        if aliases:
            names |= set(aliases)

        #: Check to see if this object has a matching [name|alias].
        if names:
            return hodgepodge.helpers.any_string_matches_any_pattern(
                strings=names,
                patterns=patterns,
                case_sensitive=False,
            )
        return False


@dataclass(eq=False, frozen=True)
class Matrix(StixObject):
    name: str
    tactic_refs: List[str]

    #: Optional string fields.
    description: str = field(repr=False, default=None)

    #: Optional list fields.
    object_marking_refs: List[str] = field(default_factory=list)
    external_references: List["ExternalReference"] = field(default_factory=list)

    def __eq__(self, other):
        return isinstance(other, type(self)) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)


@dataclass(eq=False, frozen=True)
class Identity(StixDomainObject):
    name: str
    identity_class: str

    #: Optional list fields.
    object_marking_refs: List[str] = field(repr=False, default_factory=list)

    def is_organization(self):
        return self.identity_class == "organization"

    def has_unknown_identity_class(self):
        return not self.is_organization()


@dataclass(eq=True, frozen=True)
class MarkingDefinition(StixDomainObject):
    definition_type: str
    definition: Dict[str, str]

    def is_statement(self):
        return self.definition_type == "statement"

    def is_tlp(self):
        return self.definition_type == "tlp"

    def is_tlp_white(self):
        return self.is_tlp() and self.definition[self.definition_type] == "white"

    def is_tlp_green(self):
        return self.is_tlp() and self.definition[self.definition_type] == "green"

    def is_tlp_amber(self):
        return self.is_tlp() and self.definition[self.definition_type] == "amber"

    def is_tlp_red(self):
        return self.is_tlp() and self.definition[self.definition_type] == "red"

    def has_unknown_definition_type(self):
        return not (self.is_statement() or self.is_tlp())

    def __hash__(self):
        definition = str(sorted(self.definition.items()))
        return hash((definition, self.definition_type))


@dataclass(eq=False, frozen=True)
class Tactic(StixDomainObject):
    name: str
    x_mitre_shortname: str

    #: Optional boolean fields.
    revoked: bool = False
    x_mitre_deprecated: bool = False

    #: Optional string fields.
    description: str = field(repr=False, default=None)

    #: Optional list fields.
    object_marking_refs: List[str] = field(repr=False, default_factory=list)
    external_references: List[ExternalReference] = field(repr=False, default_factory=list)

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
    description: str = field(repr=False, default=None)

    #: Optional list fields.
    x_mitre_platforms: List[str] = field(default_factory=list)
    x_mitre_contributors: List[str] = field(default_factory=list)
    kill_chain_phases: List[KillChainPhase] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    object_marking_refs: List[str] = field(repr=False, default_factory=list)
    external_references: List[ExternalReference] = field(repr=False, default_factory=list)

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
        return red_raccoon.platforms.has_matching_platform(self.platforms, platforms)

    def applies_to_current_platform(self):
        return red_raccoon.platforms.list_includes_current_platform(self.platforms)

    def applies_to_linux(self):
        return red_raccoon.platforms.list_includes_linux(self.platforms)

    def applies_to_macos(self):
        return red_raccoon.platforms.list_includes_macos(self.platforms)

    def applies_to_posix(self):
        return red_raccoon.platforms.list_includes_posix(self.platforms)

    def applies_to_windows(self):
        return red_raccoon.platforms.list_includes_windows(self.platforms)


@dataclass(eq=False, frozen=True)
class EnterpriseTechnique(_Technique):

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
    def requires_network(self):
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
        for kill_chain_phase in self.kill_chain_phases:
            if kill_chain_phase.is_mitre_attack() and kill_chain_phase.phase_name == 'impact':
                return True
        return False

    def has_confidentiality_impact(self):
        return self.is_used_for_impact() and "Confidentiality" in self.impact_types

    def has_integrity_impact(self):
        return self.is_used_for_impact() and "Integrity" in self.impact_types

    def has_availability_impact(self):
        return self.is_used_for_impact() and "Availability" in self.impact_types


@dataclass(eq=False, frozen=True)
class MobileTechnique(_Technique):

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
        return 'Post-Adversary Device Access' in self.tactic_types

    def does_not_require_device_access(self):
        return self.requires_device_access() is False or 'Without Adversary Device Access' in self.tactic_types


@dataclass(eq=False, frozen=True)
class PreAttackTechnique(_Technique):

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
        return self.detectable_by_common_defenses == 'Yes'

    def is_not_detectable_by_common_defenses(self):
        return self.detectable_by_common_defenses == 'No'

    def is_partially_detectable_by_common_defenses(self):
        return self.detectable_by_common_defenses == 'Partial'

    def increases_difficulty_for_adversary(self):
        return self.difficulty_for_adversary == 'Yes'

    def does_not_increase_difficulty_for_adversary(self):
        return not self.increases_difficulty_for_adversary()


@dataclass(eq=False, frozen=True)
class Mitigation(StixDomainObject):
    name: str

    #: Optional boolean fields.
    revoked: bool = False
    x_mitre_deprecated: bool = False

    #: Optional string fields.
    description: str = field(repr=False, default=None)
    x_mitre_version: str = None
    x_mitre_old_attack_id: str = None

    #: Optional list fields.
    object_marking_refs: List[str] = field(repr=False, default_factory=list)
    external_references: List[ExternalReference] = field(repr=False, default_factory=list)

    @property
    def mitre_version(self):
        return self.x_mitre_version

    @property
    def old_attack_id(self):
        return self.x_mitre_old_attack_id


@dataclass(eq=False, frozen=True)
class Group(StixDomainObject):
    name: str

    #: Optional boolean fields.
    revoked: bool = False
    x_mitre_deprecated: bool = False

    #: Optional string fields.
    description: str = field(repr=False, default=None)
    x_mitre_version: str = None

    #: Optional list fields.
    x_mitre_contributors: List[str] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    object_marking_refs: List[str] = field(repr=False, default_factory=list)
    external_references: List[ExternalReference] = field(repr=False, default_factory=list)

    @property
    def mitre_version(self):
        return self.x_mitre_version

    @property
    def contributors(self):
        return self.x_mitre_contributors


@dataclass(eq=False, frozen=True)
class _Software(StixDomainObject):
    name: str

    #: Optional boolean fields.
    revoked: bool = False
    x_mitre_deprecated: bool = False

    #: Optional string fields.
    description: str = field(repr=False, default=None)
    x_mitre_version: str = None
    x_mitre_old_attack_id: str = None

    #: Optional list fields.
    x_mitre_aliases: List[str] = field(default_factory=list)
    x_mitre_contributors: List[str] = field(default_factory=list)
    x_mitre_platforms: List[str] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    object_marking_refs: List[str] = field(repr=False, default_factory=list)
    external_references: List[ExternalReference] = field(repr=False, default_factory=list)

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
        return red_raccoon.platforms.has_matching_platform(self.platforms, platforms)

    def applies_to_current_platform(self):
        return red_raccoon.platforms.list_includes_current_platform(self.platforms)

    def applies_to_linux(self):
        return red_raccoon.platforms.list_includes_linux(self.platforms)

    def applies_to_macos(self):
        return red_raccoon.platforms.list_includes_macos(self.platforms)

    def applies_to_posix(self):
        return red_raccoon.platforms.list_includes_posix(self.platforms)

    def applies_to_windows(self):
        return red_raccoon.platforms.list_includes_windows(self.platforms)


@dataclass(eq=False, frozen=True)
class Malware(_Software):
    pass


@dataclass(eq=False, frozen=True)
class Tool(_Software):
    pass


@dataclass(eq=False, frozen=True)
class Relationship(StixObject):
    relationship_type: str
    source_ref: str
    target_ref: str

    #: Optional string fields.
    description: str = field(repr=False, default=None)

    #: Optional list fields.
    external_references: List[ExternalReference] = field(repr=False, default_factory=list)
    object_marking_refs: List[str] = field(repr=False, default_factory=list)

    @property
    def src(self):
        return self.source_ref

    @property
    def src_type(self):
        return red_raccoon.integrations.stix.parsers.get_type_from_internal_id(self.source_ref)

    @property
    def dst(self):
        return self.target_ref

    @property
    def dst_type(self):
        return red_raccoon.integrations.stix.parsers.get_type_from_internal_id(self.target_ref)

    def is_usage(self):
        return self.relationship_type == 'uses'

    def is_mitigation(self):
        return self.relationship_type == 'mitigates'

    def is_revocation(self):
        return self.relationship_type == 'revoked-by'

    def has_unknown_relationship_type(self):
        return not (self.is_usage() or self.is_mitigation() or self.is_revocation())
