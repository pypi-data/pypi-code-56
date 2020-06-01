from .hvac import LutronObjectHVAC
from .output import LutronObjectOUTPUT


class ObjectCollection(object):
    def __init__(self, gw, readOnly=False):
        assert gw.__class__.__name__=='Lutron'
        self._gw=gw
        self._readOnly=False
        self._objects=[]
        self._objectsByIntegrationId={}
        self._indexManager=0

    @property
    def gw(self):
        return self._gw

    @property
    def logger(self):
        return self.gw.logger

    def len(self):
        return len(self._objects)

    def isReadOnly(self):
        if self._readOnly or self.gw.isReadOnly():
            return True
        return False

    def _validateIntegrationId(self, integrationId):
        try:
            if integrationId is not None:
                iid=int(integrationId)
                if iid>0:
                    return iid
        except:
            pass

    def get(self, integrationId, create=False):
        try:
            integrationId=self._validateIntegrationId(integrationId)
            return self._objectsByIntegrationId[integrationId]
        except:
            if create:
                return self._factory(integrationId)

    def _createObject(self, integrationId):
        """Should by overriden"""
        return None

    def _factory(self, integrationId):
        integrationId=self._validateIntegrationId(integrationId)
        if integrationId:
            obj=self.get(integrationId)
            if obj is None:
                obj=self._createObject(integrationId)
                self._objects.append(obj)
                self._objectsByIntegrationId[integrationId]=obj
            return obj
        pass

    def create(self, integrationId):
        return self.get(integrationId, True)

    def manager(self):
        if self.gw.isOpen():
            if self._objects:
                count=32
                while count>0:
                    count-=1
                    try:
                        item=self._objects[self._indexManager]
                        self._indexManager+=1
                    except:
                        self._indexManager=0
                        break
                    try:
                        item.manager()
                    except:
                        self.logger.exception('item manager')

    def refresh(self):
        for item in self._objects:
            item.refresh()

    def __getitem__(self, key):
        return self.get(key, create=True)

    def search(self, pattern):
        items=[]
        for item in self._objects:
            if item.match(pattern):
                items.append(item)
        return items

    def dump(self, matching=None):
        if matching:
            items=self.search(matching)
        else:
            items=self._objects
        for item in items:
            print(item)


class LutronObjectCollectionHVAC(ObjectCollection):
    def _createObject(self, integrationId):
        return LutronObjectHVAC(self, integrationId)


class LutronObjectCollectionOUTPUT(ObjectCollection):
    def _createObject(self, integrationId):
        return LutronObjectOUTPUT(self, integrationId)
