import requests
import json
import pytest

HOST_URL = "34.207.136.8:31314"


def _trigger_requests(req_method, url, header, data, proxies=None):
    print("\n\nRegenerating traffic from CloudVector events....")
    return requests.request(method=req_method, url=url, proxies=proxies, headers=header, data=data, verify=False)


def test_oauth_token(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    response = _trigger_requests("POST", "http://34.207.136.8:31314/oauth/token",
                      header={'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8', 'Authorization': 'Bearer', 'Connection': 'keep-alive', 'Content-Length': '238', 'Content-Type': 'application/json', 'Origin': 'http://34.207.136.8:31282', 'Referer': 'http://34.207.136.8:31282/login', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'},
                      data=json.dumps(data))
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200

