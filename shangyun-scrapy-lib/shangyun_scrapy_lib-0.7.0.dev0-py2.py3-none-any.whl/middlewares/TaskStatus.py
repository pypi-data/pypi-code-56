from scrapy import Spider, Request
from scrapy.http import Response

from shangyun_scrapy_lib.constants import TaskStatus
from shangyun_scrapy_lib.utils.MongoUtils import requests_relate


class TaskStatusSpiderMiddleware(object):
    """
    给每个结果生成一个uuid，
    """

    def process_start_requests(self, start_requests, spider: Spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        # Must return only requests (not items).
        for r in start_requests:
            if isinstance(r, Request):
                r.meta["status"] = TaskStatus.not_run
                _update_status(r)
            yield r

    def process_spider_output(self, response: Response, result, spider: Spider):
        def set_status(res):
            if isinstance(res, Request):
                res.meta["status"] = TaskStatus.not_run
                _update_status(res)
            return res

        if response.request:
            r: Request = response.request
            r.meta["status"] = TaskStatus.success
            _update_status(r)

        return [set_status(res) for res in result or ()]


class TaskStatusDownloaderMiddleware(object):
    def process_request(self, request: Request, spider):
        request.meta["status"] = TaskStatus.running
        _update_status(request)
        return request


def _update_status(r: Request):
    _id = r.meta.get("id")
    if not _id:
        return
    requests_relate.col.update_one({"_meta.id": _id}, {"$set": {"_meta.status": r.meta.get("status")}})
