from datetime import datetime
from gbapi.api.stats import Stats
from gbapi.api.structured_data import StructuredData
from .sub.wip import FinishedWork

class WiP(StructuredData):
	def __init__(self, stats, sdata, ainfo, attr):
		super(WiP, self).__init__(sdata)
		
		self.info = ainfo['_aCellValues']
		self.dev_state = self.state = self.info['_sDevelopmentState']
		self.completion = self.progress = self.info['_iCompletionProgress']
		self.is_private = self.info['_sbIsPrivate']
		self.finished_work = FinishedWork(self.info['_aFinishedWork'])
		self.added = datetime.utcfromtimestamp(self.info['_tsDateAdded'])
		
		self.attr = attr['_aCellValues']['_aAttributes']
		self.stats = Stats(stats)