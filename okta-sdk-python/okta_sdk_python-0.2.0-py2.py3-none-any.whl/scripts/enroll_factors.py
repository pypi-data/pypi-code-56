import json
import time

from okta.FactorsClient import FactorsClient
from okta.models.factor.Factor import Factor
from okta.models.Embedded import Embedded
from okta.models.Link import Link
from okta.framework.OktaError import OktaError
from okta.framework.Serializer import Serializer
from script_config import base_url, api_token, get_user_id

factorsClient = FactorsClient(base_url=base_url, api_token=api_token)
user_id = get_user_id()

print("Enrolled factors")
factors = factorsClient.get_lifecycle_factors(user_id)
print(json.dumps(factors, cls=Serializer, indent=2))
print("")

enroll_request = {
    "factorType": "push",
    "provider": "OKTA"
}

response = factorsClient.enroll_factor(user_id, enroll_request)
poll_url = response.links.get("poll").href
qrcode_url = response.embedded.get("activation").links.get("qrcode").href
expires_at = response.embedded.get("activation").expiresAt

print("Enroll push factor started")
print("Expires at: {0}".format(expires_at))
print("")
print("{0}".format(qrcode_url))

factor_result = response.embedded.get("activation").factorResult
while factor_result == "WAITING":
    poll_response = factorsClient.push_activation_poll(poll_url)
    factor_result = poll_response.factorResult or poll_response.status
    if factor_result == "WAITING":
        print("Waiting for confirmation of push enrollment")
        time.sleep(5)
    elif factor_result == "TIMEOUT":
        restart_url = response.links.get("activate").href
        print("Push factor enrollment timed out")
        print("Restart URL: {0}".format(restart_url))
    elif factor_result == "ACTIVE":
        print("Push factor enrolled successfully")
    else:
        print(json.dumps(poll_response, cls=Serializer, indent=2))
        exit(2)
