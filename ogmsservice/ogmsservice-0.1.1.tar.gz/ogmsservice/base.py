#Data : 2020-5-30
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Provide base service for all related service to inherit


from .utils import HttpHelper

class Service:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
    def getBaseURL(self):
        return "http://" + self.ip + ":" + str(self.port) + "/"

    def connect(self):
        strData = HttpHelper.Request_get_str_sync(self.ip, self.port, "/ping")
        if strData == "OK":
            return True
        else:
            return False
