from dataclasses import dataclass
from requests.auth import HTTPBasicAuth

@dataclass(order=False)
class APICredentials:
    """
    ecrm Credentials class

    Attributes: 
        username (str): ecrm webservice username  
        password (str): ecrm webservice password  

    """
    username: str
    password: str

    def getAuth(self) -> HTTPBasicAuth:
        """ 
        The function to get ecrm authentication. 
  
        Parameters: 
            username (str): ecrm webservice username  
            password (str): ecrm webservice password
          
        Returns: 
            HTTPBasicAuth: Basic authentication header. 
        """
        if not isinstance(self.username, str) or len(self.username) == 0:
            raise Exception("Incorrect Username")

        elif not isinstance(self.password, str) or len(self.password) == 0:
            raise Exception("Incorrect password")

        return HTTPBasicAuth(username=self.username, password=self.password)



