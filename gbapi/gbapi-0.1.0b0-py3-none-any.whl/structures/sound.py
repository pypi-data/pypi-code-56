from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData

class Sound(StructuredData):
	def __init__(self, stats, sdata, attr):
		super(Sound, self).__init__(sdata)
		self.stats = Stats(stats)
		self.attr = attr['_aCellValues']['_aAttributes']