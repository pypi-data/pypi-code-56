import config
import requests



class Client:
    def __init__(self, cfg: config.Config):
        self.cfg = cfg
    

    def login(self, phone: str, password: str, org: str):
        response = requests.post(self.cfg.base_url + "/v1/auth/login", json={
            "phone": phone,
            "password": password,
            "creditorOrganizationId": org
        })
        if response.status_code != 200:
            raise Exception("login failed")
        data = response.json()
        token = data["user"]["token"]
        self.cfg.set("phone", phone)
        self.cfg.set("password", password)
        self.cfg.set("org", org)
        self.cfg.set("token", token)
        self.cfg.save()
            