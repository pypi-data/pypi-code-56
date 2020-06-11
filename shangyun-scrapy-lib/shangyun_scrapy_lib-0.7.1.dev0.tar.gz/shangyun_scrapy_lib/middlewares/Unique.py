import time

import scrapy
from scrapy import Spider, Request
from scrapy.http import Response


class UniqueSpiderMiddleware(object):
    """
    给每个结果生成一个uuid，
    """
    def process_start_requests(self, start_requests, spider: Spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        # Must return only requests (not items).
        for r in start_requests:
            name = spider.name
            if isinstance(r, Request):
                if name not in r.meta.get("id", ""):
                    crawl_id = getattr(spider, "crawl_task_id")(r)
                    r.meta["id"] = "{}-{}".format(name, crawl_id)
            yield r

    def process_spider_input(self, response: Response, spider: Spider):

        pass

    def process_spider_output(self, response: Response, result, spider: Spider):
        def ensure_uuid(res):
            name = spider.name
            if isinstance(res, dict) or isinstance(res, scrapy.Item):
                _type, _id = res.get("type"), res.get("id")
                # 如果name在id中，则说明已经添加过了，直接返回
                if not _id or name in _id:
                    return res

                if _type == "news":
                    res["id"] = "news-{}-{}".format(name, _id)
                elif _type == "comment":
                    res["id"] = "comment-{}-{}".format(name, _id)
                elif _type == "trend":
                    res["id"] = "trend-{}-{}-{}".format(name, res['news_id'] or res['comment_id'], int(time.time()))

            elif isinstance(res, Request):
                if name not in res.meta.get("id", ""):
                    crawl_id = getattr(spider, "crawl_task_id")(res)
                    res.meta["id"] = "{}-{}-{}".format(name, crawl_id, res.meta.get("update", 0))
            return res


        return [ensure_uuid(res) for res in result or ()]
