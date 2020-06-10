import os

from pymongo import MongoClient


class MongoUtils:
    def __init__(self, db: str, col: str):
        self.mongo = MongoClient(
            host=os.environ.get('CRAWLAB_MONGO_HOST') or 'localhost',
            port=int(os.environ.get('CRAWLAB_MONGO_PORT') or 27017),
            username=os.environ.get('CRAWLAB_MONGO_USERNAME'),
            password=os.environ.get('CRAWLAB_MONGO_PASSWORD'),
            authSource=os.environ.get('CRAWLAB_MONGO_AUTHSOURCE') or 'admin'
        )
        self.db = self.mongo[db]
        self.col = self.mongo[db][col]
        self.index_list = []

    def create_index(self, name: str) -> bool:
        res = self.col.create_index([(name, 1)], name=name, unique=True)
        self.index_list = [index['name'] for index in self.col.list_indexes()]
        return res

    def exist_index(self, name):
        if len(self.index_list) == 0:
            self.index_list = [index['name'] for index in self.col.list_indexes()]

        return name in self.index_list


def ensure_index():
    name = "id"
    if not news_result.exist_index(name):
        news_result.create_index(name)
    if not comment_result.exist_index(name):
        comment_result.create_index(name)
    if not trend_result.exist_index(name):
        trend_result.create_index(name)

    if not requests_relate.exist_index("_meta.id"):
        requests_relate.create_index("_meta.id")



db_name = os.environ.get('CRAWLAB_MONGO_DB') or 'crawlab_test'
col_name = os.environ.get('ERROR_LOGGER_COLLECTION') or 'error'
task_error = MongoUtils(db_name, col_name)

# 关键任务的存储
col_name = os.environ.get('TASK_RELATE_COLLECTION') or 'requests'
requests_relate = MongoUtils(db_name, col_name)

# 任务执行的统计
col_name = os.environ.get('STATISTIC_COLLECTION') or 'statistic'
requests_statistic = MongoUtils(db_name, col_name)

# 存储新闻
col_name = os.environ.get('CRAWLAB_COLLECTION') or 'news'
news_result = MongoUtils(db_name, col_name)

# 存储评论
col_name = os.environ.get('CRAWLAB_COLLECTION') or 'comments'
comment_result = MongoUtils(db_name, col_name)

# 存储趋势
col_name = os.environ.get('CRAWLAB_COLLECTION') or 'trend'
trend_result = MongoUtils(db_name, col_name)


# 确保每个数据存储的collection都有索引
ensure_index()

__all__ = [task_error, requests_relate, requests_statistic,
           news_result, comment_result, trend_result, MongoUtils]

if __name__ == '__main__':
    # print(task_statistic.col.insert({"test": 123}))
    pass
