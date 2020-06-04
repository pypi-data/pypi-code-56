"""
    This module contains the test cases of the different commands supported by
    this tool.
"""

from unittest import mock

import pytest
from requests.auth import HTTPBasicAuth
from requests import HTTPError

from umbrella_cli import services
from umbrella_cli import models

class TestManagementApiService:

    """
        Pytest fixtures
    """
    @pytest.fixture
    def single_site(self):
        return {
            "originId": 395218748,
            "isDefault": False,
            "name": "Test",
            "modifiedAt": "2020-04-05T19:07:38.000Z",
            "createdAt": "2020-04-05T19:07:38.000Z",
            "type": "site",
            "internalNetworkCount": 2,
            "vaCount": 4,
            "siteId": 1479824
        }

    @pytest.fixture
    def multiple_sites(self):
        return [
            {
                "originId": 395218748,
                "isDefault": False,
                "name": "BLUE",
                "modifiedAt": "2020-04-05T19:07:38.000Z",
                "createdAt": "2020-04-05T19:07:38.000Z",
                "type": "site",
                "internalNetworkCount": 2,
                "vaCount": 4,
                "siteId": 1479824
            },
            {
                "originId": 136056751,
                "isDefault": True,
                "name": "Default Site",
                "modifiedAt": "2018-03-06T01:23:13.000Z",
                "createdAt": "2018-03-06T01:23:13.000Z",
                "type": "site",
                "internalNetworkCount": 0,
                "vaCount": 0,
                "siteId": 635875
            }
        ]

    def test_get_absolute_url(self):
        """ 
        Check that the URL constructed from the base URL and endpoint is valid
        """
        expected_url = (
            "https://management.api.umbrella.com/v1"
            "/organizations/1234567/"
        )
        api = services.ManagementApiService("ACCESS", "SECRET", 1234567)

        assert expected_url == api._get_absolute_url()

    @mock.patch("umbrella_cli.services.requests.get")
    def test_get_sites_ok(self, mock_requests, multiple_sites):
        """ Test the GET sites with valid data """
        api = services.SitesEndpointService("ACCESS", "SECRET", 1234567)

        assert api.org_id == 1234567
        
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = multiple_sites

        api.get_list()

        mock_requests.assert_called_with(
            url=(
                "https://management.api.umbrella.com"
                "/v1/organizations/1234567/sites"
            ),
            auth=HTTPBasicAuth("ACCESS", "SECRET"),
            headers=api._headers,
            verify=False
        )

    @mock.patch("umbrella_cli.services.requests.post")
    def test_create_site_with_valid_data(self, mock_requests, single_site):
        """ Create a site with valid data """
        api = services.SitesEndpointService("ACCESS", "SECRET", 1234567)

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = single_site

        site = models.Site(name="Test")

        result = api.create(site)

        mock_requests.assert_called_with(
            url=(
                "https://management.api.umbrella.com"
                "/v1/organizations/1234567/sites"
            ),
            auth=HTTPBasicAuth("ACCESS", "SECRET"),
            headers=api._headers,
            json={"name":"Test"},
            verify=False
        )

        assert result.name == "Test"
        assert result.origin_id == 395218748
        assert result.internal_network_count == 2
        

class TestSiteService:
    def test_internal_network_service_url(self):
        """ Validate the generated URL """
        expected_url = (
            "https://management.api.umbrella.com/v1"
            "/organizations/1234567/sites"
        )

        api = services.SitesEndpointService("ACCESS", "SECRET", 1234567)

        assert expected_url == api._get_absolute_url()


class TestInternalNetworkService:
    def test_internal_network_service_url(self):
        """ Validate the generated URL """
        expected_url = (
            "https://management.api.umbrella.com/v1"
            "/organizations/1234567/internalnetworks"
        )

        api = services.InternalNetworkEndpointService("ACCESS", "SECRET", 1234567)

        assert expected_url == api._get_absolute_url()
