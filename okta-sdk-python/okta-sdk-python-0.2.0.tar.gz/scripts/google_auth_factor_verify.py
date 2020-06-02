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
factor_id, factor_profile = get_factor_id("GOOGLE", "token:software:totp")

print("Verifying Google Authenticator")
result = "WAITING"

while result != "SUCCESS":
    try:
        pass_code = input("Enter your OTP --> ")
        response = factorsClient.verify_factor(user_id, factor_id, passcode=pass_code)
        result = response.factorResult
        print("Google Authenticator verification passed")
    except OktaError as e:
        print(e.error_causes)
