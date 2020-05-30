from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup
#from selenium import webdriver


@dataclass
class Scraper:
    #driver: Optional[webdriver.Chrome] = None

    # @property
    # def soup(self):
    #     if not self.driver:
    #         raise TypeError("Driver not started")
    #     return BeautifulSoup(self.driver.page_source, 'html.parser')

    @staticmethod
    def make_request(url: str, json_=False) -> BeautifulSoup:
        headers = {
            'user-agent': 'Googlebot'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if json_:
            return response.json()
        return BeautifulSoup(response.content, 'html.parser')
