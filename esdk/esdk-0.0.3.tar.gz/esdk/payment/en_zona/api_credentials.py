from dataclasses import dataclass
import base64


@dataclass(order=False)
class APICredentials:
    """
    transfermovil credentials class
    
    Attributes: 

   

    """
    
    consumer_key: str 
    consumer_secret: str
    
    def __encodecredentials__(self,credential : str = None) -> str:

        if not isinstance(credential,str) or len(credential) == 0:
            raise Exception("Encode credentials cannot be empty")
        
        credential_bytes = credential.encode('ascii')    
        encode64 = base64.b64encode(credential_bytes)
        encode64_string = str(encode64)
        return encode64_string[2:-1]

  
    def getheaders(self) -> dict:

        if not isinstance(self.consumer_key,str) or len(self.consumer_key) == 0:
            raise Exception("Incorrect Consumer Key")

        elif not isinstance(self.consumer_secret,str) or len(self.consumer_secret) == 0:
            raise Exception("Incorrect Consumer Secret")
        
        credentials = f"{self.consumer_key}:{self.consumer_secret}"
        
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Basic {self.__encodecredentials__(credentials)}",
                   }
        return headers
    


