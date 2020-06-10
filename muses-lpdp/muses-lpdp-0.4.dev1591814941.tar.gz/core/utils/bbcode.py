from precise_bbcode.bbcode import get_parser

from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.tag_pool import tag_pool


class EmailBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return BBCodeTag.render(value, option, parent)

    name = 'email'
    definition_string = '[email]{EMAIL}[/email]'
    format_string = '<a href="mailto:{EMAIL}">{EMAIL}</a>'

    class Options:
        render_embedded = False
        strip = False
        end_tag_closes = True


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
        end_tag_closes = True


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
        end_tag_closes = True


tag_pool.register_tag(RightBBCodeTag)


class JustifierBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return BBCodeTag.render(value, option, parent)

    name = 'justifier'
    definition_string = '[justifier]{TEXT}[/justifier]'
    format_string = '<p style="text-align:justify">{TEXT}</p>'

    class Options:
        render_embedded = False
        strip = False
        end_tag_closes = True


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
        end_tag_closes = True


tag_pool.register_tag(PreFormattedBBCodeTag)


class Mp3BBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return BBCodeTag.render(value, option, parent)

    name = 'mp3'
    definition_string = '[mp3]{URL}[/mp3]'
    format_string = '<audio controls src=\"{URL}\">Your browser does not support the <code>audio</code> ' \
                    'element.</audio>'

    class Options:
        render_embedded = False
        strip = False
        replace_links = False
        end_tag_closes = True


tag_pool.register_tag(Mp3BBCodeTag)


class BrBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return BBCodeTag.render(value, option, parent)

    name = 'br'
    definition_string = '[br]'
    format_string = '<br />'

    class Options:
        render_embedded = False
        strip = False
        standalone = True


tag_pool.register_tag(BrBBCodeTag)


class HrBBCodeTag(BBCodeTag):

    def render(self, value, option=None, parent=None):
        return BBCodeTag.render(value, option, parent)

    name = 'hr'
    definition_string = '[hr]'
    format_string = '<hr />'

    class Options:
        render_embedded = False
        strip = False
        standalone = True


tag_pool.register_tag(HrBBCodeTag)


def bbcode2html(text):
    parser = get_parser()
    return parser.render(text)
