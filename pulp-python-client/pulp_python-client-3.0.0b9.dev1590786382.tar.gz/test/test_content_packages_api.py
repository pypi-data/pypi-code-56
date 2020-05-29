# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import pulpcore.client.pulp_python
from pulpcore.client.pulp_python.api.content_packages_api import ContentPackagesApi  # noqa: E501
from pulpcore.client.pulp_python.rest import ApiException


class TestContentPackagesApi(unittest.TestCase):
    """ContentPackagesApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_python.api.content_packages_api.ContentPackagesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create(self):
        """Test case for create

        Create a python package content  # noqa: E501
        """
        pass

    def test_list(self):
        """Test case for list

        List python package contents  # noqa: E501
        """
        pass

    def test_read(self):
        """Test case for read

        Inspect a python package content  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
