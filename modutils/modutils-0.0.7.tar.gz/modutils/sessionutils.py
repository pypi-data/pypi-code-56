import logging

from functools import partial
from requests import Session, Response
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter

from typing import Union, Text

class BaseSession(Session):
    retries: int
    verbose: bool

    def __init__(self, max_retries: int = 3, pool_connections: int = 16, pool_maxsize: int = 16,
                 resolve_status_codes: list = None, verbose: bool = False, auth: tuple = None):
        super().__init__()
        adapters = HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize,
                                    max_retries=max_retries)
        self.mount("https://", adapters)
        self.mount('http://', adapters)
        self.retries = max_retries
        self.verbose = verbose
        self.resolve_status_codes = [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
        if isinstance(resolve_status_codes, int):
            self.resolve_status_codes.append(resolve_status_codes)
        elif isinstance(resolve_status_codes, list):
            for sc in resolve_status_codes:
                if isinstance(sc, int):
                    self.resolve_status_codes.append(sc)

        if auth:
            self.auth = HTTPBasicAuth(*auth)

        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        self.session_logger = logging.getLogger(name='BaseSession')
        self._log_msg_fmt = '{method}, {scheme}, {host}, {path}, {content_size}, {user_agent}, {status_code}'


    def _log_response(self, response: Response) -> None:
        """log each requests/response from resolver"""
        self.session_logger.info(self._log_msg_fmt.format(
            scheme=response.url.split("://")[0], host=response.url.split('/')[2], method=response.request.method,
            path=response.request.path_url, status_code=response.status_code, content_size=len(response.content),
            user_agent=response.request.headers.get("User-Agent", "Unknown")))
        if response.status_code >= 300 and self.verbose:
            self.session_logger.error(f'REPONSE: {response.text}')

    def _resolver(self, request: partial) -> Response:
        """attempt to resolve a requests with an invalid status code

        if the status code of the requests is not one to resolve:
            Default:  [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
        the requests will be sent up to max_retries or until receiving an accepted status_code

        :param request: partial requests function to be used to attempt and resolve a valid response

        :return: response from the requests
        """
        attempt = 1
        resp = request()
        while attempt <= self.retries and resp.status_code not in self.resolve_status_codes:
            resp = request()
            attempt += 1
        self._log_response(resp)
        return resp

    def get(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session get
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self._resolver(partial(super(BaseSession, self).get, url, **kwargs))

    def head(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session head
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self._resolver(partial(super(BaseSession, self).head, url, **kwargs))

    def delete(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session delete
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self._resolver(partial(super(BaseSession, self).delete, url, **kwargs))

    def patch(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session patch
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self._resolver(partial(super(BaseSession, self).patch, url, **kwargs))

    def post(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session post
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self._resolver(partial(super(BaseSession, self).post, url, **kwargs))

    def put(self, url: Union[Text, bytes], **kwargs) -> Response:
        """ override of requests.Session put
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        """
        return self._resolver(partial(super(BaseSession, self).put, url, **kwargs))






