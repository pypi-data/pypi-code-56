from plone import api
from plone.app.layout.viewlets import common as base
from zope.annotation.interfaces import IAnnotations

from collective.easyformplugin.poll import _
from collective.easyformplugin.poll import CEFPSS


class PollEasyFormViewlet(base.ViewletBase):
    
    
    def allowSingleSubmission(self):
        try:
            if not api.user.is_anonymous():
                if api.user.has_permission('cmf.ModifyPortalContent'):
                    return False
                if self.context.Type() == 'EasyForm':
                    annotations = IAnnotations(self.context)
                    return annotations.get(CEFPSS, False)
        except:
            return False
        return False
    