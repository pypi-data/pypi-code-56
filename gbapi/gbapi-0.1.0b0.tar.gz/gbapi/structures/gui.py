from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData

class GUI(StructuredData):
	def __init__(self, stats, sdata, attr):
		super(GUI, self).__init__(sdata)
		self.attr = attr['_aCellValues']['_aAttributes']
		self.stats = Stats(stats)