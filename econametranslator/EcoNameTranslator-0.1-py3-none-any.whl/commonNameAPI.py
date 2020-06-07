import requests
from higherLevelAPI import *
import itertools
from dataCleaning import *
from dataCleaning import *
from taxonomyAPI import *

def commonNameAPI(bestEffortTuple):
    name, speciesResult = bestEffortTuple
    if len(speciesResult) > 0: return (name,True,speciesResult)
    return commonNameReq(name)

def commonNameReq(name):
    try:
        res = requests.get("https://www.itis.gov/ITISWebService/jsonservice/searchByCommonName?srchKey="+name).json()
        commonNames = res['commonNames']
        if commonNames is None: return (name,False,[])
        if len(name.split(" ")) == 1: commonNames = list(filter(lambda x: checkIfCommonNameResultIsValid(name,x['commonName']),commonNames))
        commonNames = list(map(lambda x: (x['commonName'],x['tsn']) , commonNames))
        commonNames = list(map(tranlsateUidToSpeciesName,commonNames))
        return (name,True,list(set(map(cleanSingleSpeciesString,itertools.chain(*commonNames)))))
    except Exception as e:
        return (name,False,[])

def tranlsateUidToSpeciesName(dataTuple):
    commonName,uId = dataTuple
    res = requests.get("https://www.itis.gov/ITISWebService/jsonservice/getFullRecordFromTSN?tsn="+str(uId)).json()['scientificName']['combinedName']
    if len(res.strip().split(" ")) < 2: 
        return higherLevelAPI((commonName,('family',res)))[2]
    else:
        return [res]

def checkIfCommonNameResultIsValid(name,result):
    result = result.lower().split(" ")
    stringPotential1 = name 
    stringPotential2 = name+'s' #plurals
    return stringPotential1 in result or stringPotential2 in result
