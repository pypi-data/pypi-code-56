
import json
import pytest
import random


def get_params_from_file(param):
    with open("params_captured.json") as fobj:
        params = json.load(fobj)
    for api, params_info in params.items():
        if param in params_info:
            values = params[api][param]
            if None in values:
                values.remove(None)
            return random.choice(values)




@pytest.fixture(scope="session", autouse=True)
def grant_type():
    return get_params_from_file("grant_type")




@pytest.fixture(scope="session", autouse=True)
def email():
    return get_params_from_file("email")




@pytest.fixture(scope="session", autouse=True)
def client_secret():
    return get_params_from_file("client_secret")




@pytest.fixture(scope="session", autouse=True)
def dummy():
    return get_params_from_file("dummy")




@pytest.fixture(scope="session", autouse=True)
def password():
    return get_params_from_file("password")




@pytest.fixture(scope="session", autouse=True)
def client_id():
    return get_params_from_file("client_id")






@pytest.fixture(scope="session", autouse=True)
def account_id():
    return get_params_from_file("account_id")




@pytest.fixture(scope="session", autouse=True)
def user_idt():
    return get_params_from_file("user_idt")




@pytest.fixture(scope="session", autouse=True)
def beneficiary_id():
    return get_params_from_file("beneficiary_id")




@pytest.fixture(scope="session", autouse=True)
def description():
    return get_params_from_file("description")




@pytest.fixture(scope="session", autouse=True)
def amount():
    return get_params_from_file("amount")




@pytest.fixture(scope="session", autouse=True)
def user_id():
    return get_params_from_file("user_id")




@pytest.fixture(scope="session", autouse=True)
def new_param():
    return get_params_from_file("new_param")






















@pytest.fixture(scope="session", autouse=True)
def page():
    return get_params_from_file("page")












@pytest.fixture(scope="session", autouse=True)
def account_idt():
    return get_params_from_file("account_idt")
















