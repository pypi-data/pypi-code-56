from precise_bbcode.bbcode import get_parser

from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.tag_pool import tag_pool


class EmailBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return BBCodeTag.render(value, option, parent)

    name = 'email'
    definition_string = '[email]{EMAIL}[/email]'
    format_string = '<a href="mailto:{EMAIL}">Lien courriel : {EMAIL}</a>'

    class Options:
        render_embedded = False
        strip = False


tag_pool.register_tag(EmailBBCodeTag)


class InvisibleBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return BBCodeTag.render(value, option, parent)

    name = 'invisible'
    definition_string = '[invisible]{TEXT}[/invisible]'
    format_string = '<span style:"display:none">{TEXT}</span>'

    class Options:
        render_embedded = False
        strip = False


tag_pool.register_tag(InvisibleBBCodeTag)


class RightBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return BBCodeTag.render(value, option, parent)

    name = 'right'
    definition_string = '[right]{TEXT}[/right]'
    format_string = '<div align="right">{TEXT}</div>'

    class Options:
        render_embedded = False
        strip = False


tag_pool.register_tag(RightBBCodeTag)


class JustifierBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return BBCodeTag.render(value, option, parent)

    name = 'justify'
    definition_string = '[justifier]{TEXT}[/justifier]'
    format_string = '<p style="text-align:justify">{TEXT}</p>'

    class Options:
        render_embedded = False
        strip = False


tag_pool.register_tag(JustifierBBCodeTag)


class PreFormattedBBCodeTag(BBCodeTag):
    def render(self, value, option=None, parent=None):
        return BBCodeTag.render(value, option, parent)

    name = 'preformatted'
    definition_string = '[pre]{TEXT}[/pre]'
    format_string = '<pre>{TEXT}</pre>'

    class Options:
        render_embedded = False
        strip = False


tag_pool.register_tag(PreFormattedBBCodeTag)


def bbcode2html(text: str):
    parser = get_parser()
    return parser.render(text)
