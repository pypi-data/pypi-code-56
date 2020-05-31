#Data : 2020-5-30
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Provide data services

import urllib3

from .utils import HttpHelper
from .utils import CommonMethod
from .base import Service

class Data(Service):
    def __init__(self, id, tag, type, size, value, datetime, ip, port):
        Service.__init__(self, ip, port)
        self.id = id
        self.tag = tag
        self.type = type
        self.size = size
        self.value = value
        self.datetime = datetime

    def isExist(self):
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/geodata/json/" + self.id)
        if CommonMethod.getJsonValue(jsData, "result") == "suc" :
            if CommonMethod.getJsonValue(jsData, "data") == "":
                return False
            return True
        return False

    def save(self, filepath):
        http = urllib3.PoolManager()
        response = http.request('GET', self.getBaseURL() + "geodata/" + self.id)
        with open(filepath, 'wb') as f:
            f.write(response.data)
        return 1

class DataConfigrationItem:
    def __init__(self, stateid, statename, eventname, dataid, destoryed = False, requested = False, optional = False):
        self.stateid = stateid
        self.statename = statename
        self.eventname = eventname
        self.dataid = dataid
        self.destoryed = destoryed
        self.requested = requested
        self.optional = optional

    @staticmethod
    def MakeUpDataItem(jsData):
        dat = DataConfigrationItem(jsData["StateId"], jsData["StateName"], jsData["Event"], jsData["DataId"], bool(jsData["Destroyed"]))
        return dat