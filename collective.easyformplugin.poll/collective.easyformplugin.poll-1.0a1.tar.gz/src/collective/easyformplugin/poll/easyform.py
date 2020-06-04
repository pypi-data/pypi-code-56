from collective.easyform.actions import Action
from collective.easyform.actions import ActionFactory
from collective.easyform.interfaces import IAction
from collective.easyform.interfaces import ISaveData
from collective.easyform.actions import SaveData
from collective.easyform.actions import getFieldsInOrder
from collective.easyform.actions import get_context
from collective.easyform.actions import get_schema
from plone import api
from plone.supermodel.exportimport import BaseHandler
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer

from collective.easyformplugin.poll import _
from collective.easyformplugin.poll import CEFPSS, CEFPSV
from collective.easyformplugin.poll.interfaces import IPoll
from collective.easyformplugin.poll.interfaces import IPollSaveData


import logging


logger = logging.getLogger('collective.easyformplugin.poll')


@implementer(IPoll)
class PollTrigger(Action):
    """Action Executor for easyform IPoll adapter"""


@implementer(IPollSaveData)
class PollSaveData(SaveData):
    """Data Saver for Poll."""

    def __init__(self, **kw):
        for i, f in IPollSaveData.namesAndDescriptions():
            setattr(self, i, kw.pop(i, f.default))
        super(PollSaveData, self).__init__(**kw)

    def getPollFormInput(self):
        fieldData = self.getSavedFormInput()
        data = []
        for d in fieldData:
            data.append({k: d.get(k, '') for k in self.pollFields})
        return data

    def tallyFormInput(self):
        fieldData = self.getSavedFormInput()
        tally = {q:{} for q in self.pollFields}
        for data in fieldData:
            for ques in self.pollFields:
                if ques not in data:
                    continue
                elif data[ques] not in tally[ques]:
                    tally[ques][data[ques]] = 1
                else:
                    tally[ques][data[ques]] +=  1
        return tally

    def getColumnNamePair(self, filterField=None):
        # """Returns a list of column titles"""
        context = get_context(self)
        showFields = []
        if filterField:
            showFields = getattr(self, "pollFields", [])
            if showFields is None:
                showFields = []

        names = {
            name: field.title
            for name, field in getFieldsInOrder(get_schema(context))
            if not showFields or name in showFields
        }
        return names


    def onSuccess(self, fields, request):
        context = get_context(self)
        annotations = IAnnotations(context)
        singleSubmission = annotations.get(CEFPSS, False)
        voters = annotations.get(CEFPSV, [])
        if not api.user.is_anonymous():
            auth_user = api.user.get_current()
            if singleSubmission and auth_user.id in voters:
                return False
            voters.append(auth_user.id)
            annotations[CEFPSV] = voters
        super(PollSaveData, self).onSuccess(fields, request)
        


PollAction = ActionFactory(
    PollTrigger, _(u'PollTrigger'),
    'collective.easyformplugin.poll.easyform.PollTrigger'
)

PollSaveDataAction = ActionFactory(
    PollSaveData, _(u'PollSaveData'),
    'collective.easyformplugin.poll.easyform.PollSaveData'
)

PollHandler = BaseHandler(PollTrigger)
PollSaveDataHandler = BaseHandler(PollSaveData)