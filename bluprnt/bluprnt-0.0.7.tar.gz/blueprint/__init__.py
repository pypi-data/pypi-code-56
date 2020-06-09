import os
import json
import logging
from urllib.parse import urljoin
from base64 import urlsafe_b64decode
import requests

GCP_PROJECT = os.environ["GCP_PROJECT"]
FUNCTION_REGION = os.environ["FUNCTION_REGION"]


class ServiceError(Exception):
    def __init__(self, status_code, message):
        if status_code >= 500:
            logging.error(message)
        else:
            logging.warning(message)
        super().__init__(message)


def _get_oidc_token(audience):
    if os.getenv("LOCAL"):
        from subprocess import Popen, PIPE

        return (
            Popen(["gcloud", "auth", "print-identity-token"], stdout=PIPE)
            .communicate()[0][:-1]
            .decode()
        )
    token_url = (
        "http://metadata.google.internal"
        "/computeMetadata/v1/instance/service-accounts/default/identity"
        f"?audience={audience}"
    )
    return requests.get(
        url=token_url, headers={"Metadata-Flavor": "Google"},
    ).content.decode()


def call(name, data=None):
    domain = f"https://{FUNCTION_REGION}-{GCP_PROJECT}.cloudfunctions.net"
    url = urljoin(domain, name)
    headers = {"Authorization": "Bearer " + _get_oidc_token(url)}
    logging.info("Service call: %s %s", name, data)
    r = requests.post(url, headers=headers, json=data)
    r.raise_for_status()
    return r.json()


def user_info(request):
    encoded_user_info = request.headers.get("X-Endpoint-Api-Userinfo")
    if encoded_user_info:
        if not encoded_user_info.endswith("=="):
            encoded_user_info += "=="
        return json.loads(urlsafe_b64decode(encoded_user_info))
    return None
