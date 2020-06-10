from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData

class Script(StructuredData):
	def __init__(self, stats, sdata):
		super(Script, self).__init__(sdata)
		self.stats = Stats(stats)