"""Note data model"""

import datetime


class Note:

    def __init__(self, label, priority, status, id=0, description=None, theme=None, start_date=None, finish_date=None):
        self._id = id
        self._label = label
        self._description = description
        self._priority = priority
        self._status = status
        self._theme = theme
        self._creation_datetime = datetime.datetime.now()
        self._start_date = start_date
        self._finish_date = finish_date

    @property
    def id(self):
        return self._id

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        self._priority = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def creation_datetime(self):
        return self._creation_datetime

    @property
    def start_date(self):
        return self._start_date

    @property
    def finish_date(self):
        return self._finish_date

    @finish_date.setter
    def finish_date(self, value):
        self._finish_date = value

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        self._theme = value

    def __str__(self):
        return "{ Note: id = " + str(self._id) + ", label = " + self._label + " }"
