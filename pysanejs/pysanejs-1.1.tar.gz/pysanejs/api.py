#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
from urllib.parse import urljoin
from typing import Union


class SaneJS():

    def __init__(self, root_url: str='https://sanejs.circl.lu/'):
        self.root_url = root_url
        self.session = requests.session()

    @property
    def is_up(self):
        try:
            r = self.session.head(self.root_url)
            return r.status_code == 200
        except Exception:
            return False

    def sha512(self, sha512: Union[str, list]) -> dict:
        r = self.session.post(self.root_url, data=json.dumps({'sha512': sha512}))
        return r.json()

    def library(self, library: Union[str, list], version: str=None) -> dict:
        to_query = {'library': library}
        if version:
            to_query['version'] = version
        r = self.session.post(urljoin(self.root_url, 'library'), data=json.dumps(to_query))
        return r.json()
