"""Behaviours to assign manageSubmission (to ideas).

Includes a form field and a behaviour adapter that stores the data in the
standard Subject field.
"""

from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider

from collective.easyformplugin.poll import _
from collective.easyformplugin.poll import CEFPSS
from collective.easyformplugin.poll.interfaces import IManageSubmissionMarker


@provider(IFormFieldProvider)
class IManageSubmission(model.Schema):
    """Add manageSubmission to content
    """

    directives.fieldset(
            'settings',
            label=_(u'Settings'),
            fields=('singleSubmission',),
        )

    singleSubmission = schema.Bool(
        title=_(u'field_showto_auth_users', default=u"Only allow one submission per user"),
        required=False)


@implementer(IManageSubmission)
@adapter(IManageSubmissionMarker)
class ManageSubmission(object):
    """Store manageSubmission in the Dublin Core metadata Subject field. This makes
    manageSubmission easy to search for.
    """

    def __init__(self, context):
        self.context = context

    # the properties below are not necessary the first time when you just want to see your added field(s)
    @property
    def singleSubmission(self):
        return self.context.singleSubmission

    @singleSubmission.setter
    def singleSubmission(self, value):
        if value is None:
            value = False
        self.context.singleSubmission = value
        annotations = IAnnotations(self.context)
        annotations[CEFPSS] = value