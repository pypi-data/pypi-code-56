#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main component of the ui.

These components must be implemented when you want to use the baseui helper library.

In particular, your main component must be a subclass of :class:`BaseMain`

.. versionadded:: 0.3.0
"""

from prettyetc.etccore.confmgr import ConfigFileFactory
from prettyetc.etccore.langlib.parsers import BadInput
from prettyetc.etccore.langlib.root import RootField
from prettyetc.etccore.logger import errhelper

from .common import CommonComponent

__all__ = ("BaseMain", "generate_main")


class BaseMain(CommonComponent):  # pylint: disable=W0223
    """
    Represents the main instance of an UI.

    It defines a set of abstract methods that provide a basic abstract
    interface for an UI and useful methods to manage
    :class:`~prettyetc.etccore.langlib.root.RootField` instances creation and manipulation.

    :param prettyetc.etccore.confmgr.ConfigFileFactory configfactory:

        The configuration file factory.

    :param callable read_callback:

        A callable object called when a config file is open.
        It should open the file at a defined path and process it
        through the parsers (or the file matcher).

        .. deprecated:: 0.2.0
            Use predefined :meth:`~BaseMain.read_file` instead.

    :param callable close_callback:

        Removed in 0.2.0: This parameter never works.

    .. versionchanged:: 0.2.0
        Now this class inherits :class:`abc.ABC`
        and all the abstract methods are decorated
        with :func:`abc.abstractmethod`.

    .. versionchanged:: 0.3.0
        Class renamed to BaseMain and moved to :mod:`.ui.main` module.
    """

    loggername = "baseui.ui.main"

    uiname = None
    """
    The name of the UI, should be the same of the __prettyetc_ui__ module attribute.

    .. versionadded:: 0.4.0
    """

    @classmethod
    def main(cls, *args, **kwargs):
        """
        Launch the UI, using the :class:`~prettyetc.baseui.main.UiLauncher` class.

        If :attr:`~BaseMain.uiname` is set
        this method will pass to :meth:`~prettyetc.baseui.main.UiLauncher.main`,
        the ui name in the preferred_uis parameter.

        .. versionchanged:: 0.4.0
            Now this method launches the UI by calling
            :meth:`~prettyetc.baseui.main.UiLauncher.main`
            so you don't need to override it.

        """
        from prettyetc.baseui.main import UiLauncher  # pylint: disable=C0415
        if cls.uiname is not None:
            kwargs.setdefault("preferred_uis", (cls.uiname,))

        UiLauncher.main(*args, **kwargs)

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
        self._read_listeners = []

    # read file property
    @property
    def read_file(self) -> callable:
        r"""
        Read the file by path and process it.

        By default it calls all required stuffs
        to process the given config file, but doesn't show anything.

        All stuffs in the baseui package
        (the :class:`~prettyetc.baseui.main.UiLauncher` class, for example)
        expects that this method exists and it has the correct behaviour

        This method behaviour can be changed by assign it
        (it is a property) or by override it.

        Here is the required method specifications:

        :param str path: Path to the file.

        :param \*\*factory_kwargs:
            All :class:`~prettyetc.etccore.confmgr.ConfigFileFactory` extra parameters.

        :return: The parsed :class:`~prettyetc.etccore.langlib.root.RootField`
                 from given file,
                 or a :class:`~prettyetc.etccore.langlib.parsers.BadInput` if parsing fails.

        :rtype: :class:`~prettyetc.etccore.langlib.root.RootField` or
                :class:`~prettyetc.etccore.langlib.parsers.BadInput`

        .. versionadded:: 0.3.0
        """
        return self._read_file

    @read_file.setter
    def read_file(self, callback: callable):
        """The read_file property setter."""
        if not callable(callback):
            raise TypeError(
                "Given object typed {} is not callable.".format(callback))

        self._read_file = callback

    open_config_file = read_file
    """
    Alias for :meth:`~BaseMain.read_file`

    .. versionchanged:: 0.3.0

        This method no longer call :meth:`~BaseMain.add_root`
        and :meth:`~BaseMain.handle_badinput` methods.

    .. deprecated:: 0.3.0
        Use :meth:`~BaseMain.read_file` instead.
    """

    # read listeners helpers
    @property
    def read_listener(self) -> list:
        """
        Read listeners.

        Each function in this property will be called when a read operation is done.
        In other words when :meth:`BaseMain.read_file` is called.

        The listener function must take a positional argument
        that is the returned value of :meth:`BaseMain.read_file`.

        You can add a new function following 2 different ways:

        - assigning a callable to this property.
        - through the :meth:`~BaseMain.bind_read` method.

        .. versionadded 0.4.0
        """
        return self._read_listeners

    @read_listener.setter
    def read_listener(self, func):
        """Add a new listener to the event listeners."""
        if callable(func):
            self._read_listeners.append(func)
        else:
            raise TypeError(
                "Given object typed {} is not a callable object".format(
                    type(func).__name__))

    @read_listener.deleter
    def read_listener(self):
        """Clear all the listeners."""
        self._read_listeners = []

    def bind_read(self, func: callable) -> object:
        """
        Add a new function to read listeners.

        .. seealso::
            Property :attr:`~BaseMain.read_listener`

        .. versionadded 0.4.0
        """
        self.read_listener = func

    # field serializing
    def write_file(self,
                   rootfield: RootField,
                   dest_path: str = None,
                   language: str = None):
        """
        Serialize the given :class:`~prettyetc.etccore.langlib.root.RootField`
        object into string, that will be written in file.

        :param prettyetc.etccore.langlib.root.RootField rootfield:
            The RootField object to be written.

        :param str dest_path:
            If given, the rootfield will be written into file with given path,
            otherwise the rootfield path will be used.

            .. note::
                Any error in opening the file must be handled by caller.

        :param str language:
            If given, the rootfield will be written using the given language name, if available.

        :raise ValueError: If language (or dest_path) is unspecified.

        .. versionadded 0.4.0
        """
        # override = False
        if dest_path is None:
            dest_path = rootfield.name
            # override = True

        if language is None:
            language = rootfield.attributes["langname"]

        if dest_path is None:
            raise ValueError("Missing destination path.")
        if language is None:
            raise ValueError("Missing language.")

        confile = self.configfactory(dest_path)
        ex = confile.write(rootfield, language)
        if ex is not None:
            raise errhelper(ex, self.logger)

    # default implementations
    def _default_read(self, path: str, **factory_kwargs):
        """Default implementation of read method."""
        if self.read_callback is None:
            configfile = self.configfactory(path, **factory_kwargs)
            root = configfile.read()
            for listener in self._read_listeners:
                listener(root)
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
            This method no longer is an abstract method.

        .. deprecated:: 0.3.0
            This method is not used by baseui components.
        """

    def handle_badinput(self, path, badinput_ex: BadInput):
        """
        Handle bad input by given :exc:`~prettyetc.etccore.langlib.parsers.BadInput`.

        .. versionchanged:: 0.3.0
            This method is no longer an abstract method.

        .. deprecated:: 0.3.0
            This method is not used by the baseui components.
        """


def generate_main(uiname: str,
                  on_show: callable,
                  on_initui: callable = lambda *_: None,
                  on_close: callable = lambda *_: None,
                  cls: type = BaseMain) -> type:
    """
    Generate a subclass of :class:`~BaseMain`, by given callbacks and name.

    This function allows to use the prettyetc's UI dynamic launcher
    without subclassing :class:`~BaseMain` direcly.

    Here an example:

    .. code-block:: python3

        from prettyetc.baseui.ui import generate_main

        def on_show(main, *args):
            # some blocking stuffs

        __main_class__ = generate_main("example", on_show)

    All the requirements and methods specifications are in the generated subclass,
    so this function provides some parameters (a few required).

    :param str uiname: The given string becomes :attr:`~BaseMain.uiname`
        Must be provided as the :class:`~BaseMain` requires it.

        .. note::
            :class:`~BaseMain` class does not really requires it,
            but you must provide '__prettyetc_ui__', with the name of ui,
            at the same level of '__main_class__'.

    :param callable on_show: The given callable becomes :meth:`~BaseMain.show`
        It must be provided and the given callback must be blocking (returns until the UI ends).

    :param callable on_initui: The given callable becomes :meth:`~BaseMain.init_ui` (optional)

    :param callable on_close: The given callable becomes :meth:`~BaseMain.close` (optional)

    :param type cls: The base of the generated class.
        It must be a subclass of :class:`~BaseMain` or it won't be loaded into the UI launcher.

    .. important::
        Given callbacks must have at least the first parameter,
        that is the instance of BaseMain.

    .. versionadded:: 0.4.0
    """

    class _CallbackBaseMain(cls):
        """Generated BaseMain class from given callbacks."""
        uiname = uiname
        show = on_show
        init_ui = on_initui
        close = on_close

    return _CallbackBaseMain
