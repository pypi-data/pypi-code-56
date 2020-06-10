from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData

class Gamefile(StructuredData):
	def __init__(self, stats, sdata):
		super(Gamefile, self).__init__(sdata)
		self.stats = Stats(stats)