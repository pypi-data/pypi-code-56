#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:Ruci
# datetime:2020/6/5 15:11
# software: PyCharm

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^login/$',views.login,name='login'),
    url(r'^registered/$',views.registered,name='registered'),
    url(r'^yzm/$',views.request_yzm,name='yzm')

]