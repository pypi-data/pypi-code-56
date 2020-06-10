"""
The following module contains functionality for working with different STIX 2.x collections from the
MITRE Cyber Threat Intelligence (CTI) repository (e.g. the MITRE ATT&CK framework).
"""

import itertools
import logging

import hodgepodge.helpers
import hodgepodge.path
import red_raccoon.mitre_cti.parsers
import red_raccoon.api.stix
import red_raccoon.stix.parsers

from red_raccoon.mitre_cti import DEFAULT_MITRE_ATTACK_ENTERPRISE_URL, \
    DEFAULT_MITRE_ATTACK_MOBILE_URL, DEFAULT_MITRE_ATTACK_PRE_ATTACK_URL, \
    DEFAULT_MITRE_ATTACK_ENTERPRISE_PATH, DEFAULT_MITRE_ATTACK_MOBILE_PATH, \
    DEFAULT_MITRE_ATTACK_PRE_ATTACK_PATH, MATRIX, TACTIC, ALL_MITRE_CTI_COLLECTIONS, \
    MITRE_ATTACK_ENTERPRISE, MITRE_ATTACK_MOBILE, MITRE_ATTACK_PRE_ATTACK

from red_raccoon.mitre_cti.types import Tactic, EnterpriseTechnique, MobileTechnique, \
    PreAttackTechnique, StixObject

from red_raccoon.stix import IDENTITY, MARKING_DEFINITION, ATTACK_PATTERN as TECHNIQUE, \
    INTRUSION_SET as GROUP, COURSE_OF_ACTION as MITIGATION, MALWARE, TOOL, USES, MITIGATES

logger = logging.getLogger(__name__)


class MitreCTI:
    def __init__(self, mitre_attack_enterprise_data=None,
                 mitre_attack_enterprise_path=DEFAULT_MITRE_ATTACK_ENTERPRISE_PATH,
                 mitre_attack_enterprise_url=DEFAULT_MITRE_ATTACK_ENTERPRISE_URL,
                 mitre_attack_mobile_data=None,
                 mitre_attack_mobile_path=DEFAULT_MITRE_ATTACK_MOBILE_PATH,
                 mitre_attack_mobile_url=DEFAULT_MITRE_ATTACK_MOBILE_URL,
                 mitre_attack_pre_attack_data=None,
                 mitre_attack_pre_attack_path=DEFAULT_MITRE_ATTACK_PRE_ATTACK_PATH,
                 mitre_attack_pre_attack_url=DEFAULT_MITRE_ATTACK_PRE_ATTACK_URL,
                 prefer_offline_repositories=True, ignore_deprecated=True, ignore_revoked=True,
                 remove_citations=True, remove_markdown_links=True, remove_html_tags=True):

        #: Whether or not to ignore deprecated/revoked objects.
        self._ignore_deprecated = ignore_deprecated
        self._ignore_revoked = ignore_revoked

        #: Whether or not to remove citations, markdown links, and HTML tags from text fields.
        self._remove_citations = remove_citations
        self._remove_markdown_links = remove_markdown_links
        self._remove_html_tags = remove_html_tags

        #: Whether or not to prefer offline repositories.
        self._prefer_offline_repositories = prefer_offline_repositories

        #: MITRE ATT&CK Enterprise matrix.
        self._mitre_attack_enterprise_data = mitre_attack_enterprise_data
        self._mitre_attack_enterprise_path = mitre_attack_enterprise_path
        self._mitre_attack_enterprise_url = mitre_attack_enterprise_url

        #: MITRE ATT&CK Mobile matrix.
        self._mitre_attack_mobile_data = mitre_attack_mobile_data
        self._mitre_attack_mobile_path = mitre_attack_mobile_path
        self._mitre_attack_mobile_url = mitre_attack_mobile_url

        #: MITRE ATT&CK Pre-ATT&CK matrix.
        self._mitre_attack_pre_attack_data = mitre_attack_pre_attack_data
        self._mitre_attack_pre_attack_path = mitre_attack_pre_attack_path
        self._mitre_attack_pre_attack_url = mitre_attack_pre_attack_url

        #: MITRE ATT&CK test_data sources (loaded on-demand).
        self._mitre_attack_enterprise_client = None
        self._mitre_attack_mobile_client = None
        self._mitre_attack_pre_attack_client = None

    @property
    def mitre_attack_enterprise_client(self):
        client = self._mitre_attack_enterprise_client
        if client is None:
            client = self._mitre_attack_enterprise_client = red_raccoon.api.stix.get_default_client(
                url=self._mitre_attack_enterprise_url,
                data=self._mitre_attack_enterprise_data,
                path=self._mitre_attack_enterprise_path,
                tags=[MITRE_ATTACK_ENTERPRISE],
            )
        return client

    @property
    def mitre_attack_mobile_client(self):
        api = self._mitre_attack_mobile_client
        if api is None:
            api = self._mitre_attack_mobile_client = red_raccoon.api.stix.get_default_client(
                url=self._mitre_attack_mobile_url,
                data=self._mitre_attack_mobile_data,
                path=self._mitre_attack_mobile_path,
                tags=[MITRE_ATTACK_MOBILE],
            )
        return api

    @property
    def mitre_attack_pre_attack_client(self):
        api = self._mitre_attack_pre_attack_client
        if api is None:
            api = self._mitre_attack_pre_attack_client = red_raccoon.api.stix.get_default_client(
                url=self._mitre_attack_pre_attack_url,
                data=self._mitre_attack_pre_attack_data,
                path=self._mitre_attack_pre_attack_path,
                tags=[MITRE_ATTACK_PRE_ATTACK],
            )
        return api

    def get_mitre_attack_tactic_by_id(self, tactic_id):
        return self.get_object(object_id=tactic_id, object_types={TACTIC})

    def get_mitre_attack_technique_by_id(self, technique_id):
        return self.get_object(object_id=technique_id, object_types={TECHNIQUE})

    def get_mitre_attack_group_by_id(self, group_id):
        return self.get_object(object_id=group_id, object_types={GROUP})

    def get_mitre_attack_tool_by_id(self, software_id):
        return self.get_object(object_id=software_id, object_types={TOOL})

    def get_mitre_attack_malware_by_id(self, software_id):
        return self.get_object(object_id=software_id, object_types={MALWARE})

    def get_mitre_attack_software_by_id(self, software_id):
        return self.get_object(object_id=software_id, object_types={TOOL, MALWARE})

    def get_mitre_attack_mitigation_by_id(self, mitigation_id):
        return self.get_object(object_id=mitigation_id, object_types={MITIGATION})

    def get_mitre_attack_matrices(self):
        return self.get_objects(object_types={MATRIX})

    def get_mitre_attack_identities(self):
        return self.get_objects(object_types={IDENTITY})

    def get_mitre_attack_marking_definitions(self):
        return self.get_objects(object_types={MARKING_DEFINITION})

    def get_mitre_attack_tactics(self, tactic_ids=None, tactic_names=None, technique_ids=None,
                                 technique_names=None, group_ids=None, group_names=None,
                                 software_ids=None, software_names=None, mitigation_ids=None,
                                 mitigation_names=None, platforms=None, collections=None):

        #: Lookup tactics.
        tactics = self.get_objects(
            object_ids=tactic_ids,
            object_names=tactic_names,
            object_types={TACTIC},
            collections=collections,
        )

        #: Filter tactics by platform, related techniques, groups, software, and/or mitigations.
        if tactics and (platforms or technique_ids or technique_names or group_ids or group_names
                        or software_ids or software_names or mitigation_ids or mitigation_names):

            #: Lookup techniques matching the provided filters.
            techniques = self.get_mitre_attack_techniques(
                tactic_ids=tactic_ids,
                tactic_names=tactic_names,
                technique_ids=technique_ids,
                technique_names=technique_names,
                group_ids=group_ids,
                group_names=group_names,
                software_ids=software_ids,
                software_names=software_names,
                mitigation_ids=mitigation_ids,
                mitigation_names=mitigation_names,
                platforms=platforms,
                collections=collections,
            )
            tactics = list(filter_tactics_by_techniques(tactics, techniques))

        return tactics

    def get_mitre_attack_techniques(self, technique_ids=None, technique_names=None, tactic_ids=None,
                                    tactic_names=None, group_ids=None, group_names=None,
                                    software_ids=None, software_names=None, mitigation_ids=None,
                                    mitigation_names=None, platforms=None, collections=None):

        #: Determine which STIX 2.x API client to use.
        client = self._get_client_by_collection_names(collections)

        #: Lookup techniques.
        techniques = self._get_objects(
            client=client,
            object_ids=technique_ids,
            object_names=technique_names,
            object_types={TECHNIQUE},
        )

        #: Filter techniques by platform.
        if techniques and platforms:
            techniques = list(filter_objects_by_platform(techniques, platforms))

        #: Filter techniques by related tactics.
        if techniques and (tactic_ids or tactic_names):
            tactics = self.get_mitre_attack_tactics(
                tactic_ids=tactic_ids,
                tactic_names=tactic_names,
                technique_ids=technique_ids,
                technique_names=technique_names,
                group_ids=group_ids,
                group_names=group_names,
                software_ids=software_ids,
                software_names=software_names,
                mitigation_ids=mitigation_ids,
                mitigation_names=mitigation_names,
                platforms=platforms,
                collections=collections,
            )
            techniques = list(filter_techniques_by_tactics(techniques, tactics))

        #: Filter techniques by related groups, software, and/or mitigations.
        if techniques and (group_ids or group_names or software_ids or software_names
                           or mitigation_ids or mitigation_names):

            source_objects = set()
            source_object_types = set()
            source_names = set()
            relationship_types = set()

            #: Add groups to the query.
            if group_ids or group_names:
                source_objects |= hodgepodge.helpers.as_set(group_ids)
                source_names |= hodgepodge.helpers.as_set(group_names)
                source_object_types.add(GROUP)
                relationship_types.add(USES)

            #: Add malware, and tools to the query.
            if software_ids or software_names:
                source_objects |= hodgepodge.helpers.as_set(software_ids)
                source_names |= hodgepodge.helpers.as_set(software_names)
                source_object_types.add(MALWARE)
                source_object_types.add(TOOL)
                relationship_types.add(USES)

            #: Add mitigations to the query.
            if mitigation_ids or mitigation_names:
                source_objects |= hodgepodge.helpers.as_set(mitigation_ids)
                source_names |= hodgepodge.helpers.as_set(mitigation_names)
                source_object_types.add(MITIGATION)
                relationship_types.add(MITIGATES)

            #: Lookup related techniques.
            source_object_internal_ids = self._get_object_internal_ids(
                client=client,
                object_ids=source_objects,
                object_names=source_names,
                object_types=source_object_types,
            )
            target_object_internal_ids = client.get_target_object_internal_ids_by_source_objects(
                source_object_internal_ids=source_object_internal_ids,
                source_object_types=source_object_types,
                target_object_internal_ids=[t.id for t in techniques],
                target_object_types={TECHNIQUE},
                relationship_types=relationship_types,
            )
            techniques = [t for t in techniques if t.id in target_object_internal_ids]

        return techniques

    def get_mitre_attack_groups(self, group_ids=None, group_names=None, tactic_ids=None,
                                tactic_names=None, technique_ids=None, technique_names=None,
                                software_ids=None, software_names=None, mitigation_ids=None,
                                mitigation_names=None, platforms=None, collections=None):

        #: Determine which STIX 2.x API client to use.
        client = self._get_client_by_collection_names(collections)

        #: Lookup groups.
        groups = self._get_objects(
            client=client,
            object_ids=group_ids,
            object_names=group_names,
            object_types={GROUP},
        )

        #: Filter groups by related tactics, techniques, or mitigations or platform.
        if groups and (tactic_ids or tactic_names or technique_ids or technique_names
                       or mitigation_ids or mitigation_names or platforms):

            techniques = self.get_mitre_attack_techniques(
                tactic_ids=tactic_ids,
                tactic_names=tactic_names,
                technique_ids=technique_ids,
                technique_names=technique_names,
                group_ids=group_ids,
                group_names=group_names,
                software_ids=software_ids,
                software_names=software_names,
                mitigation_ids=mitigation_ids,
                mitigation_names=mitigation_names,
                platforms=platforms,
                collections=collections,
            )
            source_object_internal_ids = client.get_source_object_internal_ids_by_target_objects(
                source_object_internal_ids={g.id for g in groups},
                target_object_internal_ids={t.id for t in techniques},
                source_object_types={GROUP},
                relationship_types={USES},
                target_object_types={TECHNIQUE},
            )
            groups = [g for g in groups if g.id in source_object_internal_ids]

        #: Filter groups by related software or platform.
        if groups and (software_ids or software_names or platforms):
            software = self.get_mitre_attack_software(
                tactic_ids=tactic_ids,
                tactic_names=tactic_names,
                technique_ids=technique_ids,
                technique_names=technique_names,
                group_ids=group_ids,
                group_names=group_names,
                software_ids=software_ids,
                software_names=software_names,
                mitigation_ids=mitigation_ids,
                mitigation_names=mitigation_names,
                platforms=platforms,
                collections=collections,
            )
            source_object_internal_ids = client.get_source_object_internal_ids_by_target_objects(
                source_object_internal_ids={g.id for g in groups},
                target_object_internal_ids={t.id for t in software},
                source_object_types={GROUP},
                relationship_types={USES},
                target_object_types={MALWARE, TOOL},
            )
            groups = [g for g in groups if g.id in source_object_internal_ids]

        return groups

    def get_mitre_attack_tools(self, software_ids=None, software_names=None, tactic_ids=None,
                               tactic_names=None, technique_ids=None, technique_names=None,
                               group_ids=None, group_names=None, mitigation_ids=None,
                               mitigation_names=None, platforms=None, collections=None):

        software = self.get_mitre_attack_software(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            group_ids=group_ids,
            group_names=group_names,
            software_ids=software_ids,
            software_names=software_names,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
            platforms=platforms,
            collections=collections,
        )
        return list(filter(lambda o: o.type == TOOL, software))

    def get_mitre_attack_malware(self, software_ids=None, software_names=None, tactic_ids=None,
                                 tactic_names=None, technique_ids=None, technique_names=None,
                                 group_ids=None, group_names=None, mitigation_ids=None,
                                 mitigation_names=None, platforms=None, collections=None):

        software = self.get_mitre_attack_software(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            group_ids=group_ids,
            group_names=group_names,
            software_ids=software_ids,
            software_names=software_names,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
            platforms=platforms,
            collections=collections,
        )
        return list(filter(lambda o: o.type == MALWARE, software))

    def get_mitre_attack_software(self, software_ids=None, software_names=None, tactic_ids=None,
                                  tactic_names=None, technique_ids=None, technique_names=None,
                                  group_ids=None, group_names=None, mitigation_ids=None,
                                  mitigation_names=None, platforms=None, collections=None):

        #: Determine which STIX 2.x API client to use.
        client = self._get_client_by_collection_names(collections)

        #: Lookup malware families/tools.
        software = self._get_objects(
            client=client,
            object_ids=software_ids,
            object_names=software_names,
            object_types={MALWARE, TOOL},
        )

        #: Filter malware by platform.
        if software and platforms:
            software = list(filter_objects_by_platform(software, platforms))

        #: Filter malware by related tactics, techniques, or mitigations.
        if software and (tactic_ids or tactic_names or technique_ids or technique_names or
                         mitigation_ids or mitigation_names):

            techniques = self.get_mitre_attack_techniques(
                tactic_ids=tactic_ids,
                tactic_names=tactic_names,
                technique_ids=technique_ids,
                technique_names=technique_names,
                group_ids=group_ids,
                group_names=group_names,
                software_ids=software_ids,
                software_names=software_names,
                mitigation_ids=mitigation_ids,
                mitigation_names=mitigation_names,
                platforms=platforms,
                collections=collections,
            )
            source_object_internal_ids = client.get_source_object_internal_ids_by_target_objects(
                source_object_internal_ids=[o.id for o in software],
                target_object_internal_ids=[o.id for o in techniques],
                source_object_types={MALWARE, TOOL},
                relationship_types={USES},
                target_object_types={TECHNIQUE},
            )
            software = [o for o in software if o.id in source_object_internal_ids]

        #: Filter malware by related groups.
        if software and (group_ids or group_names):
            source_object_internal_ids = self._get_object_internal_ids(
                client=client,
                object_ids=group_ids,
                object_names=group_names,
                object_types={GROUP},
            )
            target_object_internal_ids = client.get_target_object_internal_ids_by_source_objects(
                source_object_internal_ids=source_object_internal_ids,
                target_object_internal_ids=[s.id for s in software],
                source_object_types={GROUP},
                relationship_types={USES},
                target_object_types={MALWARE, TOOL}
            )
            software = [s for s in software if s.id in target_object_internal_ids]

        return software

    def get_mitre_attack_mitigations(self, mitigation_ids=None, mitigation_names=None,
                                     tactic_ids=None, tactic_names=None, technique_ids=None,
                                     technique_names=None, group_ids=None, group_names=None,
                                     software_ids=None, software_names=None, platforms=None,
                                     collections=None):

        #: Determine which STIX 2.x API client to use.
        client = self._get_client_by_collection_names(collections)

        #: Lookup mitigations.
        mitigations = self._get_objects(
            client=client,
            object_ids=mitigation_ids,
            object_names=mitigation_names,
            object_types={MITIGATION},
        )

        #: Filter mitigations by platform, or by related tactic, technique, group, or software.
        if mitigations and (tactic_ids or tactic_names or technique_ids or technique_names or
                            group_ids or group_names or software_ids or software_names or
                            platforms):

            techniques = self.get_mitre_attack_techniques(
                tactic_ids=tactic_ids,
                tactic_names=tactic_names,
                technique_ids=technique_ids,
                technique_names=technique_names,
                group_ids=group_ids,
                group_names=group_names,
                software_ids=software_ids,
                software_names=software_names,
                mitigation_ids=mitigation_ids,
                mitigation_names=mitigation_names,
                platforms=platforms,
                collections=collections,
            )
            source_object_internal_ids = client.get_source_object_internal_ids_by_target_objects(
                source_object_internal_ids=[o.id for o in mitigations],
                target_object_internal_ids=[o.id for o in techniques],
                source_object_types={MITIGATION},
                relationship_types={MITIGATES},
                target_object_types={TECHNIQUE},
            )
            mitigations = [o for o in mitigations if o.id in source_object_internal_ids]

        return list(mitigations)

    def get_mitre_attack_directed_relationships(self, source_objects=None, source_object_types=None,
                                                target_objects=None, target_object_types=None,
                                                relationship_types=None, collections=None):

        return list(self.iter_mitre_attack_directed_relationships(
            source_objects=source_objects,
            source_object_types=source_object_types,
            target_objects=target_objects,
            target_object_types=target_object_types,
            relationship_types=relationship_types,
            collections=collections,
        ))

    def iter_mitre_attack_directed_relationships(self, source_objects=None,
                                                 source_object_types=None, source_object_names=None,
                                                 target_objects=None, target_object_types=None,
                                                 target_object_names=None, relationship_types=None,
                                                 collections=None):

        #: Determine which STIX 2.x API client to use.
        client = self._get_client_by_collection_names(collections)

        #: Normalize the set of source objects.
        if source_objects:
            source_object_internal_ids = self._get_object_internal_ids(
                client=client,
                object_ids=source_objects,
                object_types=source_object_types,
                object_names=source_object_names,
            )
        else:
            source_object_internal_ids = None

        #: Normalize the set of target objects.
        if target_objects:
            target_object_internal_ids = self._get_object_internal_ids(
                client=client,
                object_ids=target_objects,
                object_types=target_object_types,
                object_names=target_object_names,
            )
        else:
            target_object_internal_ids = None

        #: Lookup relationships.
        relationships = client.iter_directed_relationships(
            source_object_internal_ids=source_object_internal_ids,
            target_object_internal_ids=target_object_internal_ids,
            source_object_types=source_object_types,
            target_object_types=target_object_types,
            relationship_types=relationship_types,
        )
        return self._parse_object_stream(relationships)

    def get_mitre_attack_undirected_relationships(self, objects=None, object_types=None,
                                                  object_names=None, relationship_types=None,
                                                  collections=None):

        return list(self.iter_mitre_attack_undirected_relationships(
            objects=objects,
            object_types=object_types,
            object_names=object_names,
            relationship_types=relationship_types,
            collections=collections,
        ))

    def iter_mitre_attack_undirected_relationships(self, objects=None, object_types=None,
                                                   object_names=None, relationship_types=None,
                                                   collections=None):

        #: Determine which STIX 2.x API client to use.
        client = self._get_client_by_collection_names(collections)

        #: Lookup relationships.
        object_internal_ids = self._get_object_internal_ids(
            client=client,
            object_ids=objects,
            object_types=object_types,
            object_names=object_names,
        )
        relationships = client.iter_undirected_relationships(
            object_internal_ids=object_internal_ids,
            relationship_types=relationship_types,
        )
        return self._parse_object_stream(relationships)

    def get_mitre_attack_object(self, object_id=None, object_names=None, object_types=None,
                                collections=None):

        return self.get_object(
            object_id=object_id,
            object_names=object_names,
            object_types=object_types,
            collections=collections,
        )

    def get_mitre_attack_objects(self, object_ids=None, object_types=None, object_names=None,
                                 collections=None):

        return list(self.iter_mitre_attack_objects(
            object_ids=object_ids,
            object_names=object_names,
            object_types=object_types,
            collections=collections,
        ))

    def iter_mitre_attack_objects(self, object_ids=None, object_types=None, object_names=None,
                                  collections=None):

        return self.iter_objects(
            object_ids=object_ids,
            object_names=object_names,
            object_types=object_types,
            collections=collections,
        )

    def get_object(self, object_id=None, object_names=None, object_types=None, collections=None):
        client = self._get_client_by_collection_names(collections)
        return self._get_object(client, object_id, object_names, object_types)

    def _get_object(self, client, object_id, object_names, object_types):
        if object_id:
            data = client.get_object_by_id(object_id=object_id, object_types=object_types)
        else:
            data = client.get_object_by_name(object_names=object_names, object_types=object_types)
        return self._parse_object(data)

    def get_objects(self, object_ids=None, object_types=None, object_names=None, collections=None):
        client = self._get_client_by_collection_names(collections)
        return list(self._get_objects(client, object_ids, object_types, object_names))

    def _get_objects(self, client, object_ids=None, object_types=None, object_names=None):
        return list(self._iter_objects(client, object_ids, object_types, object_names))

    def iter_objects(self, object_ids=None, object_types=None, object_names=None, collections=None):
        client = self._get_client_by_collection_names(collections)
        return self._iter_objects(client, object_ids, object_types, object_names)

    def _iter_objects(self, client, object_ids=None, object_types=None, object_names=None):
        if object_ids:
            stream = client.iter_objects(
                object_ids=as_stream_of_object_ids(object_ids),
                object_types=object_types,
                object_names=object_names,
            )
        else:
            stream = client.iter_objects(object_names=object_names, object_types=object_types)
        return self._parse_object_stream(stream)

    def _get_object_internal_ids(self, client, object_ids=None, object_types=None,
                                 object_names=None):

        return list(self._iter_object_internal_ids(
            client=client,
            object_ids=object_ids,
            object_types=object_types,
            object_names=object_names,
        ))

    def _iter_object_internal_ids(self, client, object_ids=None, object_types=None,
                                  object_names=None):

        objects = self._iter_objects(
            client=client,
            object_ids=object_ids,
            object_types=object_types,
            object_names=object_names,
        )
        for obj in objects:
            yield obj.id

    def _get_client_by_collection_names(self, collections):
        clients = []

        #: Check if any unsupported collection names were passed in.
        collections = hodgepodge.helpers.as_set(collections, str)
        if not collections:
            collections = ALL_MITRE_CTI_COLLECTIONS
        else:
            unsupported_collections = collections.difference(ALL_MITRE_CTI_COLLECTIONS)
            if unsupported_collections:
                raise ValueError(
                    "Encountered {} unsupported collection(s): {} (supported: {})".format(
                        len(unsupported_collections),
                        sorted(unsupported_collections),
                        sorted(ALL_MITRE_CTI_COLLECTIONS)
                    )
                )

        #: MITRE ATT&CK Enterprise matrix.
        if MITRE_ATTACK_ENTERPRISE in collections:
            clients.append(self.mitre_attack_enterprise_client)

        #: MITRE ATT&CK Mobile matrix.
        if MITRE_ATTACK_MOBILE in collections:
            clients.append(self.mitre_attack_mobile_client)

        #: MITRE ATT&CK Pre-ATT&CK matrix.
        if MITRE_ATTACK_PRE_ATTACK in collections:
            clients.append(self.mitre_attack_pre_attack_client)

        #: If no clients were found, an invalid collection name was provided.
        if not clients:
            raise ValueError("Invalid set of collection names: {}".format(collections))

        #: If a single collection was provided, return the first client - otherwise, a composite.
        if len(clients) == 1:
            client = clients[0]
        else:
            tags = []
            for client in clients:
                for tag in client.tags:
                    if tag not in tags:
                        tags.append(tag)

            client = red_raccoon.api.stix.get_composite_client(data_sources=clients, tags=tags)
        return client

    def _parse_object(self, data):
        if not data:
            return None

        return red_raccoon.mitre_cti.parsers.parse_object(
            data=data,
            ignore_deprecated=self._ignore_deprecated,
            ignore_revoked=self._ignore_revoked,
            remove_citations=self._remove_citations,
            remove_html_tags=self._remove_html_tags,
            remove_markdown_links=self._remove_markdown_links,
        )

    def _parse_object_stream(self, stream):
        stream = red_raccoon.mitre_cti.parsers.parse_object_stream(
            stream=stream,
            ignore_deprecated=self._ignore_deprecated,
            ignore_revoked=self._ignore_revoked,
            remove_citations=self._remove_citations,
            remove_html_tags=self._remove_html_tags,
            remove_markdown_links=self._remove_markdown_links,
        )
        for obj in stream:
            yield obj


def filter_tactics_by_techniques(tactics, techniques):
    tactics = hodgepodge.helpers.as_set(tactics, expected_types=[Tactic])
    techniques = hodgepodge.helpers.as_set(techniques, expected_types=[
        EnterpriseTechnique, MobileTechnique, PreAttackTechnique
    ])

    #: Filter the provided set of tactics, and techniques by kill chain phase.
    names = set(itertools.chain.from_iterable(t.kill_chain_phase_names for t in techniques))
    for tactic in tactics:
        if tactic.kill_chain_phase_name in names:
            yield tactic


def filter_techniques_by_tactics(techniques, tactics):
    tactics = hodgepodge.helpers.as_set(tactics, expected_types=[Tactic])
    techniques = hodgepodge.helpers.as_set(techniques, expected_types=[
        EnterpriseTechnique, MobileTechnique, PreAttackTechnique
    ])

    #: Filter the provided set of tactics, and techniques by kill chain phase.
    names = {t.kill_chain_phase_name for t in tactics}
    for technique in techniques:
        if any(name in names for name in technique.kill_chain_phase_names):
            yield technique


def filter_objects_by_platform(objects, platforms):
    for obj in objects:
        if obj.platforms and obj.has_matching_platform(platforms):
            yield obj


def as_stream_of_object_ids(object_ids):
    object_ids = hodgepodge.helpers.as_set(object_ids, expected_types=[str, StixObject])
    return {o for o in object_ids if isinstance(o, str)} | \
           {o.id for o in object_ids if isinstance(o, StixObject)}
