# __init__.py
# Copyright HanzHaxors 2020
# Copyright Seth A. Robinson 2013

import json as JSON

class ArgumentError(Exception):
	""""""

class Data:
	"""
	Proton SDK Data
	Example:
	"action|move\\n\\rX|32\\n\\rY|34"
	
	TODO:
	fix 2D Array bug ("Vector2|2|4\\n\\r")
	"""
	def __init__(self, data: str = ""):
		self.__dictData = dict()
		self.__serialized = str()
		self.__keysd = list()
		self.__valuesd = list()
		
		if data != "":
			self.__dictData = self.toDict(data)
	
	def __refresh__(self):
		self.__serialized = str()
		self.__keysd = list()
		self.__valuesd = list()
	
	def toDict(self, data: str = ""):
		self.__refresh__()
		if data == "" and self.__dictData != dict():
			return self.__dictData
		elif data != "":
			linesOfData = data.split("\n\r")
			newDict = dict()
			for line in linesOfData:
				self.__keysd.append(line.split("|")[0])
				self.__valuesd.append(line.split("|")[1])
			for key in self.__keysd:
				try:
					newDict[key] = int(self.__valuesd[self.__keysd.index(key)])
				except:
					newDict[key] = self.__valuesd[self.__keysd.index(key)]
			return newDict
	
	def serialize(self):
		self.__serialized = str()
		for key in self.__dictData:
			self.__serialized += key+"|"+str(self.__dictData[key])+"\n\r"
		self.__serialized = self.__serialized[:-2]
		return self.__serialized
	
	def set(self, key, data):
		if key == None or data == None:
			raise ArgumentError("key and/or data parameter required")
		
		self.__dictData[key] = data
	
	def get(self, key):
		if key == None:
			raise ArgumentError("key parameter required")
		return self.__dictData[key]
	
	def unset(self, key):
		if key == None:
			raise ArgumentError("key parameter required")
		del self.__dictData[key]
	
	def loads(self, data: str = "", *splitter, json=False):
		if json:
			self.__dictData = JSON.loads(data)
		else:
			self.__dictData = self.toDict(data)

class Vector2:
	"""
	TODO
	"""
	def __init__(self, x: float = 0.0, y: float = 0.0):
		self.x = x
		self.X = x
		self.y = y
		self.Y = y
	
	def __setattr__(self, name, value):
		pass # TODO: Override __setattr__ in Vector2 class for changing the player too