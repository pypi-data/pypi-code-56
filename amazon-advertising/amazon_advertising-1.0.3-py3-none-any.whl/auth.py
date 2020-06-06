import requests
from .config import get_endpoint


class Auth(object):

    def __init__(self, client_id: str,  client_secret: str, redirect_uri: str, marketplace="US", scope: str = "cpc_advertising:campaign_management"):
        """
        scope:
            The OAuth 2.0 permission scope used to limit the application's access to an advertiser's account.
            For the Sponsored Brands, Sponsored Display, and Sponsored Products APIs, set scope to cpc_advertising:campaign_management.
            For the Data Provider API, set scope to advertising::audiences.
            For the DSP API, set scope to advertising::campaign_management.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        # get api endpoint
        self.endpoints = get_endpoint(marketplace)
        self.marketplace = marketplace

    @property
    def authorization_url(self):
        return self.endpoints.get("AUTHORIZATION")

    def get_token(self, grant_type: str, code: str):
        """
        grant_type
            refresh_token
            authorization_code

        """

        token_url = self.endpoints.get("TOKEN")

        data = {
            "grant_type": grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        if grant_type == "refresh_token":
            data["refresh_token"] = code
        else:
            data["code"] = code

        r = requests.post(token_url, data=data)

        if r.status_code == 200:
            return r.json()
