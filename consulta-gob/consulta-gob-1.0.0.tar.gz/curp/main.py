import requests

URL = "https://curp-api.mx/api/consulta"
def consulta_CURP(CURP, TOKEN):
    payload = {
    "curp" : CURP,
    "api_token" : TOKEN
    }

    response = requests.get(url, json = payload)
    return response
