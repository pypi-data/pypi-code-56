
from .mixins import (
    PythonMixin,
    GitMixin,
    GitChangelogMixin,
    Message
)


class ArchiveCodeMessage(GitChangelogMixin, GitMixin, PythonMixin, Message):
    template = 'archive.tpl'
