import datetime

import pytest


def test_Import():
    from elexon import ElexonRawClient

# def test_ElexonRawClient():
#     """Tests an API call to get a TV show's info"""
#
#     client = ElexonRawClient('muqgoc24efh0trr') # available for free from the Elexon Portal
#
#     # Actual Aggregated Generation per Type
#     generation1 = api.Transparency.B1620(SettlementDate = '2020-01-01', Period = '5')
#     # Alternatively, use the general request() function by passing the endpoint in with the arguments:
#     generation2 = api.request('B1620', SettlementDate = '2020-01-01', Period = '5')
#
#     assert generation1==generation2
#     # assert isinstance(response, dict)
#     # assert response['id'] == 1396, "The ID should be in the response"
#     # assert set(tv_keys).issubset(response.keys()), "All keys should be in the response"
