from bs4 import BeautifulSoup
import re, json
import requests

from .functions import runFunction
from .matches import findMatches
from .messages import NOT_FOUND, MATCH_FAILED
from .nodes import nodeChildren, firstChild
from . import thread_locals

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

def nodeParser(fn):
    def wrapper(self, structure, content, currentData):
        if not structure.has_attr("name"):
            raise ValueError(f"<{structure.name}> structure must have a name.")
        else:
            name = structure.attrs['name']

        value = fn(self, structure, content, currentData)

        if structure.has_attr("after"):
            post_functions = structure.attrs['after']
            for function in post_functions.split("+"):
                value = runFunction(function.strip(), value)

        # if it's VALUE_CONTENT, it doesn't have a name, it's the value itself
        if name == "VALUE_CONTENT":
            return value
        else:
            return {**currentData, name: value}

    return wrapper

class Webparsa:
    def __init__(self, mapping, **functions):
        thread_locals.parsa_functions = functions
        self.mapping = BeautifulSoup(mapping, "lxml")

    def getValue(self, value, content):
        if value.startswith("self.attrs."):
            attr = value[11:]
            value = content.attrs.get(attr, "")
        elif value == "self.text":
            value = content.text

        return value

    def getList(self, nextNextStructure, possibleElements):
        values = []
        for possibleElement in possibleElements:
            newValue = self._parse(nextNextStructure, possibleElement)
            if newValue != NOT_FOUND:
                values.append(newValue)
        return values

    @nodeParser
    def parseList(self, structure, content, currentData):
        child = firstChild(structure) # LIST ELEMENTS CAN ONLY HAVE ONE CHILD

        return self.getList(child, findMatches(child, content))

    @nodeParser
    def parseDict(self, structure, content, currentData):
        return self._parse(structure, content)

    @nodeParser
    def parseValue(self, structure, content, currentData):
        return self.getValue(structure.text, content)

    def _parse(self, parent: BeautifulSoup, content: BeautifulSoup):
        data = {}
        for structure in parent.children:
            if structure.name is None:
                continue

            if structure.name == "list":
                data = self.parseList(structure, content, data)

            elif structure.name == "dict":
                data = self.parseDict(structure, content, data)

            elif structure.name == "unrequired":
                value = self._parse(structure, content)
                if value != NOT_FOUND:
                    data.update(value)

            elif structure.name == "value":
                data = self.parseValue(structure, content, data)

            else:
                foundItems = findMatches(structure, content)
                foundSomething = False

                for found in foundItems:
                    value = self._parse(structure, found)
                    if value is not NOT_FOUND:
                        data.update(value)
                        break
                else:
                    return NOT_FOUND
                    
        return data

    def parseText(self, text):
        content = BeautifulSoup(text, "html.parser")

        return self._parse(self.mapping, content)

    def parseURL(self, url, headers=headers):
        text = requests.get(url, headers=headers).text

        return self.parseText(text)
