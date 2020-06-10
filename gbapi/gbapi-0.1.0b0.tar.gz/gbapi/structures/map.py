from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData

class Map(StructuredData):
	def __init__(self, stats, sdata, ainfo):
		super(Map, self).__init__(sdata)
		
		"""
		{
			"_aAdditionalViewVariables": [],
			"_sViewTemplate": "?>\n<dl>\n<dt>Version<\/dt>\n<dd class=\"Version\">\n<? if (!empty($d[\"_sVersion\"])): ?>\n<?= $d[\"_sVersion\"] ?>\n<? else: ?>\nUnknown\n<? endif ?>\n<\/dd>\n<\/dl>\n<?",
			"_aCellValues": {
				"_sVersion": ""
			}
		}
		"""
		
		self.info = ainfo['_aCellValues']
		self.version = self.info['_sVersion']
		self.stats = Stats(stats)