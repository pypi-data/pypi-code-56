ACCOUNT_TYPES = ["agency", "vendor", "seller"]

REGIONS = {
    "NA": {
        "AUTHORIZATION": "https://www.amazon.com/ap/oa",
        "TOKEN": "https://api.amazon.com/auth/o2/token",
        "API": "https://advertising-api.amazon.com",
    },
    "EU": {
        "AUTHORIZATION": "https://eu.account.amazon.com/ap/oa",
        "TOKEN": "https://api.amazon.co.uk/auth/o2/token",
        "API": "https://advertising-api-eu.amazon.com",
    },
    "FE": {
        "AUTHORIZATION": "https: // apac.account.amazon.com/ap/oa",
        "TOKEN": "https://api.amazon.co.jp/auth/o2/token",
        "API": "https://advertising-api-fe.amazon.com",
    },
    "SANDBOX": {
        "AUTHORIZATION": "https://www.amazon.com/ap/oa",
        "TOKEN": "https://api.amazon.com/auth/o2/token",
        "API": "https://advertising-api-test.amazon.com",
    }
}

MARKETPLACES = {
    "US": REGIONS.get("NA"),
    "CA": REGIONS.get("NA"),
    "UK": REGIONS.get("EU"),
    "FR": REGIONS.get("EU"),
    "IT": REGIONS.get("EU"),
    "DE": REGIONS.get("EU"),
    "AE": REGIONS.get("EU"),
    "JP": REGIONS.get("FE"),
    "AU": REGIONS.get("FE"),
    "SANDBOX": REGIONS.get("SANDBOX")
}


def get_endpoint(marketplace, endpoint_type=None):
    endpoints = MARKETPLACES.get(marketplace)
    if endpoints is None:
        raise ValueError("marketplace %s is not supported" % marketplace)
    if not endpoint_type:
        return endpoints

    return endpoints.get(endpoint_type)
