import requests 

def taxonomyAPI(names):
    politeness = 50
    responses = []
    excepted = []
    for i in range(0,len(names),politeness):
        print(f"Processing Records {str(i)} to {str(min(i+politeness,len(names)))} [of {len(names)}]")
        apiInputWithCapitalisedGenus = list(map(lambda x: x.capitalize(),names[i:i+politeness]))
        succeeded,failed = callTaxaAPI(apiInputWithCapitalisedGenus)
        responses.extend(succeeded)
        excepted.extend(failed)

    speciesResponses = list(map(processSingleResponse,responses))
    return speciesResponses,excepted

def processSingleResponse(response):
    if response['is_known_name']: return (response['supplied_name_string'].lower(), True, parseSingleTaxonomyFromAPI(response))
    elif 'results' in response: return (response['supplied_name_string'].lower(),False, parseSingleTaxonomyFromAPI(response))
    return (response['supplied_name_string'], False, ('',''))

def parseSingleTaxonomyFromAPI(taxonomicAPIres):
    dataFromMultipleSources = taxonomicAPIres['results']
    dataFromMultipleSources = list(map(extractTaxaData,dataFromMultipleSources))
    for item in ['species','genus','subfamily','family']:
        for taxaMap in dataFromMultipleSources:
            if (item in taxaMap) and (taxaMap[item].strip() != ''): 
                return (item,taxaMap[item].strip())
    return ('','')
    
def extractTaxaData(singleTaxaSource):
    mappingDict = {}
    try: mappingDict = dict(zip(singleTaxaSource['classification_path_ranks'].lower().split("|"),\
                                singleTaxaSource['classification_path'].lower().split("|")))
    except: pass
    return mappingDict

def callTaxaAPI(rawNames):
    excepted = []
    preparedAPILoad = prepareTaxaAPIinput(rawNames) #try a bulk-call
    success,result = makeCall(preparedAPILoad) 
    if (not success) or (len(result) != len(rawNames)):
        namesSucceeded = list(filter(lambda resp: 'supplied_string_name' in resp, result))
        namesSucceeded = list(map(lambda resp: resp['supplied_string_name'], namesSucceeded))
        failedNames = list(set(rawNames) - set(namesSucceeded))
        succeededResults, failedNames = individuallyMakeRequests(failedNames)
        result.extend(succeededResults)
        excepted.extend(failedNames)
    
    return result, excepted

def prepareTaxaAPIinput(names):
    namesToSend = "|".join(names)
    return namesToSend
    
def individuallyMakeRequests(names):
    succeededResults = []
    failedNames = []
    for name in names:
        success,result = makeCall(name)
        if success: succeededResults.extend(result)
        else: failedNames.extend(name)
    
    return succeededResults, failedNames

def makeCall(preparedAPILoad):
    try:
        apiResult = requests.get(f'http://resolver.globalnames.org/name_resolvers.json?names={preparedAPILoad}').json()['data']
        return (True,apiResult)
    except Exception as e: 
        return (False,[])
