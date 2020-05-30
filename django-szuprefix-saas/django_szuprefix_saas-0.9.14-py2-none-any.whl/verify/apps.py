# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig

class Config(AppConfig):
    name = "django_szuprefix_saas.verify"
    label = "verify"
    verbose_name = "审核"

    def ready(self):
        super(Config, self).ready()
        from . import receivers
