import requests
from .abstract_request import AbstractRequest
from .config import get_endpoint


class Client(object):

    def __init__(self, client_id,  access_token, profile_id=None, marketplace="US", timeout=6, raise_for_status=True):
        self.client_id = client_id
        self.access_token = access_token
        self.profile_id = profile_id
        self.timeout = 6
        self.raise_for_status = raise_for_status

        # get api endpoint
        self.api_url = get_endpoint(marketplace, "API")
        self.marketplace = marketplace

    def build_url(self, endpoint: str):
        if endpoint.startswith("http"):
            return endpoint
        return self.api_url + endpoint

    def make_default_headers(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % self.access_token,
            "Amazon-Advertising-API-ClientId": self.client_id,
        }
        if self.profile_id is not None:
            headers.update(
                {
                    "Amazon-Advertising-API-Scope": self.profile_id
                }
            )
        return headers

    def build_request(self, url, request: AbstractRequest) -> requests.Request:
        # build request args
        body = request.build_args()

        method = request.method.upper()
        req = requests.Request(method, url)
        if body:
            if req.method in ["POST", "PUT", "PATH"]:
                req.json = body
            else:
                req.params = body
        req.headers = self.make_default_headers()

        return req

    def send(self, request: AbstractRequest) -> requests.Response:
        # build url
        url = self.build_url(request.api)

        # build requests.Request and send it
        req = self.build_request(url, request)

        prepped = req.prepare()
        s = requests.Session()
        resp = s.send(prepped, stream=request.stream, timeout=self.timeout)

        if self.raise_for_status == True:
            resp.raise_for_status()

        try:
            build_response = getattr(request, "build_response")
            if callable(build_response):
                return build_response(resp)
        except AttributeError:
            pass

        return resp
