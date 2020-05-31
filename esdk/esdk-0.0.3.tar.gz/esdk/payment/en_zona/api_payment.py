from dataclasses import dataclass
import requests
from requests.exceptions import ConnectionError
import base64
from .api_constants import APIConstants
from .api_credentials   import APICredentials
from requests.auth import HTTPBasicAuth
@dataclass(order=False)
class APIPayment:
    
    test: bool = False
    ssl_verify: bool = False
    
    def generate_token(self, credentials: APICredentials, scope: str = APIConstants.SCOPE_ALL):
        if self.test == False:
            url = f"{APIConstants.URL_ENVIROMENT_PROD}/token"
        else:
            url = f"{APIConstants.URL_ENVIROMENT_TEST}/token"
            
        
        payload = {
            "grant_type": "client_credentials",
            "scope": scope,
        }
        
        try:
            response = requests.post("https://apisandbox.enzona.net/token", headers={"Content-Type": "application/json"}, json={
                "grant_type": "client_credentials",
                "scope": scope
            })
        except ConnectionError as error:
            return {'success': False, 'error': 'Network Error', 'error_detail': str(error)}
        
        a = response    
            
        
        
        
        
credentials = APICredentials("consumer_key","consumer_secret")
    
a = APIPayment()
a.generate_token(credentials)
    



