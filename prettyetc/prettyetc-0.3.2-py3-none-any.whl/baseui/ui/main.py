#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main component of the ui.

.. versionadded:: 0.3.0
"""

from prettyetc.etccore.confmgr import ConfigFileFactory
from prettyetc.etccore.langlib.parsers import BadInput

from .common import CommonComponent


class BaseMain(CommonComponent):  # pylint: disable=W0223
    """
    Represents the main instance of an ui.

    It defines a set of abstract methods that provide a basic abstract
    interface.

    :param ConfigFileFactory configfactory:
        The configuration file factory.

    :param callable read_callback:

        A callable object called when a config file is open.
        It should open the file at path and process it
        through the parsers (or the file matcher).

        .. deprecated:: 0.2.0
            Use predefined :meth:`~BaseMainUi.read_file` instead

    :param callable close_callback:

        Removed in 0.2.0: This parameter never works.

    .. versionchanged:: 0.2.0
        Now this class inhiterits :class:`abc.ABC`
        and all the abstract methods are decorated
        with :func:`abc.abstractmethod`.

    .. versionchanged:: 0.3.0
        Class renamed to BaseMain and moved to :mod:`prettyetc.baseui.ui.main`
    """

    loggername = "baseui.ui.main"

    @classmethod
    def main(cls, *args, **kwargs):
        """Launch the ui, using the UiLauncher."""

    def __init__(
            self,
            configfactory: ConfigFileFactory,
            *args,
            # deprecated
            read_callback=None,
            **kwargs):
        self._read_file = self._default_read
        super().__init__(*args, **kwargs)

        self.configfactory = configfactory

        # deprecated
        if read_callback is not None:
            self.logger.warning("The read_callback attribute is deprecated. "
                                "Use the read_file method instead.")
        self.read_callback = read_callback

    # helpers
    @property
    def read_file(self):
        r"""
        Read the file by path and process it.

        By default it calls all required stuffs
        to process the given config file, but doesn't show anything.

        All stuffs in the baseui package
        (the :class:`~prettyetc.baseui.main.UiLauncher` class, for example)
        expects that this method exists and has the correct behaviour

        This method behaviour can be changed by assign it
        (it is a property) or by override it.

        Here is the required method specifications:

        :param str path: Path to the file.

        :param \**factory_kwargs:
            All :class:`~prettyetc.etccore.confmgr.ConfigFileFactory` extra parameters.

        :return: The parsed :class:`~prettyetc.etccore.langlib.root.RootField`
                 from given file, or a BadInput if parsing fails.

        :rtype: :class:`~prettyetc.etccore.langlib.root.RootField` or BadInput


        .. versionadded:: 0.3.0
        """
        return self._read_file

    @read_file.setter
    def read_file(self, callback):
        """The read_file property setter."""
        if not callable(callback):
            raise TypeError(
                "Given object typed {} is not callable.".format(callback))

        self._read_file = callback

    open_config_file = read_file
    """
    Alias for :class:`~prettyetc.baseui.ui.main.BaseMain.read_file`

    .. versionchanged:: 0.3.0

        This method no longer call :meth:`~BaseMain.add_root`
        and :meth:`~BaseMain.handle_badinput` methods.

    .. deprecated:: 0.3.0
        Use read_file instead.
    """

    # write_file property

    # convert property

    # default implementations
    def _default_read(self, path: str, **factory_kwargs):
        """Default implementation of read method."""
        if self.read_callback is None:
            configfile = self.configfactory(path, **factory_kwargs)
            root = configfile.read()
            return root

            # if isinstance(root, BadInput):
            #     self.handle_badinput(path, root)
            # elif isinstance(root, RootField):
            #     self.add_root(root)
            # else:
            #     raise errhelper(TypeError("Bad root returned"), self.logger)

        # deprecated
        return self.read_callback(self, path, self.configfactory)

    # deprecations
    def add_root(self, root):
        """
        Add given :class:`~prettyetc.etccore.langlib.root.RootField` object to ui.

        .. versionchanged:: 0.3.0
            This method is no longer an abstract method.

        .. deprecated:: 0.3.0
            This method is not used by baseui components.
        """

    def handle_badinput(self, path, badinput_ex: BadInput):
        """
        Handle bad input by given :exc:`~prettyetc.etccore.langlib.parsers.BadInput`.

        .. versionchanged:: 0.3.0
            This method is no longer an abstract method.

        .. deprecated:: 0.3.0
            This method is not used by baseui components.
        """
