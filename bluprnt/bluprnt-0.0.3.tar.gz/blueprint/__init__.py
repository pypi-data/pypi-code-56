import os
from urllib.parse import urljoin
import requests

GCP_PROJECT = os.environ["GCP_PROJECT"]
FUNCTION_REGION = os.environ["FUNCTION_REGION"]


def _get_oidc_token(audience):
    if os.getenv("LOCAL"):
        from subprocess import Popen, PIPE

        return (
            Popen(
                ["gcloud", "auth", "print-identity-token", "--audiences=" + audience],
                stdout=PIPE,
            )
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


def call(name, data):
    try:
        domain = f"https://{FUNCTION_REGION}-{GCP_PROJECT}.cloudfunctions.net"
        url = urljoin(domain, name)
        headers = {"Authorization": "Bearer " + _get_oidc_token(url)}
        r = requests.post(url, headers=headers, json=data)
        return {
            "success": r.status_code < 400,
            "status_code": r.status_code,
            "content": r.json(),
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": None,
            "content": {"message": str(e)},
        }
