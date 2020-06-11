import traceback

from scrapy import Request
from scrapy.http import Response
from shangyun_scrapy_lib.constants import TaskStatus
from shangyun_scrapy_lib.utils.MongoUtils import task_error, requests_relate
from shangyun_scrapy_lib.utils.Serialize import request_serialize


class TaskErrorSpiderMiddleware(object):
    def process_spider_exception(self, response: Response, exception, spider):
        error_info = {
            "error": traceback.format_exc(),
            "request": request_serialize(response.request),
            "type": "spider"
        }
        task_error.col.save(error_info)
        # 通过id更新task状态r
        if response.request:
            r: Request = response.request
            r.meta["status"] = TaskStatus.parse_error
            _update_status(r)


class TaskErrorDownloaderMiddleware(object):
    def process_exception(self, request: Request, exception: Exception, spider):
        # 保存错误信息
        error_info = {
            "error": traceback.format_exc(),
            "request": request_serialize(request),
            "type": "download"
        }
        task_error.col.save(error_info)
        # 更新task状态
        request.meta["status"] = TaskStatus.download_error
        _update_status(request)


def _update_status(r: Request):
    _id = r.meta.get("id")
    if not _id:
        return
    requests_relate.col.update_one({"_meta.id": _id}, {"$set": {"_meta.status": r.meta.get("status")}})
