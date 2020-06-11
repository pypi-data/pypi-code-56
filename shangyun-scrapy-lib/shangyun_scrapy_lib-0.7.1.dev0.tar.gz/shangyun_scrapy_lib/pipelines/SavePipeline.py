import os

from shangyun_scrapy_lib.BaseItems.base_item import BaseItem
from shangyun_scrapy_lib.constants import DataType
from shangyun_scrapy_lib.utils.MongoUtils import trend_result, comment_result, news_result


class NewsSpiderPipeline(object):
    def __init__(self):
        self.trend_col = trend_result.col
        self.comment_col = comment_result.col
        self.news_col = news_result.col
        self.task_id = os.environ.get('CRAWLAB_TASK_ID')

        self.type2col = {
            DataType.NEWS: self.news_col,
            DataType.COMMENT: self.comment_col,
            DataType.TREND: self.trend_col
        }

    def process_item(self, item: BaseItem, spider):
        item['task_id'] = self.task_id
        col = self.type2col[item["data_type"]]
        if item.get("id", False):
            col.find_one_and_update({"id": item["id"]},
                                    {"$set": item},
                                    upsert=True)
        else:
            col.save(item)
        print("测试2测试2-------------------------------------")
        print(item, col)
        print("测试2测试2-------------------------------------")
        return item
