"""Provide the `Arguable` base class."""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from collections.abc import Sequence
from typing import ClassVar, Optional

from .utils import removeprefix, removesuffix


class Arguable:
    """Use as a base class to automatically configure instances via command-line arguments.

    Parameters are declared via the `config` class attribute in the form of an `argparse.Namespace`
    instance.

    Attributes:
        config: Namespace object which contains the default configuration.
        config_parser: Class-level parser, populated with parameters from config.
        config_prefix: If not None, determines the prefix for parameter names on the command line.
        config_removesuffix: Otherwise the class' name in lowercase is used, minus this suffix.
        super_parser: Application-level parser, populated with parameters from all configs.
    """

    config = Namespace()
    config_parser: ClassVar[Optional[ArgumentParser]] = None
    config_prefix: ClassVar[Optional[str]] = None
    config_removesuffix: ClassVar[str] = ''
    super_parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    @classmethod  # TODO: Remove when darglint supports it (see #100).
    def __init_subclass__(cls, prefix: str = None, removesuffix: str = None):
        """Create and update config_parser and super_parser with the class' config parameters.

        Args:
            prefix: If provided, serves as a prefix for parameter names,
                otherwise the class' name in lowercase is used.
            removesuffix: If no prefix is provided, the class' name in lowercase
                will be used, reduced by this suffix (if given).
        """
        super().__init_subclass__()
        if prefix is not None:
            cls.config_prefix = prefix
        if removesuffix is not None:
            cls.config_removesuffix = removesuffix
        cls.config_parser = ArgumentParser()
        cls.update_parser(cls.config_parser)
        cls.update_parser(cls.super_parser)

    def __init__(self, *args, **kwargs):
        """Set the `config` attribute on this instance, populated with command-line args."""
        super().__init__(*args, **kwargs)
        base = f'{self.config_base_name()}_'
        self.config = Namespace(**{
            removeprefix(name, base): value
            for name, value in vars(self.config_parser.parse_known_args()[0]).items()
        })

    @classmethod
    def config_base_name(cls):
        """Get the base name for parameters of this class."""
        if cls.config_prefix is not None:
            base = cls.config_prefix
        else:
            base = cls.__name__.lower()
            base = removesuffix(base, cls.config_removesuffix)
        return base

    @classmethod
    def update_parser(cls, parser: ArgumentParser):
        """Update the given parser with the `config` parameters of the class."""
        base = cls.config_base_name()
        for name, default in vars(cls.config).items():
            kwargs = {}
            if type(default) is bool:
                kwargs['action'] = f'store_{"false" if default else "true"}'
            else:
                if isinstance(default, Sequence) and not isinstance(default, str):
                    kwargs['type'] = type(default[0])
                    kwargs['nargs'] = len(default)
                else:
                    kwargs['type'] = type(default)
                kwargs['default'] = default
                kwargs['metavar'] = ''
            parser.add_argument(
                f'--{base}-{name.replace("_", "-")}',
                **kwargs,
                help=name.replace('_', ' ').capitalize(),
            )
