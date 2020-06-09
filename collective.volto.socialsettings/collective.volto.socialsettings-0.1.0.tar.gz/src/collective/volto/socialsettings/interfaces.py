# -*- coding: utf-8 -*-
from collective.volto.socialsettings import _
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import List
from zope.schema import TextLine


class ISocialSettings(Interface):
    """ Interface for social settings controlpanel """

    social_links = List(
        title=_(u"Social links"),
        description=_(
            u"Insert a list of values for social links like the following "
            u"example: title|icon|url "
            u'Where: "title" is the title (name) of social network,'
            u' "icon" is an icon string (https://react.semantic-ui.com/elements/icon/#brandsicons-can-represent-logos-to-common-brands)'  # noqa
            u' and "url" is the link of social network to use or mailto:MAIL. '
            u'Example: "facebook|facebook f|http://www.facebook.com/stradanove"'  # noqa
        ),
        default=[],
        value_type=TextLine(),
    )


class ICollectiveVoltoSocialsettingsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
