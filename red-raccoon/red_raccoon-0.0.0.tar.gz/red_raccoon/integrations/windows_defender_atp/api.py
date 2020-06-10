from hodgepodge.helpers import ensure_type

import red_raccoon.log as log
import hodgepodge.networking
import hodgepodge.timestamps
import hodgepodge.helpers
import requests
import logging
import arrow
import os

logger = logging.getLogger(__name__)

DEFAULT_TENANT_ID = os.getenv('WINDOWS_DEFENDER_ATP_TENANT_ID')
DEFAULT_APPLICATION_ID = os.getenv('WINDOWS_DEFENDER_ATP_APPLICATION_ID')
DEFAULT_APPLICATION_SECRET = os.getenv('WINDOWS_DEFENDER_ATP_APPLICATION_SECRET')

DEFAULT_BACKFILL_FOR_EVENT_DATA = 24 * 60 * 60      #: 24 hours.


class WindowsDefenderATPSIEMAPI:
    def __init__(self, tenant_id=DEFAULT_TENANT_ID, application_id=DEFAULT_APPLICATION_ID,
                 application_secret=DEFAULT_APPLICATION_SECRET,
                 default_backfill_for_event_data=DEFAULT_BACKFILL_FOR_EVENT_DATA):

        self.tenant_id = tenant_id
        self.application_id = application_id
        self.application_secret = application_secret
        self.application_resource = 'https://graph.windows.net'

        self.default_backfill_for_event_data = default_backfill_for_event_data

        self._access_token = None

    def _parse_tenant_id(self, tenant_id):
        tenant_id = ensure_type(tenant_id, str)
        if len(tenant_id) != 36:
            raise ValueError("Tenant IDs should be 36 characters in length: {}".format(tenant_id))
        return tenant_id

    def _parse_application_id(self, application_id):
        application_id = ensure_type(application_id, str)
        if len(application_id) != 36:
            raise ValueError("Application IDs should be 36 characters in length: {}".format(application_id))
        return application_id

    def _parse_application_secret(self, application_secret):
        application_secret = ensure_type(application_secret, str)
        if len(application_secret) != 32:
            raise ValueError("Application secrets should be 32 characters in length: {}".format(application_secret))
        return application_secret

    @property
    def access_token(self):
        token = self._access_token
        if token is None:
            token = self._access_token = self.authenticate()
        return token

    def authenticate(self):
        url = "https://login.windows.net/{}/oauth2/token".format(self.tenant_id)
        data = {
            "resource": self.application_resource,
            "client_Id": self.application_id,
            "client_Secret": self.application_secret,
            "grant_type": "client_credentials",
        }
        response = requests.post(url, data=data)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise

        body = response.json()
        token = self._access_token = body['access_token']
        return token

    def get_raw_events(self, minimum_event_timestamp=None, maximum_event_timestamp=None, event_ids=None,
                       event_names=None, event_types=None, event_descriptions=None, host_ids=None, hostnames=None,
                       ipv4_addresses=None, ipv6_addresses=None, md5_checksums=None, sha1_checksums=None,
                       sha256_checksums=None, usernames=None, paths=None, urls=None, ad_domains=None, ad_groups=None,
                       ad_names=None):

        return list(self.iter_raw_events(
            minimum_event_timestamp=minimum_event_timestamp,
            maximum_event_timestamp=maximum_event_timestamp,
            event_ids=event_ids,
            event_names=event_names,
            event_types=event_types,
            event_descriptions=event_descriptions,
            host_ids=host_ids,
            hostnames=hostnames,
            ipv4_addresses=ipv4_addresses,
            ipv6_addresses=ipv6_addresses,
            md5_checksums=md5_checksums,
            sha1_checksums=sha1_checksums,
            sha256_checksums=sha256_checksums,
            usernames=usernames,
            paths=paths,
            urls=urls,
            ad_domains=ad_domains,
            ad_groups=ad_groups,
            ad_names=ad_names,
        ))

    def iter_raw_events(self, minimum_event_timestamp=None, maximum_event_timestamp=None, event_ids=None,
                        event_names=None, event_types=None, event_descriptions=None, host_ids=None, hostnames=None,
                        ipv4_addresses=None, ipv6_addresses=None, md5_checksums=None, sha1_checksums=None,
                        sha256_checksums=None, usernames=None, paths=None, urls=None, ad_domains=None, ad_groups=None,
                        ad_names=None):

        #: If a minimum event timestamp was not provided, calculate a minimum timestamp using the default backfill.
        if minimum_event_timestamp:
            minimum_event_timestamp = hodgepodge.timestamps.as_epoch_timestamp(minimum_event_timestamp)
        else:
            minimum_event_timestamp = arrow.now().shift(seconds=-self.default_backfill_for_event_data).timestamp

        #: If a maximum event timestamp was provided.
        if maximum_event_timestamp:
            maximum_event_timestamp = hodgepodge.timestamps.as_epoch_timestamp(maximum_event_timestamp)

        event_ids = hodgepodge.helpers.as_set(event_ids, str)
        event_names = hodgepodge.helpers.as_set(event_names, str)
        event_types = hodgepodge.helpers.as_set(event_types, str)
        event_descriptions = hodgepodge.helpers.as_set(event_descriptions, str)
        host_ids = hodgepodge.helpers.as_set(host_ids, str)
        hostnames = hodgepodge.helpers.as_set(hostnames, str)
        ipv4_addresses = hodgepodge.helpers.as_set(ipv4_addresses, str)
        ipv6_addresses = hodgepodge.helpers.as_set(ipv6_addresses, str)
        usernames = hodgepodge.helpers.as_set(usernames, str)
        ad_domains = hodgepodge.helpers.as_set(ad_domains, str)
        ad_groups = hodgepodge.helpers.as_set(ad_groups, str)
        ad_names = hodgepodge.helpers.as_set(ad_names, str)
        paths = hodgepodge.helpers.as_set(paths, str)
        urls = hodgepodge.helpers.as_set(urls, str)
        md5_checksums = hodgepodge.helpers.as_set(md5_checksums, str)
        sha1_checksums = hodgepodge.helpers.as_set(sha1_checksums, str)
        sha256_checksums = hodgepodge.helpers.as_set(sha256_checksums, str)

        hint = log.get_hint(
            minimum_event_timestamp=hodgepodge.helpers.as_human_readable_timestamp(minimum_event_timestamp),
            maximum_event_timestamp=hodgepodge.helpers.as_human_readable_timestamp(maximum_event_timestamp),
            event_ids=event_ids,
            event_names=event_names,
            event_types=event_types,
            event_descriptions=event_descriptions,
            host_ids=host_ids,
            hostnames=hostnames,
            ipv4_addresses=ipv4_addresses,
            ipv6_addresses=ipv6_addresses,
            md5_checksums=md5_checksums,
            sha1_checksums=sha1_checksums,
            sha256_checksums=sha256_checksums,
            usernames=usernames,
            paths=paths,
            urls=urls,
            ad_domains=ad_domains,
            ad_groups=ad_groups,
            ad_names=ad_names,
        )
        log.info(logger, "Searching for events", hint=hint)

        #: Query for events.
        url = 'https://wdatp-alertexporter-us.securitycenter.windows.com/api/alerts'
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token),
        }
        params = self._get_event_query_parameters(
            minimum_event_timestamp=minimum_event_timestamp,
            maximum_event_timestamp=maximum_event_timestamp,
        )
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        #: Filter the stream of events.
        for event in response.json():
            yield event

    def _get_event_query_parameters(self, minimum_event_timestamp, maximum_event_timestamp):
        params = {}

        if minimum_event_timestamp:
            params['sinceTimeUtc'] = arrow.get(minimum_event_timestamp)

        if maximum_event_timestamp:
            params['untilTimeUtc'] = arrow.get(maximum_event_timestamp)

        return params
