from datetime import datetime

from scrapy import Spider, Request
from scrapy.http import Response

from shangyun_scrapy_lib.utils.MongoUtils import requests_relate
from shangyun_scrapy_lib.utils.Serialize import request_serialize
import logging

logger = logging.getLogger(__name__)


class TaskRelateSpiderMiddleware(object):
    """
    判断下mongo中有没有创建唯一索引，防止数据重复
    """

    def process_start_requests(self, start_requests, spider: Spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        # Must return only requests (not items).
        for r in start_requests:
            # 将种子链接也保存到mongo中
            if isinstance(r, Request):
                r.meta["insert_time"] = datetime.now()# .strftime("%Y-%M-%d %h:%m:%s")
                requests_relate.col.find_one_and_update(
                    {"_meta.id": r.meta.get("id")},
                    {"$set": request_serialize(r)},
                    upsert=True
                )
            yield r

    def process_spider_output(self, response: Response, result, spider: Spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        # Must return an iterable of Request, dict or Item objects.

        parent_request: Request = response.request
        parent_id = parent_request.meta.get("id", False)
        if not parent_id:
            logger.warning("the parent request has not id")

        for r in result:
            if isinstance(r, Request):
                r.meta["parent_id"] = parent_id or ""
                r.meta["insert_time"] = datetime.now() #.strftime("%Y-%M-%d %h:%m:%s")
                requests_relate.col.find_one_and_update(
                    {"_meta.id": r.meta.get("id")},
                    {"$set": request_serialize(r)},
                    upsert=True
                )
            yield r
