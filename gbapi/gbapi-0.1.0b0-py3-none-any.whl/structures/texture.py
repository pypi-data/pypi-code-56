from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData

class Texture(StructuredData):
	def __init__(self, stats, sdata, attr):
		super(Texture, self).__init__(sdata)
		self.stats = Stats(stats)
		self.attr = attr['_aCellValues']['_aAttributes']