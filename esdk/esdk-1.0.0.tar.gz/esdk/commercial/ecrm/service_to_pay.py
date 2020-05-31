
class ServiceToPay:
    """
    ecrm service payment class

    Attributes: 
        service (dict): ecrm service object
    """
    def __init__(self, account_state_eid,service_type,service_name,amount):
        """ 
        Constructor 
  
        Parameters: 
            account_state_eid (str): Service account.        
            service_name (str): Service name.        
            service_type (str): Service type, can be found in api_constants.        
            amount (float): Amount to pay.        
         
        """
        self.service = {'account_state_eid': account_state_eid,
                                   'service_typology': service_type,
                                   'service_name': service_name, 'real_import': amount}
        
    def get_service(self):
        """ 
        The function to returns service to pay 
  
        Returns: 
            service (dict): ecrm service object        
        """
        return self.service    
        
