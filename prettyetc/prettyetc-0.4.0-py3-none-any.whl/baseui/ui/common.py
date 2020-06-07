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
        this does not show it.

        By default it does nothing,
        however it should be called when required.

        .. note::
            This method is not called in :meth:`CommonComponent.__init__`.
        """

    @abc.abstractmethod
    def show(self):
        """
        Show the object to the user.

        Depending on the UI can be blocking or non blocking.
        """

    @abc.abstractmethod
    def close(self):
        """
        Close the object and clean it up.
        """

    def run(self, blocking: bool = True):
        """
        Implement the full lifecycle, from :meth:`CommonComponent.init_ui`
        to :meth:`CommonComponent.close`.

        It returns the result of :meth:`CommonComponent.show`.

        :param bool=True blocking:
            If True (default), this method assumes that :meth:`~CommonComponent.show`
            is blocking, so it will call :meth:`~CommonComponent.close`
            when :meth:`~CommonComponent.show` exits.
            Otherwise, the :meth:`~CommonComponent.close` will not be called by this method.

            .. versionadded:: 0.4.0
        """
        self.init_ui()
        res = self.show()
        if blocking:
            self.close()
        return res
