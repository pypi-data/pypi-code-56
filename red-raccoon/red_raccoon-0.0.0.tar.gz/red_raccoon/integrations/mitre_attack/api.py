from hodgepodge.helpers import ensure_type

from red_raccoon.integrations.stix import IDENTITY, MARKING_DEFINITION, ATTACK_PATTERN, COURSE_OF_ACTION, MALWARE, \
    TOOL, INTRUSION_SET, USES, MITIGATES

from red_raccoon.integrations.mitre_attack import MATRIX, TACTIC, DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_PATH, \
    DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_URL, DEFAULT_MITRE_ATTACK_MOBILE_STIX_DATA_PATH, \
    DEFAULT_MITRE_ATTACK_MOBILE_STIX_DATA_URL, DEFAULT_MITRE_ATTACK_PRE_ATTACK_STIX_DATA_PATH, \
    DEFAULT_MITRE_ATTACK_PRE_ATTACK_STIX_DATA_URL

from red_raccoon.integrations.mitre_attack.types import MATRIX

import red_raccoon.integrations.mitre_attack.parsers as mitre_attack_parsers
import red_raccoon.integrations.stix.parsers as stix_parsers
import red_raccoon.integrations.stix.api as stix_api
import red_raccoon.log as log
import hodgepodge.helpers
import logging

logger = logging.getLogger(__name__)


class MitreAttack:
    def __init__(self, enterprise_stix_data=None,
                 enterprise_stix_data_path=DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_PATH,
                 enterprise_stix_data_url=DEFAULT_MITRE_ATTACK_ENTERPRISE_STIX_DATA_URL,
                 mobile_stix_data=None,
                 mobile_stix_data_path=DEFAULT_MITRE_ATTACK_MOBILE_STIX_DATA_PATH,
                 mobile_stix_data_url=DEFAULT_MITRE_ATTACK_MOBILE_STIX_DATA_URL,
                 pre_attack_stix_data=None,
                 pre_attack_stix_data_path=DEFAULT_MITRE_ATTACK_PRE_ATTACK_STIX_DATA_PATH,
                 pre_attack_stix_data_url=DEFAULT_MITRE_ATTACK_PRE_ATTACK_STIX_DATA_URL,
                 ignore_revoked=True, ignore_deprecated=True):

        #: MITRE ATT&CK API cli.
        self._composite_stix_client = None
        self._enterprise_stix_client = None
        self._mobile_stix_client = None
        self._pre_attack_stix_client = None

        #: MITRE ATT&CK Enterprise matrix.
        self._enterprise_stix_data = enterprise_stix_data
        self._enterprise_stix_data_path = enterprise_stix_data_path
        self._enterprise_stix_data_url = enterprise_stix_data_url

        #: MITRE ATT&CK Mobile matrix.
        self._mobile_stix_data = mobile_stix_data
        self._mobile_stix_data_path = mobile_stix_data_path
        self._mobile_stix_data_url = mobile_stix_data_url

        #: MITRE ATT&CK Pre-ATT&CK matrix.
        self._pre_attack_stix_data = pre_attack_stix_data
        self._pre_attack_stix_data_path = pre_attack_stix_data_path
        self._pre_attack_stix_data_url = pre_attack_stix_data_url

        #: Parameters related to data loading.
        self._ignore_revoked = ignore_revoked
        self._ignore_deprecated = ignore_deprecated

    @property
    def composite_stix_client(self):
        client = self._composite_stix_client
        if client is None:
            client = self._composite_stix_client = stix_api.get_composite_stix_client(
                data_sources=[
                    self.enterprise_stix_client,
                    self.mobile_stix_client,
                    self.pre_attack_stix_client,
                ],
                ignore_revoked=self._ignore_revoked,
            )
        return client

    @property
    def enterprise_stix_client(self):
        client = self._enterprise_stix_client
        if client is None:
            client = self._enterprise_stix_client = stix_api.get_stix_client(
                data=self._enterprise_stix_data,
                path=self._enterprise_stix_data_path,
                url=self._enterprise_stix_data_url,
                ignore_revoked=self._ignore_revoked,
            )
        return client

    @property
    def mobile_stix_client(self):
        client = self._mobile_stix_client
        if client is None:
            client = self._mobile_stix_client = stix_api.get_stix_client(
                data=self._mobile_stix_data,
                path=self._mobile_stix_data_path,
                url=self._mobile_stix_data_url,
                ignore_revoked=self._ignore_revoked,
            )
        return client

    @property
    def pre_attack_stix_client(self):
        client = self._pre_attack_stix_client
        if client is None:
            client = self._pre_attack_stix_client = stix_api.get_stix_client(
                data=self._pre_attack_stix_data,
                path=self._pre_attack_stix_data_path,
                url=self._pre_attack_stix_data_url,
                ignore_revoked=self._ignore_revoked,
            )
        return client

    def _get_composite_api_client(self, data_sources):
        return stix_api.get_composite_stix_client(
            data_sources=data_sources,
            ignore_revoked=self._ignore_revoked,
        )

    def get_matrices(self):
        return self._get_matrices(client=self.composite_stix_client)

    def get_identities(self):
        return self._get_identities(client=self.composite_stix_client)

    def get_marking_definitions(self):
        return self._get_marking_definitions(client=self.composite_stix_client)

    def get_tactics(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None, group_ids=None,
                    group_names=None, software_ids=None, software_names=None, mitigation_ids=None,
                    mitigation_names=None, platforms=None):

        return self._get_tactics(
            client=self.composite_stix_client,
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
        )

    def get_tactics_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_tactics_by_related_techniques(
            client=self.composite_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_tactics_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_tactics_by_related_groups(
            client=self.composite_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_tactics_by_related_software(self, software_ids=None, software_names=None):
        return self._get_tactics_by_related_software(
            client=self._get_composite_api_client([self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_tactics_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_tactics_by_related_malware(
            client=self._get_composite_api_client([self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_tactics_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_tactics_by_related_tools(
            client=self._get_composite_api_client([self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_tactics_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_tactics_by_related_mitigations(
            client=self._get_composite_api_client([self.enterprise_stix_client, self.mobile_stix_client]),
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_tactic_by_id(self, tactic_id):
        return self.get_object(object_id=tactic_id, object_types=[TACTIC])

    def get_tactic_by_name(self, tactic_name):
        return self.get_object(object_names=[tactic_name], object_types=[TACTIC])

    def get_techniques(self, technique_ids=None, technique_names=None, tactic_ids=None, tactic_names=None,
                       group_ids=None, group_names=None, software_ids=None, software_names=None, mitigation_ids=None,
                       mitigation_names=None, platforms=None):

        return self._get_techniques(
            client=self.composite_stix_client,
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
        )

    def get_techniques_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_techniques_by_related_tactics(
            client=self.composite_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_techniques_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_techniques_by_related_groups(
            client=self.composite_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_techniques_by_related_software(self, software_ids=None, software_names=None):
        return self._get_techniques_by_related_software(
            client=self._get_composite_api_client([self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_techniques_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_techniques_by_related_malware(
            client=self._get_composite_api_client([self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_techniques_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_techniques_by_related_tools(
            client=self._get_composite_api_client([self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_techniques_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_techniques_by_related_mitigations(
            client=self._get_composite_api_client([self.enterprise_stix_client, self.mobile_stix_client]),
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_technique_by_id(self, technique_id):
        return self.get_object(object_id=technique_id, object_types=[ATTACK_PATTERN])

    def get_technique_by_name(self, technique_name):
        return self.get_object(object_names=[technique_name], object_types=[ATTACK_PATTERN])

    def get_groups(self, group_ids=None, group_names=None, tactic_ids=None, tactic_names=None, technique_ids=None,
                   technique_names=None, software_ids=None, software_names=None, mitigation_ids=None,
                   mitigation_names=None, platforms=None):

        return self._get_groups(
            client=self.composite_stix_client,
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
        )

    def get_groups_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_groups_by_related_tactics(
            client=self.composite_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_groups_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_groups_by_related_techniques(
            client=self.composite_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_groups_by_related_software(self, software_ids=None, software_names=None):
        return self._get_groups_by_related_software(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_groups_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_groups_by_related_malware(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_groups_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_groups_by_related_tools(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_groups_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_groups_by_related_mitigations(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_group_by_id(self, group_id):
        return self.get_object(object_id=group_id, object_types=[INTRUSION_SET])

    def get_group_by_name(self, group_name):
        return self.get_object(object_names=[group_name], object_types=[INTRUSION_SET])

    def get_software(self, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None,
                     technique_ids=None, technique_names=None, group_ids=None, group_names=None, mitigation_ids=None,
                     mitigation_names=None, platforms=None):

        return self._get_software(
            client=self.composite_stix_client,
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
        )

    def get_software_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_software_by_related_tactics(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_software_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_software_by_related_techniques(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_software_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_software_by_related_groups(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_software_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_software_by_related_mitigations(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_software_by_id(self, software_id):
        return self.get_object(object_id=software_id, object_types=[MALWARE, TOOL])

    def get_software_by_name(self, software_name):
        return self.get_object(object_names=[software_name], object_types=[MALWARE, TOOL])

    def get_malware(self, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None,
                    technique_ids=None, technique_names=None, group_ids=None, group_names=None, mitigation_ids=None,
                    mitigation_names=None, platforms=None):

        return self._get_malware(
            client=self.composite_stix_client,
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
        )

    def get_malware_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_malware_by_related_tactics(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_malware_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_malware_by_related_techniques(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_malware_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_malware_by_related_groups(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_malware_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_malware_by_related_mitigations(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_malware_by_id(self, software_id):
        return self.get_object(object_id=software_id, object_types=[MALWARE])

    def get_malware_by_name(self, software_name):
        return self.get_object(object_names=[software_name], object_types=[MALWARE])

    def get_tools(self, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None, technique_ids=None,
                  technique_names=None, group_ids=None, group_names=None, mitigation_ids=None, mitigation_names=None,
                  platforms=None):

        return self._get_tools(
            client=self.composite_stix_client,
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
        )

    def get_tools_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_tools_by_related_tactics(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_tools_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_tools_by_related_techniques(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_tools_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_tools_by_related_groups(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_tools_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_tools_by_related_mitigations(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_tool_by_id(self, software_id):
        return self.get_object(object_id=software_id, object_types=[TOOL])

    def get_tool_by_name(self, software_name):
        return self.get_object(object_names=[software_name], object_types=[TOOL])

    def get_mitigations(self, mitigation_ids=None, mitigation_names=None, tactic_ids=None, tactic_names=None,
                        technique_ids=None, technique_names=None, group_ids=None, group_names=None, software_ids=None,
                        software_names=None, platforms=None):

        return self._get_mitigations(
            client=self.composite_stix_client,
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
        )

    def get_mitigations_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_mitigations_by_related_tactics(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_mitigations_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_mitigations_by_related_techniques(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_mitigations_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_mitigations_by_related_groups(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_mitigations_by_related_software(self, software_ids=None, software_names=None):
        return self._get_mitigations_by_related_software(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mitigations_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_mitigations_by_related_malware(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mitigations_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_mitigations_by_related_tools(
            client=self._get_composite_api_client(data_sources=[self.enterprise_stix_client, self.mobile_stix_client]),
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mitigation_by_id(self, mitigation_id):
        return self.get_object(object_id=mitigation_id, object_types=[COURSE_OF_ACTION])

    def get_mitigation_by_name(self, mitigation_name):
        return self.get_object(object_names=[mitigation_name], object_types=[COURSE_OF_ACTION])

    def get_enterprise_matrices(self):
        return self._get_matrices(client=self.enterprise_stix_client)

    def get_enterprise_identities(self):
        return self._get_identities(client=self.enterprise_stix_client)

    def get_enterprise_marking_definitions(self):
        return self._get_marking_definitions(client=self.enterprise_stix_client)

    def get_enterprise_tactics(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                               group_ids=None, group_names=None, software_ids=None, software_names=None,
                               mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_tactics(
            client=self.enterprise_stix_client,
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
        )

    def get_enterprise_tactics_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_tactics_by_related_techniques(
            client=self.enterprise_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_enterprise_tactics_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_tactics_by_related_groups(
            client=self.enterprise_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_enterprise_tactics_by_related_software(self, software_ids=None, software_names=None):
        return self._get_tactics_by_related_software(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_tactics_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_tactics_by_related_malware(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_tactics_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_tactics_by_related_tools(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_tactics_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_tactics_by_related_mitigations(
            client=self.enterprise_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_enterprise_tactic_by_id(self, tactic_id):
        return self.get_enterprise_object(object_id=tactic_id, object_types=[TACTIC])

    def get_enterprise_tactic_by_name(self, tactic_name):
        return self.get_enterprise_object(object_names=[tactic_name], object_types=[TACTIC])

    def get_enterprise_techniques(self, technique_ids=None, technique_names=None, tactic_ids=None, tactic_names=None,
                                  group_ids=None, group_names=None, software_ids=None, software_names=None,
                                  mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_techniques(
            client=self.enterprise_stix_client,
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
        )

    def get_enterprise_techniques_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_techniques_by_related_tactics(
            client=self.enterprise_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_enterprise_techniques_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_techniques_by_related_groups(
            client=self.enterprise_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_enterprise_techniques_by_related_software(self, software_ids=None, software_names=None):
        return self._get_techniques_by_related_software(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_techniques_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_techniques_by_related_malware(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_techniques_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_techniques_by_related_tools(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_techniques_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_techniques_by_related_mitigations(
            client=self.enterprise_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_enterprise_technique_by_id(self, technique_id):
        return self.get_enterprise_object(object_id=technique_id, object_types=[ATTACK_PATTERN])

    def get_enterprise_technique_by_name(self, technique_name):
        return self.get_enterprise_object(object_names=[technique_name], object_types=[ATTACK_PATTERN])

    def get_enterprise_groups(self, group_ids=None, group_names=None, tactic_ids=None, tactic_names=None,
                              technique_ids=None, technique_names=None, software_ids=None, software_names=None,
                              mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_groups(
            client=self.enterprise_stix_client,
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
        )

    def get_enterprise_groups_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_groups_by_related_tactics(
            client=self.enterprise_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_enterprise_groups_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_groups_by_related_techniques(
            client=self.enterprise_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_enterprise_groups_by_related_software(self, software_ids=None, software_names=None):
        return self._get_groups_by_related_software(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_groups_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_groups_by_related_malware(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_groups_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_groups_by_related_tools(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_groups_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_groups_by_related_mitigations(
            client=self.enterprise_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_enterprise_group_by_id(self, group_id):
        return self.get_enterprise_object(object_id=group_id, object_types=[INTRUSION_SET])

    def get_enterprise_group_by_name(self, group_name):
        return self.get_enterprise_object(object_names=[group_name], object_types=[INTRUSION_SET])

    def get_enterprise_software(self, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None,
                                technique_ids=None, technique_names=None, group_ids=None, group_names=None,
                                mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_software(
            client=self.enterprise_stix_client,
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
        )

    def get_enterprise_software_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_software_by_related_tactics(
            client=self.enterprise_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_enterprise_software_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_software_by_related_techniques(
            client=self.enterprise_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_enterprise_software_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_software_by_related_groups(
            client=self.enterprise_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_enterprise_software_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_software_by_related_mitigations(
            client=self.enterprise_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_enterprise_software_by_id(self, software_id):
        return self.get_enterprise_object(object_id=software_id, object_types=[MALWARE, TOOL])

    def get_enterprise_software_by_name(self, software_name):
        return self.get_enterprise_object(object_names=[software_name], object_types=[MALWARE, TOOL])

    def get_enterprise_malware(self, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None,
                               technique_ids=None, technique_names=None, group_ids=None, group_names=None,
                               mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_malware(
            client=self.enterprise_stix_client,
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
        )

    def get_enterprise_malware_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_malware_by_related_tactics(
            client=self.enterprise_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_enterprise_malware_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_malware_by_related_techniques(
            client=self.enterprise_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_enterprise_malware_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_malware_by_related_groups(
            client=self.enterprise_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_enterprise_malware_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_malware_by_related_mitigations(
            client=self.enterprise_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_enterprise_malware_by_id(self, software_id):
        return self.get_enterprise_object(object_id=software_id, object_types=[MALWARE])

    def get_enterprise_malware_by_name(self, software_name):
        return self.get_enterprise_object(object_names=[software_name], object_types=[MALWARE])

    def get_enterprise_tools(self, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None,
                             technique_ids=None, technique_names=None, group_ids=None, group_names=None,
                             mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_tools(
            client=self.enterprise_stix_client,
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
        )

    def get_enterprise_tools_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_tools_by_related_tactics(
            client=self.enterprise_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_enterprise_tools_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_tools_by_related_techniques(
            client=self.enterprise_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_enterprise_tools_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_tools_by_related_groups(
            client=self.enterprise_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_enterprise_tools_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_tools_by_related_mitigations(
            client=self.enterprise_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_enterprise_tool_by_id(self, software_id):
        return self.get_enterprise_object(object_id=software_id, object_types=[TOOL])

    def get_enterprise_tool_by_name(self, software_name):
        return self.get_enterprise_object(object_names=[software_name], object_types=[TOOL])

    def get_enterprise_mitigations(self, mitigation_ids=None, mitigation_names=None, tactic_ids=None,
                                   tactic_names=None, technique_ids=None, technique_names=None, group_ids=None,
                                   group_names=None, software_ids=None, software_names=None, platforms=None):

        return self._get_mitigations(
            client=self.enterprise_stix_client,
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
        )

    def get_enterprise_mitigations_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_mitigations_by_related_tactics(
            client=self.enterprise_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_enterprise_mitigations_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_mitigations_by_related_techniques(
            client=self.enterprise_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_enterprise_mitigations_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_mitigations_by_related_groups(
            client=self.enterprise_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_enterprise_mitigations_by_related_software(self, software_ids=None, software_names=None):
        return self._get_mitigations_by_related_software(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_mitigations_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_mitigations_by_related_malware(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_mitigations_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_mitigations_by_related_tools(
            client=self.enterprise_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_enterprise_mitigation_by_id(self, mitigation_id):
        return self.get_enterprise_object(object_id=mitigation_id, object_types=[COURSE_OF_ACTION])

    def get_enterprise_mitigation_by_name(self, mitigation_name):
        return self.get_enterprise_object(
            object_names=[mitigation_name],
            object_types=[COURSE_OF_ACTION],
        )

    def get_mobile_matrices(self):
        return self._get_matrices(client=self.mobile_stix_client)

    def get_mobile_identities(self):
        return self._get_identities(client=self.mobile_stix_client)

    def get_mobile_marking_definitions(self):
        return self._get_marking_definitions(client=self.mobile_stix_client)

    def get_mobile_tactics(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                           group_ids=None, group_names=None, software_ids=None, software_names=None,
                           mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_tactics(
            client=self.mobile_stix_client,
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
        )

    def get_mobile_tactics_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_tactics_by_related_techniques(
            client=self.mobile_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_mobile_tactics_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_tactics_by_related_groups(
            client=self.mobile_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_mobile_tactics_by_related_software(self, software_ids=None, software_names=None):
        return self._get_tactics_by_related_software(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_tactics_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_tactics_by_related_malware(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_tactics_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_tactics_by_related_tools(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_tactics_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_tactics_by_related_mitigations(
            client=self.mobile_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_mobile_tactic_by_id(self, tactic_id):
        return self.get_mobile_object(object_id=tactic_id, object_types=[TACTIC])

    def get_mobile_tactic_by_name(self, tactic_name):
        return self.get_mobile_object(object_names=[tactic_name], object_types=[TACTIC])

    def get_mobile_techniques(self, technique_ids=None, technique_names=None, tactic_ids=None, tactic_names=None,
                              group_ids=None, group_names=None, software_ids=None, software_names=None,
                              mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_techniques(
            client=self.mobile_stix_client,
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
        )

    def get_mobile_techniques_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_techniques_by_related_tactics(
            client=self.mobile_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_mobile_techniques_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_techniques_by_related_groups(
            client=self.mobile_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_mobile_techniques_by_related_software(self, software_ids=None, software_names=None):
        return self._get_techniques_by_related_software(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_techniques_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_techniques_by_related_malware(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_techniques_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_techniques_by_related_tools(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_techniques_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_techniques_by_related_mitigations(
            client=self.mobile_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_mobile_technique_by_id(self, technique_id):
        return self.get_mobile_object(object_id=technique_id, object_types=[ATTACK_PATTERN])

    def get_mobile_technique_by_name(self, technique_name):
        return self.get_mobile_object(object_names=[technique_name], object_types=[ATTACK_PATTERN])

    def get_mobile_groups(self, group_ids=None, group_names=None, tactic_ids=None, tactic_names=None,
                          technique_ids=None, technique_names=None, software_ids=None, software_names=None,
                          mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_groups(
            client=self.mobile_stix_client,
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
        )

    def get_mobile_groups_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_groups_by_related_tactics(
            client=self.mobile_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_mobile_groups_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_groups_by_related_techniques(
            client=self.mobile_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_mobile_groups_by_related_software(self, software_ids=None, software_names=None):
        return self._get_groups_by_related_software(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_groups_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_groups_by_related_malware(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_groups_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_groups_by_related_tools(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_groups_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_groups_by_related_mitigations(
            client=self.mobile_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_mobile_group_by_id(self, group_id):
        return self.get_mobile_object(object_id=group_id, object_types=[INTRUSION_SET])

    def get_mobile_group_by_name(self, group_name):
        return self.get_mobile_object(object_names=[group_name], object_types=[INTRUSION_SET])

    def get_mobile_software(self, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None,
                            technique_ids=None, technique_names=None, group_ids=None, group_names=None,
                            mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_software(
            client=self.mobile_stix_client,
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
        )

    def get_mobile_software_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_software_by_related_tactics(
            client=self.mobile_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_mobile_software_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_software_by_related_techniques(
            client=self.mobile_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_mobile_software_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_software_by_related_groups(
            client=self.mobile_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_mobile_software_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_software_by_related_mitigations(
            client=self.mobile_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_mobile_software_by_id(self, software_id):
        return self.get_mobile_object(object_id=software_id, object_types=[MALWARE, TOOL])

    def get_mobile_software_by_name(self, software_name):
        return self.get_mobile_object(object_names=[software_name], object_types=[MALWARE, TOOL])

    def get_mobile_malware(self, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None,
                           technique_ids=None, technique_names=None, group_ids=None, group_names=None,
                           mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_malware(
            client=self.mobile_stix_client,
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
        )

    def get_mobile_malware_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_malware_by_related_tactics(
            client=self.mobile_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_mobile_malware_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_malware_by_related_techniques(
            client=self.mobile_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_mobile_malware_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_malware_by_related_groups(
            client=self.mobile_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_mobile_malware_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_malware_by_related_mitigations(
            client=self.mobile_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_mobile_malware_by_id(self, software_id):
        return self.get_mobile_object(object_id=software_id, object_types=[MALWARE])

    def get_mobile_malware_by_name(self, software_name):
        return self.get_mobile_object(object_names=[software_name], object_types=[MALWARE])

    def get_mobile_tools(self, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None,
                         technique_ids=None, technique_names=None, group_ids=None, group_names=None,
                         mitigation_ids=None, mitigation_names=None, platforms=None):

        return self._get_tools(
            client=self.mobile_stix_client,
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
        )

    def get_mobile_tools_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_tools_by_related_tactics(
            client=self.mobile_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_mobile_tools_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_tools_by_related_techniques(
            client=self.mobile_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_mobile_tools_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_tools_by_related_groups(
            client=self.mobile_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_mobile_tools_by_related_mitigations(self, mitigation_ids=None, mitigation_names=None):
        return self._get_tools_by_related_mitigations(
            client=self.mobile_stix_client,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )

    def get_mobile_tool_by_id(self, software_id):
        return self.get_mobile_object(object_id=software_id, object_types=[TOOL])

    def get_mobile_tool_by_name(self, software_name):
        return self.get_mobile_object(object_names=[software_name], object_types=[TOOL])

    def get_mobile_mitigations(self, mitigation_ids=None, mitigation_names=None, tactic_ids=None, tactic_names=None,
                               technique_ids=None, technique_names=None, group_ids=None, group_names=None,
                               software_ids=None, software_names=None, platforms=None):

        return self._get_mitigations(
            client=self.mobile_stix_client,
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
        )

    def get_mobile_mitigations_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_mitigations_by_related_tactics(
            client=self.mobile_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_mobile_mitigations_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_mitigations_by_related_techniques(
            client=self.mobile_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_mobile_mitigations_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_mitigations_by_related_groups(
            client=self.mobile_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_mobile_mitigations_by_related_software(self, software_ids=None, software_names=None):
        return self._get_mitigations_by_related_software(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_mitigations_by_related_malware(self, software_ids=None, software_names=None):
        return self._get_mitigations_by_related_malware(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_mitigations_by_related_tools(self, software_ids=None, software_names=None):
        return self._get_mitigations_by_related_tools(
            client=self.mobile_stix_client,
            software_ids=software_ids,
            software_names=software_names,
        )

    def get_mobile_mitigation_by_id(self, mitigation_id):
        return self.get_mobile_object(object_id=mitigation_id, object_types=[COURSE_OF_ACTION])

    def get_mobile_mitigation_by_name(self, mitigation_name):
        return self.get_mobile_object(
            object_names=[mitigation_name],
            object_types=[COURSE_OF_ACTION],
        )

    def get_pre_attack_matrices(self):
        return self._get_matrices(client=self.pre_attack_stix_client)

    def get_pre_attack_identities(self):
        return self._get_identities(client=self.pre_attack_stix_client)

    def get_pre_attack_marking_definitions(self):
        return self._get_marking_definitions(client=self.pre_attack_stix_client)

    def get_pre_attack_tactics(self, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                               group_ids=None, group_names=None, platforms=None):

        return self._get_tactics(
            client=self.pre_attack_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            group_ids=group_ids,
            group_names=group_names,
            platforms=platforms,
        )

    def get_pre_attack_tactics_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_tactics_by_related_techniques(
            client=self.pre_attack_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_pre_attack_tactics_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_tactics_by_related_groups(
            client=self.pre_attack_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_pre_attack_tactic_by_id(self, tactic_id):
        return self.get_pre_attack_object(object_id=tactic_id, object_types=[TACTIC])

    def get_pre_attack_tactic_by_name(self, tactic_name):
        return self.get_pre_attack_object(object_names=[tactic_name], object_types=[TACTIC])

    def get_pre_attack_techniques(self, technique_ids=None, technique_names=None, tactic_ids=None, tactic_names=None,
                                  group_ids=None, group_names=None, platforms=None):

        return self._get_techniques(
            client=self.pre_attack_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            group_ids=group_ids,
            group_names=group_names,
            platforms=platforms,
        )

    def get_pre_attack_techniques_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_techniques_by_related_tactics(
            client=self.pre_attack_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_pre_attack_techniques_by_related_groups(self, group_ids=None, group_names=None):
        return self._get_techniques_by_related_groups(
            client=self.pre_attack_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_pre_attack_technique_by_id(self, technique_id):
        return self.get_pre_attack_object(object_id=technique_id, object_types=[ATTACK_PATTERN])

    def get_pre_attack_technique_by_name(self, technique_name):
        return self.get_pre_attack_object(object_names=[technique_name], object_types=[ATTACK_PATTERN])

    def get_pre_attack_groups(self, group_ids=None, group_names=None, tactic_ids=None, tactic_names=None,
                              technique_ids=None, technique_names=None, platforms=None):

        return self._get_groups(
            client=self.pre_attack_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            group_ids=group_ids,
            group_names=group_names,
            platforms=platforms,
        )

    def get_pre_attack_groups_by_related_tactics(self, tactic_ids=None, tactic_names=None):
        return self._get_groups_by_related_tactics(
            client=self.pre_attack_stix_client,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )

    def get_pre_attack_groups_by_related_techniques(self, technique_ids=None, technique_names=None):
        return self._get_groups_by_related_techniques(
            client=self.pre_attack_stix_client,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )

    def get_pre_attack_group_by_id(self, group_id):
        return self.get_pre_attack_object(object_id=group_id, object_types=[INTRUSION_SET])

    def get_pre_attack_group_by_name(self, group_name):
        return self.get_pre_attack_object(object_names=[group_name], object_types=[INTRUSION_SET])

    def _get_matrices(self, client):
        log.info(logger, "Looking up matrices")
        matrices = self._get_objects(client=client, object_types=[MATRIX])
        if matrices:
            log.info(logger, "Found %d matrices", len(matrices))
        else:
            log.warning(logger, "No matrices found")
        return matrices

    def _get_identities(self, client):
        log.info(logger, "Looking up identities")
        identities = self._get_objects(client=client, object_types=[IDENTITY])
        if identities:
            log.info(logger, "Found %d identities", len(identities))
        else:
            log.warning(logger, "No identities found")
        return identities

    def _get_marking_definitions(self, client):
        log.info(logger, "Looking up marking definitions")
        marking_definitions = self._get_objects(client=client, object_types=[MARKING_DEFINITION])
        if marking_definitions:
            log.info(logger, "Found %d marking definitions", len(marking_definitions))
        else:
            log.warning(logger, "No marking definitions found")
        return marking_definitions

    def _get_tactics(self, client, tactic_ids=None, tactic_names=None, technique_ids=None, technique_names=None,
                     group_ids=None, group_names=None, software_ids=None, software_names=None, mitigation_ids=None,
                     mitigation_names=None, platforms=None):

        tactic_ids = hodgepodge.helpers.as_set(tactic_ids, str)
        tactic_names = hodgepodge.helpers.as_set(tactic_names, str)
        technique_ids = hodgepodge.helpers.as_set(technique_ids, str)
        technique_names = hodgepodge.helpers.as_set(technique_names, str)
        group_ids = hodgepodge.helpers.as_set(group_ids, str)
        group_names = hodgepodge.helpers.as_set(group_names, str)
        software_ids = hodgepodge.helpers.as_set(software_ids, str)
        software_names = hodgepodge.helpers.as_set(software_names, str)
        mitigation_ids = hodgepodge.helpers.as_set(mitigation_ids, str)
        mitigation_names = hodgepodge.helpers.as_set(mitigation_names, str)
        platforms = hodgepodge.helpers.as_set(platforms, str)

        hint = log.get_hint(
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
        )
        log.info(logger, "Looking up tactics", hint=hint)

        tactics = self._get_objects(client, object_types=(TACTIC,), object_ids=tactic_ids, object_names=tactic_names)

        #: Filter tactics by platform, or by related techniques, groups, malware families, tools, or mitigations.
        if tactics and (technique_ids or technique_names or group_ids or group_names or software_ids or
                        software_names or mitigation_ids or mitigation_names or platforms):

            techniques = self._get_techniques(
                client=client,
                technique_ids=technique_ids,
                technique_names=technique_names,
                group_ids=group_ids,
                group_names=group_names,
                software_ids=software_ids,
                software_names=software_names,
                mitigation_ids=mitigation_ids,
                mitigation_names=mitigation_names,
                platforms=platforms,
            )
            tactics = list(self._filter_tactics_by_related_techniques(
                tactics=tactics,
                techniques=techniques,
            ))

        if tactics:
            log.info(logger, "Found %d matching tactics", len(tactics), hint=hint)
        else:
            log.warning(logger, "No matching tactics found", hint=hint)
        return tactics

    def _get_tactics_by_related_techniques(self, client, technique_ids=None, technique_names=None):
        return self._get_tactics(client=client, technique_ids=technique_ids, technique_names=technique_names)

    def _get_tactics_by_related_groups(self, client, group_ids=None, group_names=None):
        return self._get_tactics(client=client, group_ids=group_ids, group_names=group_names)

    def _get_tactics_by_related_software(self, client, software_ids=None, software_names=None):
        return self._get_tactics(client=client, software_ids=software_ids, software_names=software_names)

    def _get_tactics_by_related_tools(self, client, software_ids=None, software_names=None):
        return self._get_tactics(client=client, software_ids=software_ids, software_names=software_names)

    def _get_tactics_by_related_malware(self, client, software_ids=None, software_names=None):
        return self._get_tactics(client=client, software_ids=software_ids, software_names=software_names)

    def _get_tactics_by_related_mitigations(self, client, mitigation_ids=None, mitigation_names=None):
        return self._get_tactics(client=client, mitigation_ids=mitigation_ids, mitigation_names=mitigation_names)

    def _filter_tactics_by_related_techniques(self, tactics, techniques):
        kill_chain_phase_names = set()
        for technique in techniques:
            for kill_chain_phase_name in technique.kill_chain_phase_names:
                kill_chain_phase_names.add(kill_chain_phase_name)

        for tactic in tactics:
            if tactic.kill_chain_phase_name in kill_chain_phase_names:
                yield tactic

    def _get_techniques(self, client, technique_ids=None, technique_names=None, tactic_ids=None, tactic_names=None,
                        group_ids=None, group_names=None, software_ids=None, software_names=None, mitigation_ids=None,
                        mitigation_names=None, platforms=None):

        tactic_ids = hodgepodge.helpers.as_set(tactic_ids, str)
        tactic_names = hodgepodge.helpers.as_set(tactic_names, str)
        technique_ids = hodgepodge.helpers.as_set(technique_ids, str)
        technique_names = hodgepodge.helpers.as_set(technique_names, str)
        group_ids = hodgepodge.helpers.as_set(group_ids, str)
        group_names = hodgepodge.helpers.as_set(group_names, str)
        software_ids = hodgepodge.helpers.as_set(software_ids, str)
        software_names = hodgepodge.helpers.as_set(software_names, str)
        mitigation_ids = hodgepodge.helpers.as_set(mitigation_ids, str)
        mitigation_names = hodgepodge.helpers.as_set(mitigation_names, str)
        platforms = hodgepodge.helpers.as_set(platforms, str)

        hint = log.get_hint(
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
        )
        log.info(logger, "Looking up techniques", hint=hint)

        #: Lookup techniques.
        techniques = self._get_objects(
            client=client,
            object_types=(ATTACK_PATTERN,),
            object_ids=technique_ids,
            object_names=technique_names,
        )

        #: Filter techniques by platform.
        if techniques and platforms:
            techniques = list(filter_objects_by_platform(techniques, platforms))

        #: Filter techniques by related tactics.
        if techniques and (tactic_ids or tactic_names):
            tactics = self._get_tactics(client=client, tactic_ids=tactic_ids, tactic_names=tactic_names)
            techniques = list(self._filter_techniques_by_related_tactics(techniques=techniques, tactics=tactics))

        #: Filter techniques by related groups.
        if techniques and (group_ids or group_names):
            groups = self._get_groups(client=client, group_ids=group_ids, group_names=group_names)
            techniques = list(self._filter_techniques_by_related_groups(
                client=client,
                techniques=techniques,
                groups=groups,
            ))

        #: Filter techniques by related malware families, and tools.
        if techniques and (software_ids or software_names):
            software = self._get_software(client=client, software_ids=software_ids, software_names=software_names)
            techniques = list(self._filter_techniques_by_related_software(
                client=client,
                techniques=techniques,
                software=software,
            ))

        #: Filter techniques by related mitigations.
        if techniques and (mitigation_ids or mitigation_names):
            mitigations = self._get_mitigations(
                client=client,
                mitigation_ids=mitigation_ids,
                mitigation_names=mitigation_names,
            )
            techniques = list(self._filter_techniques_by_related_mitigations(
                client=client,
                techniques=techniques,
                mitigations=mitigations,
            ))

        if techniques:
            log.info(logger, "Found %d matching techniques", len(techniques), hint=hint)
        else:
            log.warning(logger, "No matching techniques found", hint=hint)
        return techniques

    def _get_techniques_by_related_tactics(self, client, tactic_ids=None, tactic_names=None):
        return self._get_techniques(client=client, tactic_ids=tactic_ids, tactic_names=tactic_names)

    def _get_techniques_by_related_groups(self, client, group_ids=None, group_names=None):
        return self._get_techniques(client=client, group_ids=group_ids, group_names=group_names)

    def _get_techniques_by_related_software(self, client, software_ids=None, software_names=None):
        return self._get_techniques(client=client, software_ids=software_ids, software_names=software_names)

    def _get_techniques_by_related_tools(self, client, software_ids=None, software_names=None):
        return self._get_techniques(client=client, software_ids=software_ids, software_names=software_names)

    def _get_techniques_by_related_malware(self, client, software_ids=None, software_names=None):
        return self._get_techniques(client=client, software_ids=software_ids, software_names=software_names)

    def _get_techniques_by_related_mitigations(self, client, mitigation_ids=None, mitigation_names=None):
        return self._get_techniques(client=client, mitigation_ids=mitigation_ids, mitigation_names=mitigation_names)

    def _filter_techniques_by_related_tactics(self, techniques, tactics):
        kill_chain_phase_names = {t.kill_chain_phase_name for t in tactics}
        for technique in techniques:
            for kill_chain_phase_name in technique.kill_chain_phase_names:
                if kill_chain_phase_name in kill_chain_phase_names:
                    yield technique
                    break

    def _filter_techniques_by_related_groups(self, client, techniques, groups):
        if not groups:
            techniques = []
        else:
            relationships = self._get_relationships(
                client=client,
                source_object_ids={g.id for g in groups},
                source_object_types=(INTRUSION_SET,),
                relationship_types=(USES,),
                target_object_types=(ATTACK_PATTERN,),
                target_object_ids={t.id for t in techniques},
            )
            technique_ids = {r.dst for r in relationships}
            techniques = [t for t in techniques if t.id in technique_ids]
        return techniques

    def _filter_techniques_by_related_software(self, client, techniques, software):
        if not software:
            techniques = []
        else:
            software_types = {obj.type for obj in software}
            relationships = self._get_relationships(
                client=client,
                source_object_ids={s.id for s in software},
                source_object_types=software_types,
                relationship_types=(USES,),
                target_object_types=(ATTACK_PATTERN,),
                target_object_ids={t.id for t in techniques},
            )
            technique_ids = {r.dst for r in relationships}
            techniques = [t for t in techniques if t.id in technique_ids]
        return techniques

    def _filter_techniques_by_related_mitigations(self, client, techniques, mitigations):
        if not mitigations:
            techniques = []
        else:
            relationships = self._get_relationships(
                client=client,
                source_object_ids={m.id for m in mitigations},
                source_object_types=(COURSE_OF_ACTION,),
                relationship_types=(MITIGATES,),
                target_object_types=(ATTACK_PATTERN,),
                target_object_ids={t.id for t in techniques},
            )
            technique_ids = {r.dst for r in relationships}
            techniques = [t for t in techniques if t.id in technique_ids]
        return techniques

    def _get_groups(self, client, group_ids=None, group_names=None, tactic_ids=None, tactic_names=None,
                    technique_ids=None, technique_names=None, software_ids=None, software_names=None,
                    mitigation_ids=None, mitigation_names=None, platforms=None):

        tactic_ids = hodgepodge.helpers.as_set(tactic_ids, str)
        tactic_names = hodgepodge.helpers.as_set(tactic_names, str)
        technique_ids = hodgepodge.helpers.as_set(technique_ids, str)
        technique_names = hodgepodge.helpers.as_set(technique_names, str)
        group_ids = hodgepodge.helpers.as_set(group_ids, str)
        group_names = hodgepodge.helpers.as_set(group_names, str)
        software_ids = hodgepodge.helpers.as_set(software_ids, str)
        software_names = hodgepodge.helpers.as_set(software_names, str)
        mitigation_ids = hodgepodge.helpers.as_set(mitigation_ids, str)
        mitigation_names = hodgepodge.helpers.as_set(mitigation_names, str)
        platforms = hodgepodge.helpers.as_set(platforms, str)

        hint = log.get_hint(
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
        )
        log.info(logger, "Looking up groups", hint=hint)

        #: Lookup groups.
        groups = self._get_objects(
            client=client,
            object_types=(INTRUSION_SET,),
            object_ids=group_ids,
            object_names=group_names,
        )

        #: Filter groups by platform, or by related malware families, or tools.
        if groups and (software_ids or software_names or platforms):
            software = self._get_software(
                client=client,
                software_ids=software_ids,
                software_names=software_names,
                platforms=platforms,
            )
            groups = list(self._filter_groups_by_related_software(client=client, groups=groups, software=software))

        #: Filter groups by platform, or by related tactics, techniques, or mitigations.
        if groups and (tactic_ids or tactic_names or technique_ids or technique_names or mitigation_ids or
                       mitigation_names or platforms):
            techniques = self._get_techniques(
                client=client,
                tactic_ids=tactic_ids,
                tactic_names=tactic_names,
                technique_ids=technique_ids,
                technique_names=technique_names,
                mitigation_ids=mitigation_ids,
                mitigation_names=mitigation_names,
                platforms=platforms,
            )
            groups = list(self._filter_groups_by_related_techniques(
                client=client,
                groups=groups,
                techniques=techniques,
            ))

        if groups:
            log.info(logger, "Found %d matching groups", len(groups), hint=hint)
        else:
            log.warning(logger, "No matching groups found", hint=hint)
        return groups

    def _get_groups_by_related_tactics(self, client, tactic_ids=None, tactic_names=None):
        return self._get_groups(client=client, tactic_ids=tactic_ids, tactic_names=tactic_names)

    def _get_groups_by_related_techniques(self, client, technique_ids=None, technique_names=None):
        return self._get_groups(client=client, technique_ids=technique_ids, technique_names=technique_names)

    def _get_groups_by_related_software(self, client, software_ids=None, software_names=None):
        return self._get_groups(client=client, software_ids=software_ids, software_names=software_names)

    def _get_groups_by_related_tools(self, client, software_ids=None, software_names=None):
        return self._get_groups(client=client, software_ids=software_ids, software_names=software_names)

    def _get_groups_by_related_malware(self, client, software_ids=None, software_names=None):
        return self._get_groups(client=client, software_ids=software_ids, software_names=software_names)

    def _get_groups_by_related_mitigations(self, client, mitigation_ids=None, mitigation_names=None):
        return self._get_groups(client=client, mitigation_ids=mitigation_ids, mitigation_names=mitigation_names)

    def _filter_groups_by_related_techniques(self, client, groups, techniques):
        if not techniques:
            groups = []
        else:
            relationships = self._get_relationships(
                client=client,
                source_object_ids={g.id for g in groups},
                source_object_types=(INTRUSION_SET,),
                relationship_types=(USES,),
                target_object_types=(ATTACK_PATTERN,),
                target_object_ids={t.id for t in techniques},
            )
            group_ids = {r.src for r in relationships}
            groups = [g for g in groups if g.id in group_ids]
        return groups

    def _filter_groups_by_related_software(self, client, groups, software):
        if not software:
            groups = []
        else:
            software_types = {s.type for s in software}
            relationships = self._get_relationships(
                client=client,
                source_object_ids={g.id for g in groups},
                source_object_types=(INTRUSION_SET,),
                relationship_types=(USES,),
                target_object_types=software_types,
                target_object_ids={s.id for s in software},
            )
            group_ids = {r.src for r in relationships}
            groups = [g for g in groups if g.id in group_ids]
        return groups

    def _get_software(self, client, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None,
                      technique_ids=None, technique_names=None, group_ids=None, group_names=None, mitigation_ids=None,
                      mitigation_names=None, platforms=None, include_malware=True, include_tools=True):

        tactic_ids = hodgepodge.helpers.as_set(tactic_ids, str)
        tactic_names = hodgepodge.helpers.as_set(tactic_names, str)
        technique_ids = hodgepodge.helpers.as_set(technique_ids, str)
        technique_names = hodgepodge.helpers.as_set(technique_names, str)
        group_ids = hodgepodge.helpers.as_set(group_ids, str)
        group_names = hodgepodge.helpers.as_set(group_names, str)
        software_ids = hodgepodge.helpers.as_set(software_ids, str)
        software_names = hodgepodge.helpers.as_set(software_names, str)
        mitigation_ids = hodgepodge.helpers.as_set(mitigation_ids, str)
        mitigation_names = hodgepodge.helpers.as_set(mitigation_names, str)
        platforms = hodgepodge.helpers.as_set(platforms, str)

        hint = log.get_hint(
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
            include_malware=include_malware,
            include_tools=include_tools,
        )
        log.info(logger, "Looking up software", hint=hint)

        #: Lookup software.
        if include_malware and include_tools:
            object_types = [MALWARE, TOOL]
        elif include_malware:
            object_types = [MALWARE]
        elif include_tools:
            object_types = [TOOL]
        else:
            raise ValueError("Cannot exclude both malware families, and tools")

        software = self._get_objects(
            client=client,
            object_types=object_types,
            object_ids=software_ids,
            object_names=software_names,
        )

        #: Filter software by platform.
        if software and platforms:
            software = list(filter_objects_by_platform(software, platforms))

        #: Filter software by related groups.
        if software and (group_ids or group_names):
            groups = self._get_groups(client=client, group_ids=group_ids, group_names=group_names)
            software = list(self._filter_software_by_related_groups(client=client, groups=groups, software=software))

        #: Filter software by related tactics, techniques, or mitigations.
        if software and (tactic_ids or tactic_names or technique_ids or technique_names or mitigation_ids or
                         mitigation_names):

            techniques = self._get_techniques(
                client=client,
                tactic_ids=tactic_ids,
                tactic_names=tactic_names,
                technique_ids=technique_ids,
                technique_names=technique_names,
                mitigation_ids=mitigation_ids,
                mitigation_names=mitigation_names,
                platforms=platforms,
            )
            software = list(self._filter_software_by_related_techniques(
                client=client,
                software=software,
                techniques=techniques,
            ))

        #: Log the product of our search.
        if software:
            includes_malware = any(obj.type == MALWARE for obj in software)
            includes_tools = any(obj.type == TOOL for obj in software)

            if includes_malware and includes_tools:
                scope = 'malware families and tools'
            elif includes_malware:
                scope = 'malware families'
            else:
                scope = 'tools'

            log.info(logger, "Found %d matching %s", len(software), scope, hint=hint)
        else:
            log.warning(logger, "No matching software found", hint=hint)
        return software

    def _get_software_by_related_tactics(self, client, tactic_ids=None, tactic_names=None):
        return self._get_software(client=client, tactic_ids=tactic_ids, tactic_names=tactic_names)

    def _get_software_by_related_techniques(self, client, technique_ids=None, technique_names=None):
        return self._get_software(client=client, technique_ids=technique_ids, technique_names=technique_names)

    def _get_software_by_related_groups(self, client, group_ids=None, group_names=None):
        return self._get_software(client=client, group_ids=group_ids, group_names=group_names)

    def _get_software_by_related_mitigations(self, client, mitigation_ids=None, mitigation_names=None):
        return self._get_software(client=client, mitigation_ids=mitigation_ids, mitigation_names=mitigation_names)

    def _filter_software_by_related_techniques(self, client, software, techniques):
        if not techniques:
            software = []
        else:
            software_types = {s.type for s in software}
            relationships = self._get_relationships(
                client=client,
                source_object_ids={s.id for s in software},
                source_object_types=software_types,
                relationship_types=(USES,),
                target_object_types=(ATTACK_PATTERN,),
                target_object_ids={t.id for t in techniques},
            )
            software_ids = {r.src for r in relationships}
            software = [s for s in software if s.id in software_ids]
        return software

    def _filter_software_by_related_groups(self, client, software, groups):
        if not groups:
            software = []
        else:
            software_types = {s.type for s in software}
            relationships = self._get_relationships(
                client=client,
                source_object_ids={g.id for g in groups},
                source_object_types=(INTRUSION_SET,),
                relationship_types=(USES,),
                target_object_types=software_types,
                target_object_ids={s.id for s in software},
            )
            software_ids = {r.dst for r in relationships}
            software = [s for s in software if s.id in software_ids]
        return software

    def _get_malware(self, client, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None,
                     technique_ids=None, technique_names=None, group_ids=None, group_names=None, mitigation_ids=None,
                     mitigation_names=None, platforms=None):

        return self._get_software(
            client=client,
            software_ids=software_ids,
            software_names=software_names,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            group_ids=group_ids,
            group_names=group_names,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
            platforms=platforms,
            include_malware=True,
            include_tools=False,
        )

    def _get_malware_by_related_tactics(self, client, tactic_ids=None, tactic_names=None):
        return self._get_malware(client=client, tactic_ids=tactic_ids, tactic_names=tactic_names)

    def _get_malware_by_related_techniques(self, client, technique_ids=None, technique_names=None):
        return self._get_malware(client=client, technique_ids=technique_ids, technique_names=technique_names)

    def _get_malware_by_related_groups(self, client, group_ids=None, group_names=None):
        return self._get_malware(client=client, group_ids=group_ids, group_names=group_names)

    def _get_malware_by_related_mitigations(self, client, mitigation_ids=None, mitigation_names=None):
        return self._get_malware(client=client, mitigation_ids=mitigation_ids, mitigation_names=mitigation_names)

    def _get_tools(self, client, software_ids=None, software_names=None, tactic_ids=None, tactic_names=None,
                   technique_ids=None, technique_names=None, group_ids=None, group_names=None, mitigation_ids=None,
                   mitigation_names=None, platforms=None):

        return self._get_software(
            client=client,
            software_ids=software_ids,
            software_names=software_names,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
            group_ids=group_ids,
            group_names=group_names,
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
            platforms=platforms,
            include_malware=False,
            include_tools=True,
        )

    def _get_tools_by_related_tactics(self, client, tactic_ids=None, tactic_names=None):
        return self._get_malware(client=client, tactic_ids=tactic_ids, tactic_names=tactic_names)

    def _get_tools_by_related_techniques(self, client, technique_ids=None, technique_names=None):
        return self._get_malware(client=client, technique_ids=technique_ids, technique_names=technique_names)

    def _get_tools_by_related_groups(self, client, group_ids=None, group_names=None):
        return self._get_malware(client=client, group_ids=group_ids, group_names=group_names)

    def _get_tools_by_related_mitigations(self, client, mitigation_ids=None, mitigation_names=None):
        return self._get_malware(client=client, mitigation_ids=mitigation_ids, mitigation_names=mitigation_names)

    def _get_mitigations(self, client, mitigation_ids=None, mitigation_names=None, tactic_ids=None, tactic_names=None,
                         technique_ids=None, technique_names=None, group_ids=None, group_names=None, software_ids=None,
                         software_names=None, platforms=None):

        tactic_ids = hodgepodge.helpers.as_set(tactic_ids, str)
        tactic_names = hodgepodge.helpers.as_set(tactic_names, str)
        technique_ids = hodgepodge.helpers.as_set(technique_ids, str)
        technique_names = hodgepodge.helpers.as_set(technique_names, str)
        group_ids = hodgepodge.helpers.as_set(group_ids, str)
        group_names = hodgepodge.helpers.as_set(group_names, str)
        software_ids = hodgepodge.helpers.as_set(software_ids, str)
        software_names = hodgepodge.helpers.as_set(software_names, str)
        mitigation_ids = hodgepodge.helpers.as_set(mitigation_ids, str)
        mitigation_names = hodgepodge.helpers.as_set(mitigation_names, str)
        platforms = hodgepodge.helpers.as_set(platforms, str)

        hint = log.get_hint(
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
        )
        log.info(logger, "Looking up mitigations", hint=hint)

        #: Lookup mitigations.
        mitigations = self._get_objects(
            client=client,
            object_types=(COURSE_OF_ACTION,),
            object_ids=mitigation_ids,
            object_names=mitigation_names,
        )

        #: Filter mitigations by platform, or by related tactics, techniques, groups, malware families, or tools.
        if mitigations and (tactic_ids or tactic_names or technique_ids or technique_names or group_ids or
                            group_names or software_ids or software_names or platforms):

            techniques = self._get_techniques(
                client=client,
                tactic_ids=tactic_ids,
                tactic_names=tactic_names,
                technique_ids=technique_ids,
                technique_names=technique_names,
                group_ids=group_ids,
                group_names=group_names,
                software_ids=software_ids,
                software_names=software_names,
                platforms=platforms,
            )
            mitigations = list(self._filter_mitigations_by_related_techniques(
                client=client,
                mitigations=mitigations,
                techniques=techniques,
            ))

        if mitigations:
            log.info(logger, "Found %d matching mitigations", len(mitigations), hint=hint)
        else:
            log.warning(logger, "No matching mitigations found", hint=hint)
        return mitigations

    def _get_mitigations_by_related_tactics(self, client, tactic_ids=None, tactic_names=None):
        return self._get_mitigations(client=client, tactic_ids=tactic_ids, tactic_names=tactic_names)

    def _get_mitigations_by_related_techniques(self, client, technique_ids=None, technique_names=None):
        return self._get_mitigations(client=client, technique_ids=technique_ids, technique_names=technique_names)

    def _get_mitigations_by_related_groups(self, client, group_ids=None, group_names=None):
        return self._get_mitigations(client=client, group_ids=group_ids, group_names=group_names)

    def _get_mitigations_by_related_malware(self, client, software_ids=None, software_names=None):
        return self._get_mitigations(client=client, software_ids=software_ids, software_names=software_names)

    def _get_mitigations_by_related_tools(self, client, software_ids=None, software_names=None):
        return self._get_mitigations(client=client, software_ids=software_ids, software_names=software_names)

    def _get_mitigations_by_related_software(self, client, software_ids=None, software_names=None):
        return self._get_mitigations(client=client, software_ids=software_ids, software_names=software_names)

    def _filter_mitigations_by_related_techniques(self, client, mitigations, techniques):
        if not techniques:
            mitigations = []
        else:
            relationships = self._get_relationships(
                client=client,
                source_object_ids={m.id for m in mitigations},
                source_object_types=(COURSE_OF_ACTION,),
                relationship_types=(MITIGATES,),
                target_object_types=(ATTACK_PATTERN,),
                target_object_ids={t.id for t in techniques},
            )
            mitigation_ids = {r.src for r in relationships}
            mitigations = [m for m in mitigations if m.id in mitigation_ids]
        return mitigations

    def get_relationships(self, source_object_ids=None, source_object_names=None, source_object_types=None,
                          target_object_ids=None, target_object_names=None, target_object_types=None,
                          relationship_types=None):

        return self._get_relationships(
            client=self.composite_stix_client,
            source_object_ids=source_object_ids,
            source_object_names=source_object_names,
            source_object_types=source_object_types,
            target_object_ids=target_object_ids,
            target_object_names=target_object_names,
            target_object_types=target_object_types,
            relationship_types=relationship_types,
        )

    def get_enterprise_relationships(self, source_object_ids=None, source_object_names=None, source_object_types=None, 
                                     target_object_ids=None, target_object_names=None, target_object_types=None,
                                     relationship_types=None):
        return self._get_relationships(
            client=self.enterprise_stix_client,
            source_object_ids=source_object_ids,
            source_object_names=source_object_names,
            source_object_types=source_object_types,
            target_object_ids=target_object_ids,
            target_object_names=target_object_names,
            target_object_types=target_object_types,
            relationship_types=relationship_types,
        )

    def get_mobile_relationships(self, source_object_ids=None, source_object_names=None, source_object_types=None,
                                 target_object_ids=None, target_object_names=None, target_object_types=None,
                                 relationship_types=None):

        return self._get_relationships(
            client=self.mobile_stix_client,
            source_object_ids=source_object_ids,
            source_object_names=source_object_names,
            source_object_types=source_object_types,
            target_object_ids=target_object_ids,
            target_object_names=target_object_names,
            target_object_types=target_object_types,
            relationship_types=relationship_types,
        )

    def get_pre_attack_relationships(self, source_object_ids=None, source_object_names=None, source_object_types=None,
                                     target_object_ids=None, target_object_names=None, target_object_types=None,
                                     relationship_types=None):
        return self._get_relationships(
            client=self.pre_attack_stix_client,
            source_object_ids=source_object_ids,
            source_object_names=source_object_names,
            source_object_types=source_object_types,
            target_object_ids=target_object_ids,
            target_object_names=target_object_names,
            target_object_types=target_object_types,
            relationship_types=relationship_types,
        )

    def get_objects(self, object_ids=None, object_types=None, object_names=None):
        return self._get_objects(
            client=self.composite_stix_client,
            object_ids=object_ids,
            object_types=object_types,
            object_names=object_names,
        )

    def get_enterprise_objects(self, object_ids=None, object_types=None, object_names=None):
        return self._get_objects(
            client=self.enterprise_stix_client,
            object_ids=object_ids,
            object_types=object_types,
            object_names=object_names,
        )

    def get_mobile_objects(self, object_ids=None, object_types=None, object_names=None):
        return self._get_objects(
            client=self.mobile_stix_client,
            object_ids=object_ids,
            object_types=object_types,
            object_names=object_names,
        )

    def get_pre_attack_objects(self, object_ids=None, object_types=None, object_names=None):
        return self._get_objects(
            client=self.pre_attack_stix_client,
            object_ids=object_ids,
            object_types=object_types,
            object_names=object_names,
        )

    def get_object(self, object_id=None, object_types=None, object_names=None):
        return self._get_object(
            client=self.composite_stix_client,
            object_id=object_id,
            object_types=object_types,
            object_names=object_names,
        )

    def get_enterprise_object(self, object_id=None, object_types=None, object_names=None):
        return self._get_object(
            client=self.enterprise_stix_client,
            object_id=object_id,
            object_types=object_types,
            object_names=object_names,
        )

    def get_mobile_object(self, object_id=None, object_types=None, object_names=None):
        return self._get_object(
            client=self.mobile_stix_client,
            object_id=object_id,
            object_types=object_types,
            object_names=object_names,
        )

    def get_pre_attack_object(self, object_id=None, object_types=None, object_names=None):
        return self._get_object(
            client=self.pre_attack_stix_client,
            object_id=object_id,
            object_types=object_types,
            object_names=object_names,
        )

    def get_stix_objects_related_to_groups(self, group_ids=None, group_names=None):
        return self._get_stix_objects_related_to_groups(
            client=self.composite_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_enterprise_stix_objects_related_to_groups(self, group_ids=None, group_names=None):
        return self._get_stix_objects_related_to_groups(
            client=self.enterprise_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_mobile_stix_objects_related_to_groups(self, group_ids=None, group_names=None):
        return self._get_stix_objects_related_to_groups(
            client=self.mobile_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def get_pre_attack_stix_objects_related_to_groups(self, group_ids=None, group_names=None):
        return self._get_stix_objects_related_to_groups(
            client=self.pre_attack_stix_client,
            group_ids=group_ids,
            group_names=group_names,
        )

    def _get_object(self, client, object_id=None, object_names=None, object_types=None):
        if object_id and stix_parsers.is_internal_id(object_id):
            data = client.get_object(object_internal_id=object_id)
            if data:
                data = self._parse_object(data)
            else:
                data = None
        else:
            objects = self._get_objects(
                client=client,
                object_ids=hodgepodge.helpers.as_set(object_id, str),
                object_names=hodgepodge.helpers.as_set(object_names, str),
                object_types=hodgepodge.helpers.as_set(object_types, str),
            )
            data = next(iter(objects), None)
        return data

    def _get_objects(self, client, object_ids=None, object_types=None, object_names=None):
        object_ids = hodgepodge.helpers.as_set(object_ids, str)
        object_types = hodgepodge.helpers.as_set(object_types, str)
        object_names = hodgepodge.helpers.as_set(object_names, str)

        if object_ids:
            internal_ids, external_ids = stix_parsers.partition_set_of_object_ids(object_ids)
        else:
            internal_ids = set()
            external_ids = set()

        objects = client.get_objects(
            object_internal_ids=internal_ids,
            object_external_ids=external_ids,
            object_names=object_names,
            object_types=object_types,
        )
        return list(self._parse_object_stream(objects))

    def _get_object_internal_ids(self, client, object_ids=None, object_types=None, object_names=None):
        if object_ids:
            internal_ids, external_ids = stix_parsers.partition_set_of_object_ids(object_ids)
        else:
            internal_ids = None
            external_ids = None

        return client.get_object_internal_ids(
            object_internal_ids=internal_ids,
            object_external_ids=external_ids,
            object_names=object_names,
            object_types=object_types,
        )

    def _get_relationships(self, client, source_object_ids=None, source_object_names=None, source_object_types=None,
                           target_object_ids=None, target_object_names=None, target_object_types=None,
                           relationship_types=None):

        source_object_ids = hodgepodge.helpers.as_set(source_object_ids, str)
        source_object_names = hodgepodge.helpers.as_set(source_object_names, str)
        source_object_types = hodgepodge.helpers.as_set(source_object_types, str)
        target_object_ids = hodgepodge.helpers.as_set(target_object_ids, str)
        target_object_names = hodgepodge.helpers.as_set(target_object_names, str)
        target_object_types = hodgepodge.helpers.as_set(target_object_types, str)
        relationship_types = hodgepodge.helpers.as_set(relationship_types, str)

        if source_object_ids or source_object_names:
            source_object_ids = self._get_object_internal_ids(
                client=client,
                object_ids=source_object_ids,
                object_types=source_object_types,
                object_names=source_object_names,
            )

        if target_object_ids or target_object_names:
            target_object_ids = self._get_object_internal_ids(
                client=client,
                object_ids=target_object_ids,
                object_types=target_object_types,
                object_names=target_object_names,
            )

        hint = log.get_hint(
            source_object_internal_ids=len(source_object_ids) or None,
            source_object_types=source_object_types,
            relationship_types=relationship_types,
            target_object_internal_ids=len(target_object_ids) or None,
            target_object_types=target_object_types,
        )
        log.info(logger, "Looking up relationships", hint=hint)

        relationships = client.get_relationships(
            source_object_internal_ids=source_object_ids,
            source_object_types=source_object_types,
            relationship_types=relationship_types,
            target_object_internal_ids=target_object_ids,
            target_object_types=target_object_types,
        )
        relationships = list(self._parse_object_stream(relationships))
        if relationships:
            log.info(logger, "Identified %d relationships between %d %s objects and %d %s objects",
                     len(relationships),
                     len({r.src for r in relationships}), '|'.join({r.src_type for r in relationships}),
                     len({r.dst for r in relationships}), '|'.join({r.dst_type for r in relationships}), hint=hint)
        else:
            log.warning(logger, "No matching relationships found", hint=hint)
        return relationships

    def _get_stix_objects_related_to_groups(self, client, group_ids, group_names):
        group_ids = hodgepodge.helpers.as_set(group_ids, str)
        group_names = hodgepodge.helpers.as_set(group_names, str)

        #: Lookup groups.
        groups = self._get_groups(client=client, group_ids=group_ids, group_names=group_names)
        if not groups:
            log.warning(logger, "No matching groups found", hint=log.get_hint(
                group_ids=group_ids, group_names=group_names
            ))
            return []

        group_ids = {g.id for g in groups}

        #: Lookup related identities, marking definitions, and matrices.
        object_internal_ids = group_ids
        object_internal_ids |= {identity.id for identity in self._get_identities(client)}
        object_internal_ids |= {definition.id for definition in self._get_marking_definitions(client)}
        object_internal_ids |= {matrix.id for matrix in self._get_matrices(client)}

        #: Lookup related tactics.
        object_internal_ids |= {t.id for t in self._get_tactics(client=client, group_ids=group_ids)}

        #: Lookup related techniques, malware families, tools, and mitigations.
        relationships = self._get_relationships(client=client)
        software_ids = {r.dst for r in relationships if r.src in group_ids and r.dst_type in ['malware', 'tool']}
        technique_ids = {r.dst for r in relationships if r.src in group_ids and r.dst_type == 'attack-pattern'}
        mitigation_ids = {r.src for r in relationships if r.src_type == 'course-of-action' and r.dst in technique_ids}
        object_internal_ids |= (software_ids | technique_ids | mitigation_ids)

        #: Filter the set of relationships.
        relationship_ids = {
            r.id for r in relationships if r.src in object_internal_ids and r.dst in object_internal_ids
        }
        object_internal_ids |= relationship_ids
        return client.get_objects(object_internal_ids=object_internal_ids)

    def _parse_object(self, data):
        if not data:
            return None

        #: Filter deprecated objects.
        if self._ignore_deprecated and data.get('x_mitre_deprecated', False):
            log.debug(logger, "Ignoring deprecated %s object: %s", data['type'], data['id'])
            return None

        return mitre_attack_parsers.parse_object(data)

    def _parse_object_stream(self, objects):
        for obj in objects:
            obj = self._parse_object(obj)
            if obj:
                yield obj


def filter_objects_by_platform(objects, platforms):
    for obj in objects:
        if obj.has_matching_platform(platforms):
            yield obj
