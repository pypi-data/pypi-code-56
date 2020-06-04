"""
This modules includes all the tests related to Click cubcommands.
"""

from unittest import mock
import pytest
from click.testing import CliRunner

from requests import HTTPError

from umbrella_cli import cli
from umbrella_cli import services
from umbrella_cli import models

class TestSitesCommands:

    @pytest.fixture
    def credentials(self):
        return [
            "--access", "ACCESS_KEY", "--secret",
            "SECRET_KEY", "--org", "1234567"
        ]

    @mock.patch.object(services.SitesEndpointService, "get_list", autospec=True)
    def test_sites_get_all(self, mock_api_service, credentials):
        """ Test the output of fetching all sites """
        runner = CliRunner()
        mock_api_service.return_value = [
            models.Site(site_id=1479824, name="BLUE"),
            models.Site(site_id=1234567, name="Default Site")
        ]

        result = runner.invoke(cli, credentials + ["sites", "list"])

        assert "Umbrella Sites for Organization" in result.output
        assert "1479824 | BLUE" in result.output

    @mock.patch.object(services.SitesEndpointService, "get_list", autospec=True)
    def test_services_exception_handling(self, mock_api_service, credentials):
        """ Test the exception handling of the service layer """
        runner = CliRunner()
        mock_api_service.side_effect = HTTPError(
            "An error occured in services.")

        result = runner.invoke(cli, credentials + ["sites", "list"])

        assert "An error occured in services." in result.output

    @mock.patch.object(services.SitesEndpointService, "create", autospec=True)
    def test_site_create(self, mock_api_service, credentials):
        runner = CliRunner()
        mock_api_service.return_value = models.Site(site_id=123456, name="TEST")
        
        result = runner.invoke(cli, credentials + ["sites", "create", "TEST"])

        assert "New site created with ID 123456" in result.output