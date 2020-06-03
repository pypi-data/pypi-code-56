import sys
import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup as soup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pprint import pprint as pp
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s', level=logging.INFO)


class BNB:
    """
    Webscrape BNB exchange rates for provided date.
    """
    def __ini__(self):
        self.valutes = 'USD'
        # self.rate = None

    def get_page_content(self, url):
        """
        Function to use requests.on provided url,
         with retry and delay between retries.
        """
        s = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=0.3,
                        status_forcelist=[500, 502, 503, 504])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        s.mount('https://', HTTPAdapter(max_retries=retries))
        logger.debug(f'Fetching url: {url}')
        try:
            sleep(0.01)
            res = s.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if res.status_code == requests.codes['ok']:
                return res
        except Exception as exe:
            logger.error(f"Unable to load the url {exe}")
            return None

    def get_rate(self, datetime_str):
        """
        The actual webscraping from bnb.bg
        Input:
        --------
        datetime_str - string with the date - format %d.%m.%Y

        Output:
        dictionary{date: USD/BGN exchange rate}
        """
        target_date = datetime.datetime.strptime(datetime_str, '%d.%m.%Y')
        one_week_before = target_date - datetime.timedelta(days=7)
        T_DAY = f"{target_date.day:02d}"
        T_MONTH = f"{target_date.month:02d}"
        T_YEAR = target_date.year

        S_DAY = f"{one_week_before.day:02d}"
        S_MONTH = f"{one_week_before.month:02d}"
        S_YEAR = one_week_before.year
        logger.debug(target_date.year)
        logger.debug(target_date)
        logger.debug(one_week_before)
        url = (f'http://bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm?'
               f'downloadOper=&group1=second&periodStartDays={S_DAY}&periodStartMonths={S_MONTH}'
               f'&periodStartYear={S_YEAR}'
               f'&periodEndDays={T_DAY}&periodEndMonths={T_MONTH}&periodEndYear={T_YEAR}&valutes=USD'
               '&search=true&showChart=false&showChartButton=true&type=CSV'
               )
        logger.debug(url)
        try:
            soup_bnb = soup(self.get_page_content(url).content, "html.parser")
            table = soup_bnb.find('tbody')
            for row in table.findAll("tr"):
                values = row.findAll("td")
                # print(values[0].text, ' -----', values[2].text)
                last_date = values[0].text
                last_value = values[2].text
            return {last_date: last_value}
        except Exception as exe:
            logger.error(exe)
            return {datetime_str: None}

    def usage(self):
        logger.warning("Usage:\n bnbxrate '05.01.2020' \n The date is in format:%d.%m.%Y")


def main():
    try:
        command = sys.argv[1:]
        print(BNB().get_rate(str(command.pop(0))))
    except Exception as exe:
        BNB().usage()
        logger.error(exe)


if __name__ == '__main__':
    pp(BNB().get_rate('05.04.2020'))
