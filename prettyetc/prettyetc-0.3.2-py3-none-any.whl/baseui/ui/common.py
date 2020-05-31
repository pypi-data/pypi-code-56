#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Common UI components.

.. versionadded:: 0.3.0
"""

import abc

from prettyetc.etccore.logger import ChildLoggerHelper


class CommonComponent(ChildLoggerHelper, metaclass=abc.ABCMeta):
    """
    Base class of all ui components.

    It provides an interface for the object lifecycle.

    .. versionadded:: 0.3.0
    """

    loggername = "baseui.ui.common"

    def init_ui(self):
        """
        Create the basic structures for the ui,
        not showing it.

        By default it does nothing,
        however should be called when required.

        .. note::
            This method is not called in __init__.
        """

    @abc.abstractmethod
    def show(self):
        """
        Show the object to the user.

        Depending of the ui can be blocking or unblocking.
        """

    @abc.abstractmethod
    def close(self):
        """
        Unshow the object and close it.
        """

    def run(self):
        """
        Implement the full lifecycle, from init_ui to close.

        It returns the result of show.
        """
        self.init_ui()
        res = self.show()
        self.close()
        return res
