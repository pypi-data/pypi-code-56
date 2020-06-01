import requests
import json


class Vhinny:

    BACKEND_URL = 'https://7pwlq44lyc.execute-api.us-east-1.amazonaws.com/production/api-financials'

    def __init__(self, **kwargs):
        self.API_KEY = None

    def _send(self, params):
        """
        Send an API request and return the repsonse
        :param params:
        :return:
        """
        response = requests.get(self.BACKEND_URL, params=params, timeout=1.5)
        data = json.loads(response.text)['data']
        return data

    def _clean_response(self, data, prefix):
        """
        Cleaup returned response: remove prefixes and sort by the alphabetical order
        :param data:dict
        :param prefix:string
        :return:
        """
        out = {}
        for key in sorted(data):
            out[key.replace(prefix, '')] = data[key]
        return out

    def balance_sheet(self, ticker, year):
        """
        Request Balance Sheet Data
        :param ticker:str - Ticker
        :param year:int - Fiscal Year
        :return:
        """
        params = {
            'statement_type_id': 2,
            'ticker': ticker.upper(),
            'year': int(year),
        }
        data = self._send(params)
        data = self._clean_response(data=data, prefix='bs_')
        return data

    def income_statement(self, ticker, year):
        """
        Request Income Statement Data
        :param ticker:str - Ticker
        :param year:int - Fiscal Year
        :return:
        """
        params = {
            'statement_type_id': 1,
            'ticker': ticker.upper(),
            'year': int(year),
        }
        data = self._send(params)
        data = self._clean_response(data=data, prefix='is_')

        return data

    def cash_flows(self, ticker, year):
        """
        Request Balance Sheet Data
        :param ticker:str - Ticker
        :param year:int - Fiscal Year
        :return:
        """
        params = {
            'statement_type_id': 3,
            'ticker': ticker.upper(),
            'year': int(year),
        }
        data = self._send(params)
        data = self._clean_response(data=data, prefix='cf_')
        return data
