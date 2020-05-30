# coding: utf-8

"""
    Finnhub API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import finnhub
from finnhub.api.default_api import DefaultApi  # noqa: E501
from finnhub.rest import ApiException


class TestDefaultApi(unittest.TestCase):
    """DefaultApi unit test stubs"""

    def setUp(self):
        self.api = finnhub.api.default_api.DefaultApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_aggregate_indicator(self):
        """Test case for aggregate_indicator

        Aggregate Indicators  # noqa: E501
        """
        pass

    def test_company_earnings(self):
        """Test case for company_earnings

        Earnings Surprises  # noqa: E501
        """
        pass

    def test_company_eps_estimates(self):
        """Test case for company_eps_estimates

        Earnings Estimates  # noqa: E501
        """
        pass

    def test_company_executive(self):
        """Test case for company_executive

        Company Executive  # noqa: E501
        """
        pass

    def test_company_metrics(self):
        """Test case for company_metrics

        Metrics  # noqa: E501
        """
        pass

    def test_company_news(self):
        """Test case for company_news

        Company News  # noqa: E501
        """
        pass

    def test_company_peers(self):
        """Test case for company_peers

        Peers  # noqa: E501
        """
        pass

    def test_company_profile(self):
        """Test case for company_profile

        Company Profile  # noqa: E501
        """
        pass

    def test_company_profile2(self):
        """Test case for company_profile2

        Company Profile 2  # noqa: E501
        """
        pass

    def test_company_revenue_estimates(self):
        """Test case for company_revenue_estimates

        Revenue Estimates  # noqa: E501
        """
        pass

    def test_covid19(self):
        """Test case for covid19

        COVID-19  # noqa: E501
        """
        pass

    def test_crypto_candles(self):
        """Test case for crypto_candles

        Crypto Candles  # noqa: E501
        """
        pass

    def test_crypto_exchanges(self):
        """Test case for crypto_exchanges

        Crypto Exchanges  # noqa: E501
        """
        pass

    def test_crypto_symbols(self):
        """Test case for crypto_symbols

        Crypto Symbol  # noqa: E501
        """
        pass

    def test_earnings_calendar(self):
        """Test case for earnings_calendar

        Earnings Calendar  # noqa: E501
        """
        pass

    def test_filings(self):
        """Test case for filings

        Filings  # noqa: E501
        """
        pass

    def test_financials(self):
        """Test case for financials

        Financial Statements  # noqa: E501
        """
        pass

    def test_financials_reported(self):
        """Test case for financials_reported

        Financials As Reported  # noqa: E501
        """
        pass

    def test_forex_candles(self):
        """Test case for forex_candles

        Forex Candles  # noqa: E501
        """
        pass

    def test_forex_exchanges(self):
        """Test case for forex_exchanges

        Forex Exchanges  # noqa: E501
        """
        pass

    def test_forex_rates(self):
        """Test case for forex_rates

        Forex rates  # noqa: E501
        """
        pass

    def test_forex_symbols(self):
        """Test case for forex_symbols

        Forex Symbol  # noqa: E501
        """
        pass

    def test_fund_ownership(self):
        """Test case for fund_ownership

        Fund Ownership  # noqa: E501
        """
        pass

    def test_general_news(self):
        """Test case for general_news

        General News  # noqa: E501
        """
        pass

    def test_investors_ownership(self):
        """Test case for investors_ownership

        Investors Ownership  # noqa: E501
        """
        pass

    def test_ipo_calendar(self):
        """Test case for ipo_calendar

        IPO Calendar  # noqa: E501
        """
        pass

    def test_major_developments(self):
        """Test case for major_developments

        Major Developments  # noqa: E501
        """
        pass

    def test_news_sentiment(self):
        """Test case for news_sentiment

        News Sentiment  # noqa: E501
        """
        pass

    def test_pattern_recognition(self):
        """Test case for pattern_recognition

        Pattern Recognition  # noqa: E501
        """
        pass

    def test_price_target(self):
        """Test case for price_target

        Price Target  # noqa: E501
        """
        pass

    def test_quote(self):
        """Test case for quote

        Quote  # noqa: E501
        """
        pass

    def test_recommendation_trends(self):
        """Test case for recommendation_trends

        Recommendation Trends  # noqa: E501
        """
        pass

    def test_stock_candles(self):
        """Test case for stock_candles

        Stock Candles  # noqa: E501
        """
        pass

    def test_stock_dividends(self):
        """Test case for stock_dividends

        Dividends  # noqa: E501
        """
        pass

    def test_stock_splits(self):
        """Test case for stock_splits

        Splits  # noqa: E501
        """
        pass

    def test_stock_symbols(self):
        """Test case for stock_symbols

        Stock Symbol  # noqa: E501
        """
        pass

    def test_stock_tick(self):
        """Test case for stock_tick

        Tick Data  # noqa: E501
        """
        pass

    def test_support_resistance(self):
        """Test case for support_resistance

        Support/Resistance  # noqa: E501
        """
        pass

    def test_technical_indicator(self):
        """Test case for technical_indicator

        Technical Indicators  # noqa: E501
        """
        pass

    def test_transcripts(self):
        """Test case for transcripts

        Earnings Call Transcripts  # noqa: E501
        """
        pass

    def test_transcripts_list(self):
        """Test case for transcripts_list

        Earnings Call Transcripts List  # noqa: E501
        """
        pass

    def test_upgrade_downgrade(self):
        """Test case for upgrade_downgrade

        Stock Upgrade/Downgrade  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
