import json
import os
import uuid
from pathlib import Path

from requests_oauthlib import OAuth2Session

from .bank import Bank


class OAuthBank(Bank):
    def configure_oauth(self, request_url, token_url, refresh_url):
        self.token_url = token_url
        self.refresh_url = refresh_url
        self.request_url = request_url
        self.client_id = self.config["CLIENT_ID"]
        self.client_secret = self.config["CLIENT_SECRET"]
        self.redirect_uri = self.config["REDIRECT_URI"]

    def get_authenticated_session(self, token):
        # so that if expires_at has passed, we auto-refresh
        token["expires_in"] = -10

        oauth = OAuth2Session(
            self.client_id,
            token=token,
            auto_refresh_url=self.refresh_url,
            auto_refresh_kwargs={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            token_updater=self.save_token,
        )

        return oauth
