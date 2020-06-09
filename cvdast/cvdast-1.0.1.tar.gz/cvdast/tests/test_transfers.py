import requests
import json
import pytest

HOST_URL = "34.207.136.8:31314"


def _trigger_requests(req_method, url, header, data, proxies=None):
    print("\n\nRegenerating traffic from CloudVector events....")
    return requests.request(method=req_method, url=url, proxies=proxies, headers=header, data=data, verify=False)


def test_transfers(user_idt, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_idt"] = user_idt
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    response = _trigger_requests("POST", "http://34.207.136.8:31314//transfers",
                      header={'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDQ4ODg3MywidGkiOiJiOGM1ODE0MS02NWJiLTQxZDQtYTJiNi1hYzMxNmY4NjljMmQiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.xetOlcANwlWEtUyfHvO2ylDuNi7CoO28CZdz00P9oRAWJl4j6zAyc21oEmM2wQWa2Lgatt1z65G7MClnhNqeGw', 'Connection': 'keep-alive', 'Content-Length': '81', 'Content-Type': 'application/json', 'Origin': 'http://34.207.136.8:31282', 'Referer': 'http://34.207.136.8:31282/transaction/transfer', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'},
                      data=json.dumps(data))
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200

