from dataclasses import dataclass
from .api_credentials import APICredentials
from .api_constants import APIConstants
import requests
import json
from requests.exceptions import ConnectionError

@dataclass(order=False)
class APIOperations:
    """
    ecrm Operation class

    Attributes: 
        credentials (APICredentials): ecrm credentials  
        test (bool): ecrm enviroment, default false

    """

    credentials: APICredentials
    test: bool = False

    def __raise__(self,msg):
        """ 
        The function to raise excepcion with message. 
  
        Parameters: 
            msg (str): Message for excepcion raising.        
         
        """
        raise Exception(msg)

    def __check__parameters(self,credentials: APICredentials,services: list, services_keys: list) -> str:
        """ 
        The function to check parameters. 
  
        Parameters: 
            credentials (APICredentials): ecrm credentials  
            services (list): services list  
            services_keys (list): services keys to evaluate
            
        Returns:
            url (str): Return enviroment url
              
        """
        
        if not isinstance(credentials, APICredentials):
            self.__raise__("Incorrect Credentials")

        if not isinstance(self.test, bool):
            self.__raise__("Incorrect Enviroment")

        if not isinstance(services, list) or len(services) == 0:
            self.__raise__("Incorrect Services")

        for service in services:
            if not isinstance(service, dict):
                self.__raise__("Incorrect Service Format")

            else:
                for key in services_keys:
                    if not isinstance(key,str) or not key in service:
                        self.__raise__("Incorrect Service Format")

        if self.test:
            return APIConstants.URL_ENVIROMENT_TEST
        else:
            return APIConstants.URL_ENVIROMENT_PROD

    #Services Methods
    def servicesvalidate(self, services: list):      

        """ 
        The function to validate services. 
  
        Parameters: 
            services (list): services list  
            
        Returns:
            response (dict): Dict that contain request info
              
        """
        

        url = self.__check__parameters(self.credentials,services,['service_type','service_name'])

        try:
            response = requests.post( f'{url}/services/contract/validate_srv/',
                                                 params={
                                                     'lst': json.dumps(services)},
                                                 auth=self.credentials.getAuth())
        except ConnectionError as error:
            return {'success': False, 'error': 'Network Error', 'error_detail': str(error)}

        if response.status_code != 200:
            return {'success': False, 'error': response.reason, 'error_detail': response.reason}

        response_json = response.json()

        if response_json['success']:
            return {'success': True, 'data': response_json['data']}

        return {'success': False, 'error': response_json['errormsg'], 'error_detail': response_json['errormsg']}

    def servicespayment(self, services: list, order_id: str, source: str, payment_method: str, currency: str):
        """ 
        The function to validate services. 
  
        Parameters: 
            services (list): services list  
            order_id (str): App order id  
            source (str): Source that execute services payment  
            payment_method (str): Payment method, example, Transfermovil, EnZona.  
            currency (str): Payment currency.
            
        Returns:
            response (dict): Dict that contain request info
              
        """

        url = self.__check__parameters(self.credentials,services,['account_state_eid','service_typology','service_name','real_import'])

        if not isinstance(order_id,str) or len(order_id) == 0:
            self.__raise__("Incorrect Order ID")

        elif not isinstance(source,str) or len(source) == 0:
            self.__raise__("Incorrect Source")

        elif not isinstance(payment_method,str) or len(payment_method) == 0:
            self.__raise__("Incorrect payment Type")

        elif not isinstance(currency,str) or len(currency) == 0:
            self.__raise__("Incorrect Currency")

        try:
            response = requests.post(
                f'{url}/services/paymentms/add_virtual_extern_payment',
                params={'transaction_number': order_id,
                        'source_type': source,
                        'payment_type': payment_method,
                        'currency': currency,
                        'lst_invoices': json.dumps(services)},
                auth=self.credentials.getAuth())

        except ConnectionError as error:
            return {'success': False, 'error': 'Network Error', 'error_detail': str(error)}

        if response.status_code != 200:
            return {'success': False, 'error': response.reason, 'error_detail': response.reason}

        response_json = response.json()

        if response_json['success']:
            return {'success': True, 'data': response_json['data']}

        return {'success': False, 'error': response_json['errormsg'], 'error_detail': response_json['errormsg']}


