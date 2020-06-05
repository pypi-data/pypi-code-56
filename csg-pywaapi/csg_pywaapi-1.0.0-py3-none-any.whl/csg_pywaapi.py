import sys
import os
sys.path.append('..')

from waapi import WaapiClient
from pprint import pprint
from csg_helpers import soundbank_helper
import operator

client = None

def connect(port=8095):
    """Initial call to wwise, returns the project info or False"""
    global client
    try:
        client = WaapiClient(url="ws://127.0.0.1:{0}/waapi".format(port))
    except Exception as ex:
        print("Connection error: {}".format(ex))
        print("Error connecting to Wwise. Please check your Waapi settings in User Preferences (wamp port expecting 8095) .....exiting")
        #input('Press <ENTER> to continue')
        return False
        #sys.exit()
    else:
        result = client.call("ak.wwise.core.getInfo")
        return result

def exit():
    """Exiting the connection"""
    try:
        client.disconnect()
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def getClient():
    return client

def call(procedure,arguments):
    """Support manually calling a procedure with args"""
    try:
        res = client.call(procedure,arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

############# Function definitions #########################################

### Project undo and save ######

def beginUndoGroup():
    try:
        client.call("ak.wwise.core.undo.beginGroup")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def cancelUndoGroup():
    try:
        client.call("ak.wwise.core.undo.cancelGroup")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def endUndoGroup(undogroup):
    """undogroup is the name of the group of actions"""
    undoArgs = {"displayName": undogroup}
    try:
        client.call("ak.wwise.core.undo.endGroup", undoArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def saveWwiseProject():
    try:
        client.call("ak.wwise.core.project.save")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def setupSubscription(subscription, target, returnArgs = ["id", "name", "path"]):
    """Subscribe to an event. Do target when triggered, get retunArgs in"""
    try:
        client.subscribe(subscription, target, {"return": returnArgs})
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def getProjectInfo():
    arguments = {
        "from": {"ofType": ["Project"]},
        "options": {
            "return": ["type","id", "name", "filePath","@DefaultLanguage"]
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get",arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res["return"][0]

def getLanguages():
    langlist=[]
    arguments = {
        "from": {"ofType": ["Language"]},
        "options": {
            "return": ["name"]
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        for lang in res.kwresults["return"]:
            if lang['name'] != 'SFX' and lang['name'] != 'External' and lang['name'] != 'Mixed':
                langlist.append(lang['name'])
        return langlist

def getPathToWwiseProjectFolder():
    """Gets a path to the root folder of wwise project"""
    projectInfo = getProjectInfo()
    WwiseProjectPath = projectInfo["filePath"]
    WwiseProjectPath = WwiseProjectPath.replace("Y:", "~").replace('\\', '/')
    pathToWwiseFolder = os.path.expanduser(os.path.dirname(WwiseProjectPath))
    return pathToWwiseFolder

###  Object creation and property setting ######


def createWwiseObject(parentID, otype="BlendContainer", oname="", conflict="merge"):
    """Create an object of type otype, called oname, underneath parentID"""
    createObjArgs = {
        "parent": parentID,
        "type": otype,
        "name": oname,
        "onNameConflict": conflict
    }
    try:
        res = client.call("ak.wwise.core.object.create", createObjArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def createWwiseObjectFromArgs(args = {}):
    """Create with custom args"""
    try:
        res = client.call("ak.wwise.core.object.create", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setProperty(object, property, value):
    """Set property to value for object"""
    setPropertyArgs = {
        "object": object,
        "property": property,
        "value": value
    }
    try:
        res = client.call("ak.wwise.core.object.setProperty",setPropertyArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setReference(object, reference, value):
    """Set reference to value for object"""
    setArgs = {
        "object": object,
        "reference": reference,
        "value": value
    }
    try:
        res = client.call("ak.wwise.core.object.setReference",setArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setNotes(object, value):
    """Set the notes of object to value"""
    setPropertyArgs = {
        "object": object,
        "value": value
    }
    try:
        res = client.call("ak.wwise.core.object.setNotes",setPropertyArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def importAudioFiles(args):
    """Import with custom args"""
    try:
        res = client.call("ak.wwise.core.audio.import", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def setupImportArgs(parentID, fileList,originalsPath,language="SFX"):
    """Construct args for import"""
    ParentID = str(parentID)
    importFilelist = []
    for audiofile in fileList:
        foo = audiofile.rsplit('.') #remove extension from filename
        audiofilename = foo[0]
        importFilelist.append(
            {
                "audioFile": audiofile,
                "objectPath": "<Sound SFX>"+os.path.basename(audiofilename)
            }
        )

    importArgs = {
        "importOperation": "useExisting",
        "autoAddToSourceControl": True,
        "default": {
            "importLanguage": language,
            "importLocation": ParentID,
            "originalsSubFolder": originalsPath
            },
        "imports": importFilelist
        }
    return importArgs


def deleteWwiseObject(object):
    args = {"object":object}
    try:
        client.call("ak.wwise.core.object.delete",args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

###  Searching the project  ######

def getSelectedObjects(properties=[]):
    """Get currently selected object, return any extra properties"""
    baseProperties = ["id","type", "name", "path"]
    selectedObjectArgs = {
        "options": {
            "return": baseProperties+properties
        }
    }
    try:
        res = client.call("ak.wwise.ui.getSelectedObjects",selectedObjectArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["objects"]
        else:
            return []

def getDescendantObjectsOfType(fromObject,ofType,returnProperties=[],tfrom="id",select="descendants"):
    """Perform a search fromObject to find descendants ofType. Optionally change the from and select parts of the query, by default use ID as the object"""
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [fromObject]},
        "transform": [
            {"select": [select]},
            {"where":["type:isIn",[ofType]]}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getDescendantObjects(fromObject,returnProperties=[],tfrom="id",select="descendants"):
    """start fromObject, return all descendants (or optionally something else), by default use ID as the object"""
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [fromObject]},
        "transform": [
            {"select": [select]}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []


def getObjectsByName(name,type,returnProperties=[],tfrom="name"):
    """Run a query to find by name. Need to include a type in the query"""
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [type+":"+name]},
        "transform": [],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getObjectProperties(fromObject,returnProperties=[],tfrom="id"):
    """get some additional properties fromObject, by default use ID as the object"""
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [fromObject]},
        "transform": [],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None and len(res["return"])>0:
            if len(res["return"]) > 1:
                return res["return"]
            else:
                return res["return"][0]
        else:
            return []

def getAllObjectsOfType(ofType,returnProperties=[]):
    """get all objects of a certain type"""
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {"ofType": [ofType]},
        "transform": [
            #{"select": "parent"}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getReferencesToObject(objectID,returnProperties=[],tfrom="id"):
    """ get the references to a given object, by default use ID as the object"""
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [objectID]},
        "transform": [
            {"select": ["referencesTo"]}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        if res != None:
            return res["return"]
        else:
            return []

def getListOfTypes():
    """return the list of valid object types, can help debugging"""
    try:
        res = client.call("ak.wwise.core.object.getTypes")
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def filterWwiseObjects(objects,property,operation, value):
    """helper function to filter a list of objects by a specific property, value and comparison operation"""
    # e.g. return only objects with "@Volume" , "<" , "-48"
    results = []
    op = getOperator(operation)
    for obj in objects:
        if not property in obj:## this object doesnt have the property, so skip it
            continue
        if op(obj[property],value):
            results.append(obj)
    return results

def getOperator(string):
    if string == "==":
        return operator.eq
    elif string == "<":
        return operator.lt
    elif string == "<=":
        return operator.le
    elif string == ">":
        return operator.gt
    elif string == ">=":
        return operator.ge
    elif string == "!=":
        return operator.ne


#####  Soundbanks #####
def generateSoundbanks(banklist = []):
    args = {
        "command": "GenerateSelectedSoundbanksAllPlatforms",
        "objects": [
            banklist
        ]
    }
    try:
        client.call("ak.wwise.ui.commands.execute", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False

def getSoundbanks(fromType,fromValue):
    """ Return all Soundbanks referencing any object of the Work Unit directly"""
    BankList =[]
    for transform in soundbank_helper.bankTransforms:
    #for transform in bankhelper.bankTransforms:
        arguments = {
            "from": {fromType: [fromValue]},
            "transform": transform,
            "options": {
                "return": ['id', 'name', 'type']
            }
        }
        try:
            res = client.call("ak.wwise.core.object.get", arguments)
        except Exception as ex:
            print("call error: {}".format(ex))
            return False
        else:
            # print (res.kwresults["return"])
            for bank in res["return"]:
                if bank["name"] not in BankList:
                    BankList.append((bank["name"]))
    return BankList


def executeCommand(command,objects = []):
    """wrapper to execute UI commands"""
    args = {
        "command": command,
        "objects": [
            objects
        ]
    }
    try:
        res = client.call("ak.wwise.ui.commands.execute", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def automationMode(enabled):
    """set automation mode on/off"""
    args = {
        "enable": enabled
    }
    try:
        res = client.call("ak.wwise.debug.enableAutomationMode", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def checkoutWorkUnit(workunitID):
    """Source control operation to check out work unit"""
    return executeCommand("WorkgroupCheckoutWWU",workunitID)

def cleanfilePathFromWwise(path):
    """Cleans the nonsense from Mac paths that Wwise gives you"""
    cleanMacpath = path.replace("Y:","~").replace('\\', '/')
    return os.path.abspath(os.path.expanduser(cleanMacpath))

def setSwitchContainerAssignment(switch,child):
    """Assign a given child object to a given switch (switch container)"""
    args = {
        "stateOrSwitch": switch,
        "child":child
    }
    try:
        res = client.call("ak.wwise.core.switchContainer.addAssignment", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def removeSwitchContainerAssignment(switch,child):
    """Remove a given child object from a given switch (switch container)"""
    args = {
        "stateOrSwitch": switch,
        "child":child
    }
    try:
        res = client.call("ak.wwise.core.switchContainer.removeAssignment", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def moveWwiseObject(object,parent, conflict="replace"):
    """move object to new location under parent"""
    args = {

        "object": object,
        "parent": parent,
        "onNameConflict": conflict
    }
    try:
        res = client.call("ak.wwise.core.object.move", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res

def copyWwiseObject(object, parent, conflict="replace"):
    """copy object to new location under parent"""
    args = {

        "object": object,
        "parent": parent,
        "onNameConflict": conflict
    }
    try:
        res = client.call("ak.wwise.core.object.copy", args)
    except Exception as ex:
        print("call error: {}".format(ex))
        return False
    else:
        return res
############## End of Function definitions ##############################################

#If pywaapi is run as the main script, connect and print result
if __name__ == "__main__":
    result = connect()
    pprint(result)
    exit()

