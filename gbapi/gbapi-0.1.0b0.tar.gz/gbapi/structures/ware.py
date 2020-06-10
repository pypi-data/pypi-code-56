from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData

class Ware(StructuredData):
	def __init__(self, stats, sdata, ainfo):
		super(Tool, self).__init__(sdata)
		
		self.info = ainfo['_aCellValues']
		self.ware_type = self.info['_sType']
		
		self.stats = Stats(stats)