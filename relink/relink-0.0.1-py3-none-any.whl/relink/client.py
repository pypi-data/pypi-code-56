import logging
import requests


class RelinkClient:
    API_URL = "https://rel.ink/api/links/"
    RELINK_URL = "https://rel.ink/"

    def shorten_url(self, url: str) -> str:
        try:
            response = requests.post(self.API_URL, json={"url": url})
            response.raise_for_status()
            return self.RELINK_URL + response.json()["hashid"]
        except Exception as error:
            logging.error(f"Could not shorten url, something went wrong : {error}")
            raise

    def get_full_url(self, relink_url: str) -> str:
        try:
            response = requests.get(f"{self.API_URL}{relink_url.replace(self.RELINK_URL, '')}/")
            response.raise_for_status()
            return response.json()["url"]
        except Exception as error:
            logging.error(
                f"Could not get back the full url of the relink url, something went wrong : {error}"
            )
            raise
