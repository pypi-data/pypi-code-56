import requests
import math
import json

web3_host = "http://47.74.218.178:8111"

def get_eth_balance(address):
    res = call(web3_host, 'eth_getBalance', [address, 'latest'])
    return int(res, 16) / math.pow(10, 18)

def get_usdt_balance(address):
    return get_token_balance(address, '0xdac17f958d2ee523a2206206994597c13d831ec7', 6)


def get_token_balance(address, contract, decimals):
    res = call(web3_host, "eth_call", [{'data': '0x70a08231000000000000000000000000' + address[2:], 'to': contract}, 'latest'])
    return int(res, 16) / math.pow(10, decimals)


def call(host, method, params=[]):
    headers = {
        "Content-Type": "application/json",
        "X-Client": "CPY-ETH"
    }
    data = {
        'id': 1,
        'method': method,
        'jsonrpc': '2.0',
        'params': params
    }
    # print(json.dumps(data))

    res = requests.post(host, headers=headers, data=json.dumps(data))
    # print(res.text)
    res = json.loads(res.text)
    return res['result']