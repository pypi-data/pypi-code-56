import getpass
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
factor_id, factor_profile = get_factor_id("OKTA", "question")

print("Verifying security question")
question = factor_profile.get("questionText")
result = "WAITING"

while result != "SUCCESS":
    try:
        #answer = input("{0} --> ".format(question))
        answer = getpass.getpass("{0} --> ".format(question))
        response = factorsClient.verify_factor(user_id, factor_id, answer=answer)
        result = response.factorResult
        print("Security question verification passed")
    except OktaError as e:
        print(e.error_causes)
