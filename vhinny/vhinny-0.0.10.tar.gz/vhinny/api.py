from .common.logger import init_logger
from requests.exceptions import ReadTimeout
import requests
import json


class Vhinny():

    BACKEND_URL = 'https://7pwlq44lyc.execute-api.us-east-1.amazonaws.com/production/api-financials'

    log = init_logger('Vhinny', log_level='INFO')
    log.info('Hello! If you have any questions, API documentation can be found at https://github.com/vhinny-investing/api')

    def __init__(self, **kwargs):
        self.API_KEY = None

    def _send(self, params):
        """
        Send an API request and return the repsonse
        :param params:
        :return:
        """
        try:
            response = requests.get(self.BACKEND_URL, params=params, timeout=5)
            if response.status_code == 204:
                self.log.warning(f'Data requested for (ticker={params["ticker"]}, year={params["year"]}) was not found')
                return None
            data = json.loads(response.text)['data']
        except ReadTimeout:
            raise ReadTimeout("Your request timed out. Please try again later")
        return data

    @staticmethod
    def _clean_response(data, prefix):
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
        if data is not None:
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
        if data is not None:
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
        if data is not None:
            data = self._clean_response(data=data, prefix='cf_')
        return data
