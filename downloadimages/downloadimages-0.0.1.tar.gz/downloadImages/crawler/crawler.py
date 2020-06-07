import requests

from . import defaultConfig


class Crawler:

    def __init__(self, cookies_dict=None, user_agent=None, headers=None, use_session=False):
        self._session = requests.Session()

        self._cookies_dict = cookies_dict
        self._user_agent = user_agent
        self._headers = headers
        self._use_session = use_session

        if cookies_dict:
            self._session.cookies.update(cookies_dict)
        if headers:
            self._session.headers.update(headers)
        if user_agent:
            user_agent_header = {"User-Agent": user_agent}
        else:
            user_agent_header = {"User-Agent": defaultConfig.user_agent}
        self._session.headers.update(user_agent_header)

    def _get(self, url):
        if not self._use_session:
            self._session.cookies.clear()
        return self._session.get(url)

    def get_text(self, url):
        print("get_text")
        rep = self._get(url)
        return rep.text

    def get_bin_data(self, url):
        rep = self._get(url)
        return rep.content

    def _post(self, url, form=None, json=None):
        if form and json:
            raise Exception("only form or json")
        return self._session.post(url, data=form, json=json)

    def post_get_text(self, url, form, json):
        rep = self._post(url, form, json)
        return rep.text

    def post_get_bin_data(self, url, form, json):
        rep = self._post(url, form, json)
        return rep.content
