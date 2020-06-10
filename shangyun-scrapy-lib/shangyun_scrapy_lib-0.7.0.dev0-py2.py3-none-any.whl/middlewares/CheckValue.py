# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy
from scrapy import Spider, Request

from shangyun_scrapy_lib.constants import DataType


class CheckValueSpiderMiddleware(object):
    # def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        # print("SpiderMiddleware-process_spider_input")
        # Should return None or raise an exception.
        # return None

    def process_spider_output(self, response, result, spider: Spider):
        def _filter(res):
            if isinstance(res, scrapy.Item) or isinstance(res, dict):
                res.update({"name": spider.name})
                return res.get("data_type", False) in [DataType.NEWS, DataType.TREND, DataType.COMMENT]
            elif isinstance(res, Request):
                res.meta.update({"name": spider.name})
                return True
            return True
        return (r for r in result or () if _filter(r))

    # def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        # print("SpiderMiddleware-process_start_requests")
        # Must return only requests (not items).
        # for r in start_requests:
        #     yield r

    # def spider_opened(self, spider):
    #     spider.logger.info('Spider opened: %s' % spider.name)



class CheckValueDownloaderMiddleware(object):

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
