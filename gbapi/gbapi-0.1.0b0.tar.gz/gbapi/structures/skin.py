from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData

class Skin(StructuredData):
	def __init__(self, stats, sdata, attr):
		super(Skin, self).__init__(sdata)
		
		"""
		{
			"_aAdditionalViewVariables": [],
			"_sViewTemplate": "?>\n<dl>\n<? foreach ($d[\"_aAttributes\"] as $_sAttributeGroupTitle => $_aAttributes): ?>\n<dt><?= $_sAttributeGroupTitle ?><\/dt>\n<dd>\n<? if (count($_aAttributes) > 1): ?>\n<ul>\n<? foreach ($_aAttributes as $_sAttribute): ?>\n<li>\n<a href=\"\/search?query=<?= urlencode($_sAttributeGroupTitle.\" \".$_sAttribute) ?>&section=Skin<?= ($d[\"_aGame\"][\"_sAbbreviation\"]?\"&game=\".$d[\"_aGame\"][\"_sAbbreviation\"]:\"\") ?>\">\n<?= $_sAttribute ?>\n<\/a>\n<\/li>\n<? endforeach ?>\n<\/ul>\n<? else: ?>\n<a href=\"\/search?query=<?= urlencode($_sAttributeGroupTitle.\" \".$_aAttributes[0]) ?>&section=Skin<?= ($d[\"_aGame\"][\"_sAbbreviation\"]?\"&game=\".$d[\"_aGame\"][\"_sAbbreviation\"]:\"\") ?>\">\n<?= $_aAttributes[0] ?>\n<\/a>\n<? endif ?>\n<\/dd>\n<? endforeach ?>\n<\/dl>\n<?",
			"_aCellValues": {
				"_aGame": {
					"_sAbbreviation": "HL",
					"_sName": "Half-Life",
					"_sProfileUrl": "https:\/\/gamebanana.com\/games\/34",
					"_sIconUrl": "https:\/\/icons.gamebanana.com\/img\/ico\/games\/half-life.png",
					"_sBannerUrl": "https:\/\/banners.gamebanana.com\/img\/banners\/games\/5949aa4827119.jpg"
				},
				"_aAttributes": {
					"Development State": [
						"Final"
					],
					"Aesthetic": [
						"Default"
					]
				}
			}
		}
		"""
		
		self.attr = attr['_aCellValues']['_aAttributes']
		self.stats = Stats(stats)