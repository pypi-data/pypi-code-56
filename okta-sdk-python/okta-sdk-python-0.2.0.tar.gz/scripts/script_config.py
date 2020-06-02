import json

base_url = "https://wallick.oktapreview.com"
api_token = "006QvPU1GnGVxvCh4GR0Sm5P1Y9iOP75gg4GQCh2Ku"


def load_user():
    with open("scripts/user.json") as json_file:
        user = json.load(json_file)
    return user


def load_factors():
    with open("scripts/enrolled_factors.json") as json_file:
        factors = json.load(json_file)
    return factors


def get_user_id():
    try:
        user = load_user()
        return user.get("id")
    except FileNotFoundError as e:
        print(e)
        print("Make sure your JSON file with test data exists")
        exit(2)


def get_factor_id(provider, factor_type):
    try:
        factors = load_factors()
        for factor in factors:
            if factor["factorType"] == factor_type and factor["provider"] == provider:
                return (factor.get("id"), factor.get("profile"))

        return (None, None)
    except FileNotFoundError as e:
        print(e)
        print("Make sure your JSON file with test data exists")
        exit(2)
