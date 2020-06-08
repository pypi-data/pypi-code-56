from datetime import datetime, timedelta
import config
import requests



class Client:
    def __init__(self, cfg: config.Config):
        self.cfg = cfg
    
    def path(self, endpoint: str) -> str:
        return self.cfg.base_url + endpoint

    def login(self, phone: str, password: str, org: str) -> str :
        response = requests.post(self.path("/v1/auth/login"), json={
            "phone": phone,
            "password": password,
            "creditorOrganizationId": org
        })
        if response.status_code != 200:
            raise Exception("login failed")
        data = response.json()
        token = data["user"]["token"]
        expiration = datetime.now() + timedelta(hours=24)
        self.cfg.set("phone", phone)
        self.cfg.set("password", password)
        self.cfg.set("org", org)
        self.cfg.set("token", token)
        self.cfg.set("expiration", str(expiration))
        self.cfg.save()
        return token

    def token(self) -> str:
        token = self.cfg.get("token")
        
        if not token:
            raise Exception("your are not logged in")

        expiration = datetime.fromisoformat(self.cfg.get("expiration"))

        if datetime.now() > expiration:
            phone = self.cfg.get("phone")
            password = self.cfg.get("password")
            org = self.cfg.get("org")
            return self.login(phone, password, org)

        return token
    

    def approve_disbursement(self, credit_id: str):
        token = self.token()
        url = self.path("/v1/assistant/disbursements/approve") 
        payload = {"creditId": credit_id }
        headers = {"authorization": f"Bearer {token}"}
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if response.status_code != 200:
            code = data["data"]["code"]
            raise Exception(f"disbursement approvation failed: {code}")
        return data

    def check_disbursement(self, credit_id: str):
        token = self.token()
        url = self.path("/v1/assistant/disbursements/check") 
        payload = {"creditId": credit_id }
        headers = {"authorization": f"Bearer {token}"}
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if response.status_code != 200:
            code = data["data"]["code"]
            raise Exception(f"disbursement check failed: {code}")
        return data
            