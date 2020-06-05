#! -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.html import smart_urlquote


class OssFileWidget(forms.URLInput):
    template_name = 'index.html'

    def __init__(self, attrs=None):
        final_attrs = {
            'domain': settings.OSS_PROXY_URL,
            'bucket': settings.OSS_BUCKET_NAME,
            'get_token_url': '{0}{1}'.format(settings.SERVER_URL, settings.OSS_TOKEN_ROUTE)
        }

        if attrs is not None:
            final_attrs.update(attrs)
        super(OssFileWidget, self).__init__(attrs=final_attrs)

    def get_context(self, name, value, attrs):
        context = super(OssFileWidget, self).get_context(name, value, attrs)
        context['current_label'] = '当前：'
        context['widget']['href'] = smart_urlquote(context['widget']['value']) if value else ''
        return context
