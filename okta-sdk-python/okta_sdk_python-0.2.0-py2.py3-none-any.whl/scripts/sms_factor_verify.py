import json

from okta.FactorsClient import FactorsClient
from okta.framework.OktaError import OktaError
from okta.framework.Serializer import Serializer
from script_config import (
    api_token,
    base_url,
    get_factor_id,
    get_user_id
)

factorsClient = FactorsClient(base_url=base_url, api_token=api_token)
user_id = get_user_id()
factor_id, factor_profile = get_factor_id("OKTA", "sms")

print("Issuing SMS challenge...{0}".format(factor_profile.get("phoneNumber")))

# issue the challenge
response = factorsClient.verify_factor(user_id, factor_id)
result = response.factorResult

while result != "SUCCESS":
    try:
        pass_code = input("Enter your OTP --> ")
        response = factorsClient.verify_factor(
            user_id, factor_id, passcode=pass_code)
        result = response.factorResult
        print("SMS verification passed")
    except OktaError as e:
        print(e.error_causes)
