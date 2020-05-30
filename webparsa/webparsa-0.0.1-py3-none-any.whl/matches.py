
from .dicttools import deepGet, deepIterate, destructureDict
from .functions import runFunction
from . import thread_locals
import re

def findMatches(nextStructure, content):
    name = nextStructure.name
    if name.startswith("p_"):
        name = name[2:]

    parsaDataD = {attr: nextStructure.attrs[attr] for attr in nextStructure.attrs if attr.startswith("parsa.")}
    parsaData = destructureDict(parsaDataD).get("parsa", {})
    filters = parsaData.get("filters", {})
    attributes = {attr: nextStructure.attrs[attr] for attr in nextStructure.attrs if not attr.startswith("parsa.")}

    if name == "any":
        name = None

    matches = content.findAll(name=name, attrs=attributes, recursive='recursive' in parsaData)

    return runFilters(matches, filters)

def getAttributes(match):
    return {"text": match.text, "element": match, "attrs": match.attrs}

def runFilters(matches, filters):
    printFailures = True # thread_locals.verbose
    i = 0
    filtered = []
    for match in matches:
        attributes = getAttributes(match)
        attributes['index'] = i

        passed = True

        regex_attrs = filters.get('regex', {})
        for path, regex in deepIterate(regex_attrs):
            if not re.match(regex, deepGet(attributes, path)):
                passed = False
                if printFailures:
                    print("Failed on regex")
                break

        if 'function' in filters:
            if not runFunction(filters['function'], attributes):
                passed = False
                if printFailures:
                    print("Failed on function. Attributes:", attributes['index'])

        # INDEX
        elif 'index' in filters:
            index = int(filters['index'])

            # The index must match
            if i != index:
                passed = False
                if printFailures:
                    print("Failed on index")

        if passed:
            filtered.append(match)

        i += 1
    
    return filtered