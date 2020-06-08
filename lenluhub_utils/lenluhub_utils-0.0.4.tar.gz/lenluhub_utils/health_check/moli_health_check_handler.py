#!/usr/bin/python
#coding:utf-8

"""
@author: yangst2
@contact: yangst2@lenovo.com
@software: PyCharm
@file: moli_health_check.py
@time: 2020/6/4 14:50
"""


import tornado.web
from tornado.web import Application
from lenluhub_utils.health_check.moli_health_check import HealthCheck
from tornado import httputil
from typing import Any


class HealthCheckHandler(tornado.web.RequestHandler):

    def __init__(self, application: Application, request: httputil.HTTPServerRequest, **kwargs: Any):
        super().__init__(application, request, **kwargs)
        self.health_checker = HealthCheck(**kwargs)

    def get(self, *args, **kwargs):
        message, status_code, headers = self.health_checker.run(*args, **kwargs)
        self.set_status(status_code)
        self.write(message)

    def post(self, *args, **kwargs):
        message, status_code, headers = self.health_checker.run(*args, **kwargs)
        self.set_status(status_code)
        self.write(message)
