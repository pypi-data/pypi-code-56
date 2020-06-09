# -*- coding: utf-8 -*-
from collective.volto.socialsettings.interfaces import ISocialSettings
from plone import api
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class SocialLinksGet(Service):
    def __init__(self, context, request):
        super(SocialLinksGet, self).__init__(context, request)

    def reply(self):
        records = api.portal.get_registry_record(
            "social_links", interface=ISocialSettings
        )
        result = []
        for record in records:
            values = record.split("|")
            if len(values) == 3:
                result.append(
                    {"title": values[0], "icon": values[1], "url": values[2]}
                )
        return result
