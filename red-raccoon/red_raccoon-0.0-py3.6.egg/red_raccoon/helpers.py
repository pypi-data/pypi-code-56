"""
The following module contains helper functions which can be used for things like data sanitization.
"""

import re

from hodgepodge.helpers import ensure_type

_RE_MARKDOWN_LINK = re.compile(r'\[(.+?)]\((https*:\/\/.*?)\)')
_RE_CITATION = re.compile(r'(\([cC]itation: .*?\))')


def remove_markdown_links(text):
    """
    Removes markdown links from the provided string.

    For example, given the following string:

    Let me [Google](https://www.google.com) that for you.

    The following would be returned:

    Let me Google that for you.

    :param text: a string containing a markdown link.
    :return: a string with markdown links removed.
    """
    if text:
        text = ensure_type(text, str)
        matches = re.findall(_RE_MARKDOWN_LINK, text)
        for title, url in matches:
            markdown_link = "[{}]({})".format(title, url)
            text = text.replace(markdown_link, title)
    return text


def remove_citations(text):
    """
    Removes citations from the provided string.

    For example, given the following string:

    APT28 has been active since at least 2004.(Citation: DOJ GRU Indictment Jul 2018).

    The following would be returned:

    APT28 has been active since at least 2004.

    :param text: a string containing one or more citations.
    :return: a string with citations removed.
    """
    if text:
        for citation in re.findall(_RE_CITATION, text):
            text = text.replace(citation, "")
    return text


def remove_html_tags(text):
    """
    Removes HTML tags from the provided string.

    For example, given the following string:

    <code>~/.bash_profile</code> and <code>~/.bashrc</code> are shell scripts that contain
        shell commands.

    The following would be returned:

    ~/.bash_profile and ~/.bashrc are shell scripts that contain shell commands.

    :param text: a string containing one or more sets of HTML tags.
    :return: a string with HTML tags removed.
    """
    if text:
        tags = [
            ("<code>", "</code>")
        ]
        for opening_tag, closing_tag in tags:
            if opening_tag in text and closing_tag in text:
                text = text.replace(opening_tag, "")
                text = text.replace(closing_tag, "")
    return text
