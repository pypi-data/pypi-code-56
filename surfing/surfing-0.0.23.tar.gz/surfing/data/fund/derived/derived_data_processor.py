
from typing import List

from .fund_score_processor import FundScoreProcessor
from .fund_indicator_processor import FundIndicatorProcessor
from .derived_index_val import IndexValProcess
from .style_analysis_processor import StyleAnalysisProcessor


class DerivedDataProcessor(object):
    def __init__(self):
        self.fund_indicator_processor = FundIndicatorProcessor()
        self.fund_score_processor = FundScoreProcessor()
        self.index_val_processor = IndexValProcess()
        self.style_analysis_processor: List[StyleAnalysisProcessor] = []
        self.updated_count = {}

    def process_all(self, start_date, end_date):
        failed_tasks = []

        failed_tasks.extend(self.fund_indicator_processor.process(start_date, end_date))
        failed_tasks.extend(self.fund_score_processor.process(start_date, end_date))
        failed_tasks.extend(self.index_val_processor.process(start_date, end_date))
        # 暂时只算这三个universe
        for universe in ('hs300', 'csi800', 'all'):
            sap = StyleAnalysisProcessor(universe)
            self.style_analysis_processor.append(sap)
            failed_tasks.extend(sap.process(start_date, end_date))

        for key, value in self.fund_indicator_processor.updated_count.items():
            if key not in self.updated_count:
                self.updated_count[key] = value
            else:
                self.updated_count[key] += value

        for key, value in self.fund_score_processor.updated_count.items():
            if key not in self.updated_count:
                self.updated_count[key] = value
            else:
                self.updated_count[key] += value

        for key, value in self.index_val_processor.updated_count.items():
            if key not in self.updated_count:
                self.updated_count[key] = value
            else:
                self.updated_count[key] += value

        for one in self.style_analysis_processor:
            for key, value in one._updated_count.items():
                if key not in self.updated_count:
                    self.updated_count[key] = value
                else:
                    self.updated_count[key] += value
        return failed_tasks


if __name__ == '__main__':
    ddp = DerivedDataProcessor()
    # start_date = '20200430'
    start_date = '20200506'
    end_date = '20200506'
    ddp.fund_score_processor.process(start_date, end_date)
