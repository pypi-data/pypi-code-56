# coding: utf-8

"""
    Finnhub API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import finnhub
from finnhub.models.investor import Investor  # noqa: E501
from finnhub.rest import ApiException

class TestInvestor(unittest.TestCase):
    """Investor unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Investor
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = finnhub.models.investor.Investor()  # noqa: E501
        if include_optional :
            return Investor(
                name = '0', 
                share = 56, 
                turnover = '0', 
                turnover_percent = 1.337, 
                change = 56, 
                filing_date = datetime.datetime.strptime('1975-12-30', '%Y-%m-%d').date()
            )
        else :
            return Investor(
        )

    def testInvestor(self):
        """Test Investor"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
