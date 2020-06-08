#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def token(client_id, client_secret, URL):
    import requests
    import json
    from requests.auth import HTTPBasicAuth
    data = "grant_type=client_credentials"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    r = requests.post("https://public-api.ssg-wsg.sg/dp-oauth/oauth/token", data=data, auth=(client_id,client_secret), headers=headers)
    out = r.json()
    #print(out)
    access_token = out['access_token']
    
    
    import pprint
    
    auth_code = "Bearer " + access_token
    payload = {}
    headers = {'Authorization': auth_code}

    response = requests.request("GET", URL, headers=headers, data = payload)

    response_json  = response.json()
    print("Your access token is: " + access_token)
    print(" ")
    print(" ")
    print("API Output:")
    return pprint.pprint(response_json)
    
token(input("Please enter your Client ID: "),input("Please enter your Secret: "), input("Please enter your Request URL: "))

