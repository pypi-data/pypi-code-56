from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData

class Tool(StructuredData):
	def __init__(self, stats, sdata, ainfo, attr):
		super(Tool, self).__init__(sdata)
		
		self.info = ainfo['_aCellValues']
		self.download = self.info['_sDownloadUrl']
		self.homepage = self.info['_sHomepageUrl']
		
		self.stats = Stats(stats)
		self.attr = attr['_aCellValues']['_aAttributes']