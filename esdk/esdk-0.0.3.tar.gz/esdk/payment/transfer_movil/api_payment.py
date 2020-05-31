from dataclasses import dataclass
import requests
import validators
from .api_payload import APIPayload
from .api_credentials import APICredentials
from requests.exceptions import ConnectionError
from .api_constants import APIConstants

@dataclass(order=False)
class APIPayment:
    
    """
    transfermovil payment class
    
    Attributes:
        test(bool): Transfermovil enviroment
        ssl_verify(bool): Verify ssl certificate, default false.
        
    """
      
    test: bool = False
    ssl_verify: bool = False

    
    def charge(self,credential: APICredentials, payload: APIPayload) -> dict:
        """ 
        The function to create payment. 
        
        Parameters:
            credential(APICredentials): request credential
            payload(APIPayload): request payload
  
        Returns:
            response(dict): Request response
              
        """        
        
        if not isinstance(self.ssl_verify, bool):
            raise Exception("Incorrect ssl_verified")
        if not isinstance(credential, APICredentials):
            raise Exception("Incorrect credentials")
        if not isinstance(payload,APIPayload):
            raise Exception("Incorrect payload")
        
        if self.test:
            url = APIConstants.URL_ENVIROMENT_TEST
        else:
            url = APIConstants.URL_ENVIROMENT_PROD    

        try:
            response = requests.post(url,
                                     headers=credential.getheaders(),
                                     json=payload.getPayload(),
                                     verify=self.ssl_verify)
        except ConnectionError as error:
            return {'success': False, 'error': 'Network Error', 'error_detail': str(error)}

        if response.status_code != 200:
            return {'success': False, 'error': response.reason, 'error_detail' : None}
        else:
            json = response.json()

            if json['PayOrderResult']['Success'] != True:
                return {'success': False, 'error': json['PayOrderResult']['Resultmsg']}

            return {'success': True}






