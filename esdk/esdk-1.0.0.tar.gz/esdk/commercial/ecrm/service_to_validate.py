class ServiceToValidate:
    """
    ecrm service validate class

    Attributes: 
        service (dict): ecrm service object
    """
    
    def __init__(self, service_name,service_type):
        """ 
        Constructor 
  
        Parameters: 
            service_name (str): Service name.        
            service_type (str): Service type, can be found in api_constants.        
         
        """
        self.service = {"service_name": service_name,"service_type": service_type}
        
    def get_service(self):
        """ 
        The function to returns service to validate 
  
        Returns: 
            service (dict): ecrm service object        
        """
        return self.service    
        
