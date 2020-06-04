# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.easyform.interfaces import IAction
from collective.easyform.interfaces import ISaveData
from plone.autoform import directives

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from collective.easyformplugin.poll import _


class ICollectiveEasyformpluginPollLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IManageSubmissionMarker(Interface):
    """Marker"""


class IPoll(IAction):
    """Interface for Poll"""


class IPollSaveData(ISaveData):
    """Data Saver Interface for Poll."""
    
    pollFields = schema.List(
        title=_(u"label_pollfields_text", default=u"Poll Fields"),
        description=_(
            u"help_pollfields_text",
            default=u"Pick the fields whose inputs you'd like to display as "
            u"a poll. If empty, no poll will be shown.",
        ),
        unique=True,
        required=False,
        value_type=schema.Choice(vocabulary="easyform.Fields"),
    )
    directives.order_before(pollFields='showFields')
    
    showToAuthUsers = schema.Bool(
        title=_(u'field_showto_auth_users', default=u"Show results to authenticated users"),
        required=False)
    showToAnonymousUsers = schema.Bool(
        title=_(u'field_showto_anonymous_users', default=u"Show results to anonymous users"),
        required=False)
