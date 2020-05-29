# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_python
from pulpcore.client.pulp_python.models.repository_sync_url import RepositorySyncURL  # noqa: E501
from pulpcore.client.pulp_python.rest import ApiException

class TestRepositorySyncURL(unittest.TestCase):
    """RepositorySyncURL unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RepositorySyncURL
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_python.models.repository_sync_url.RepositorySyncURL()  # noqa: E501
        if include_optional :
            return RepositorySyncURL(
                remote = '0', 
                mirror = True
            )
        else :
            return RepositorySyncURL(
                remote = '0',
        )

    def testRepositorySyncURL(self):
        """Test RepositorySyncURL"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
