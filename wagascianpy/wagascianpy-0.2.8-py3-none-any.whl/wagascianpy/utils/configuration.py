# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
from enum import Enum

import configparser
import dependency_injector.containers
import dependency_injector.providers
import inflection
import os
import pprint
from six import string_types
from typing import Optional, Dict, List, Any, Tuple, Iterable

import wagascianpy.utils.environment
import wagascianpy.utils.utils
from wagascianpy.utils.classproperty import classproperty


class RepositoryType(Enum):
    Simple = 1
    Borg = 2


###############################################################################################
#                                        Default values                                       #
###############################################################################################

# WAGASCI database configuration
_WAGASCI_REPOSITORY_LOCATION = "kekcc:/hsm/t2k/t2k_JB/t2k_wagasci/rawdata"
_WAGASCI_REPOSITORY_TYPE = RepositoryType.Simple
_WAGASCI_DATABASE_LOCATION = "kekcc:/hsm/nu/wagasci/data/beam/wagascidb.db"
_WAGASCI_DOWNLOAD_LOCATION = "/tmp/rawdata"
_WAGASCI_DECODED_LOCATION = "/tmp/decoded"
_WAGASCI_DEFAULT_DATABASE_NAME = "wagascidb.db"

# BSD database configuration
_BSD_REPOSITORY_LOCATION = "kekcc:/gpfs/fs03/t2k/beam/exp/data/beam_summary/current"
_BSD_DOWNLOAD_LOCATION = "/tmp/bsd"
_BSD_DATABASE_LOCATION = "kekcc:/hsm/nu/wagasci/data/bsd/bsddb.db"
_BSD_DEFAULT_DATABASE_NAME = "bsddb.db"

# Global configuration
_T2KRUN = 10
_DATA_QUALITY_LOCATION = "/tmp/data_quality"

# Temperature database configuration
_TEMPERATURE_DATABASE_LOCATION = "kekcc:/hsm/nu/wagasci/data/temphum/mh_temperature_sensors_t2krun10.sqlite3"

# Volatile configuration (not stored to file)
_WAGASCI_UPDATE_DATABASE = False
_WAGASCI_REBUILD_DATABASE = False
_BSD_UPDATE_DATABASE = False
_BSD_REBUILD_DATABASE = False


###############################################################################################
#                                         Utilities                                           #
###############################################################################################

def conf_file_finder(filename, project_path=None):
    # type: (str, Optional[str]) -> str
    home = os.path.expanduser("~")
    wagasci_environ = None

    try:
        env = wagascianpy.utils.environment.WagasciEnvironment()
        wagasci_environ = env["WAGASCI_CONFDIR"]
    except KeyError:
        pass

    wagasci_project = os.path.join(project_path, filename) if project_path is not None else None
    if wagasci_environ:
        wagasci_environ = os.path.join(wagasci_environ, filename)
    wagasci_user = os.path.join(home, '.wagasci', filename)
    wagasci_system = os.path.join('/usr/local/wagasci/', filename)

    if wagasci_project and os.path.exists(wagasci_project):
        conf_file = wagasci_project
    elif wagasci_environ and os.path.exists(wagasci_environ):
        conf_file = wagasci_environ
    elif wagasci_user and os.path.exists(wagasci_user):
        conf_file = wagasci_user
    elif wagasci_system and os.path.exists(wagasci_system):
        conf_file = wagasci_system
    else:
        wagascianpy.utils.utils.mkdir_p(os.path.join(home, '.wagasci'))
        conf_file = wagasci_user
    return conf_file


def _conf_setter_raise(cls, name, value):
    # type: (Any, str, Any) -> None
    raise ValueError("Invalid value {} for option {} of class {}".format(name, value, cls.__name__))


def conf_setter(cls, name, value):
    # type: (Any, str, Any) -> None
    try:
        if isinstance(getattr(cls, name), Enum):
            if isinstance(value, Enum):
                setattr(cls, name, value)
            elif isinstance(value, int):
                setattr(cls, name, type(getattr(cls, name))(value))
            elif isinstance(value, string_types):
                if '.' in value:
                    value = value.split('.')[1]
                try:
                    setattr(cls, name, getattr(type(getattr(cls, name)), inflection.camelize(value.lower())))
                except AttributeError:
                    raise ValueError
        elif isinstance(getattr(cls, name), bool):
            if isinstance(value, string_types):
                value = value.lower()
            if value in [0, False, None, 'none', 'false', 'off', 'no']:
                setattr(cls, name, False)
            elif value in [1, True, 'true', 'on', 'yes']:
                setattr(cls, name, True)
            else:
                raise ValueError
        elif isinstance(getattr(cls, name), int):
            setattr(cls, name, int(value))
        elif isinstance(getattr(cls, name), float):
            setattr(cls, name, float(value))
        else:
            setattr(cls, name, str(value))
    except ValueError:
        _conf_setter_raise(cls, name, value)


def conf_getter(cls, name):
    # type: (Any, str) -> Any
    return getattr(cls, name)


###############################################################################################
#                                    Configuration classes                                    #
###############################################################################################


class VirtualConfiguration(object, metaclass=classproperty.meta):

    @classmethod
    def to_dict(cls):
        # type: (...) -> Dict[str, Any]
        return {key: val.__get__(instance=None, owner=cls) for key, val in vars(cls).items()
                if isinstance(val, classproperty)}

    @classmethod
    def get_hidden_vars(cls):
        # type: (...) -> Iterable[str]
        return [key for key, val in vars(cls).items()
                if key.startswith('_') and not key.startswith('__') and not callable(val)]

    @classmethod
    def get_classproperties(cls):
        # type: (...) -> Iterable[str]
        return [key for key, val in vars(cls).items() if isinstance(val, classproperty)]


# noinspection PyMethodParameters,PyPropertyDefinition
class GlobalConfiguration(VirtualConfiguration):
    _t2krun = _T2KRUN
    _data_quality_location = _DATA_QUALITY_LOCATION

    @classmethod
    def reset(cls):
        cls._t2krun = _T2KRUN
        cls._data_quality_location = _DATA_QUALITY_LOCATION

    @classmethod
    def is_volatile(cls):
        return False

    @classproperty
    def t2krun(cls):
        return conf_getter(cls=cls, name='_t2krun')

    @t2krun.setter
    def t2krun(cls, value):
        conf_setter(cls=cls, name='_t2krun', value=value)

    @classproperty
    def data_quality_location(cls):
        return conf_getter(cls=cls, name='_data_quality_location')

    @data_quality_location.setter
    def data_quality_location(cls, value):
        conf_setter(cls=cls, name='_data_quality_location', value=value)


# noinspection PyMethodParameters,PyPropertyDefinition
class VolatileConfiguration(VirtualConfiguration):
    _wagasci_update_database = _WAGASCI_UPDATE_DATABASE
    _wagasci_rebuild_database = _WAGASCI_REBUILD_DATABASE
    _bsd_update_database = _BSD_UPDATE_DATABASE
    _bsd_rebuild_database = _BSD_REBUILD_DATABASE

    @classmethod
    def reset(cls):
        cls._wagasci_update_database = _WAGASCI_UPDATE_DATABASE
        cls._wagasci_rebuild_database = _WAGASCI_REBUILD_DATABASE
        cls._bsd_update_database = _BSD_UPDATE_DATABASE
        cls._bsd_rebuild_database = _BSD_REBUILD_DATABASE

    @classmethod
    def is_volatile(cls):
        return True

    @classproperty
    def wagasci_update_database(cls):
        return conf_getter(cls=cls, name='_wagasci_update_database')

    @wagasci_update_database.setter
    def wagasci_update_database(cls, value):
        conf_setter(cls=cls, name='_wagasci_update_database', value=value)

    @classproperty
    def wagasci_rebuild_database(cls):
        return conf_getter(cls=cls, name='_wagasci_rebuild_database')

    @wagasci_rebuild_database.setter
    def wagasci_rebuild_database(cls, value):
        conf_setter(cls=cls, name='_wagasci_rebuild_database', value=value)

    @classproperty
    def bsd_update_database(cls):
        return conf_getter(cls=cls, name='_bsd_update_database')

    @bsd_update_database.setter
    def bsd_update_database(cls, value):
        conf_setter(cls=cls, name='_bsd_update_database', value=value)

    @classproperty
    def bsd_rebuild_database(cls):
        return conf_getter(cls=cls, name='_bsd_rebuild_database')

    @bsd_rebuild_database.setter
    def bsd_rebuild_database(cls, value):
        conf_setter(cls=cls, name='_bsd_rebuild_database', value=value)


# noinspection PyMethodParameters,PyPropertyDefinition
class WagasciDatabaseConfiguration(VirtualConfiguration):
    _wagasci_repository_location = _WAGASCI_REPOSITORY_LOCATION
    _repository_type = _WAGASCI_REPOSITORY_TYPE
    _wagasci_database_location = _WAGASCI_DATABASE_LOCATION
    _wagasci_download_location = _WAGASCI_DOWNLOAD_LOCATION
    _wagasci_decoded_location = _WAGASCI_DECODED_LOCATION
    _default_database_name = _WAGASCI_DEFAULT_DATABASE_NAME

    @classmethod
    def reset(cls):
        cls._wagasci_repository_location = _WAGASCI_REPOSITORY_LOCATION
        cls._repository_type = _WAGASCI_REPOSITORY_TYPE
        cls._wagasci_database_location = _WAGASCI_DATABASE_LOCATION
        cls._wagasci_download_location = _WAGASCI_DOWNLOAD_LOCATION
        cls._wagasci_decoded_location = _WAGASCI_DECODED_LOCATION
        cls._default_database_name = _WAGASCI_DEFAULT_DATABASE_NAME

    @classmethod
    def is_volatile(cls):
        return False

    @classproperty
    def wagasci_repository_location(cls):
        return conf_getter(cls=cls, name='_wagasci_repository_location')

    @wagasci_repository_location.setter
    def wagasci_repository_location(cls, value):
        conf_setter(cls=cls, name='_wagasci_repository_location', value=value)

    @classproperty
    def repository_type(cls):
        return conf_getter(cls=cls, name='_repository_type')

    @repository_type.setter
    def repository_type(cls, value):
        conf_setter(cls=cls, name='_repository_type', value=value)

    @classproperty
    def wagasci_database_location(cls):
        return conf_getter(cls=cls, name='_wagasci_database_location')

    @wagasci_database_location.setter
    def wagasci_database_location(cls, value):
        conf_setter(cls=cls, name='_wagasci_database_location', value=value)

    @classproperty
    def wagasci_download_location(cls):
        return conf_getter(cls=cls, name='_wagasci_download_location')

    @wagasci_download_location.setter
    def wagasci_download_location(cls, value):
        conf_setter(cls=cls, name='_wagasci_download_location', value=value)

    @classproperty
    def wagasci_decoded_location(cls):
        return conf_getter(cls=cls, name='_wagasci_decoded_location')

    @wagasci_decoded_location.setter
    def wagasci_decoded_location(cls, value):
        conf_setter(cls=cls, name='_wagasci_decoded_location', value=value)

    @classproperty
    def default_database_name(cls):
        return conf_getter(cls=cls, name='_default_database_name')

    @default_database_name.setter
    def default_database_name(cls, value):
        conf_setter(cls=cls, name='_default_database_name', value=value)


# noinspection PyMethodParameters,PyPropertyDefinition
class BsdDatabaseConfiguration(VirtualConfiguration):
    _bsd_repository_location = _BSD_REPOSITORY_LOCATION
    _bsd_download_location = _BSD_DOWNLOAD_LOCATION
    _bsd_database_location = _BSD_DATABASE_LOCATION
    _default_database_name = _BSD_DEFAULT_DATABASE_NAME

    @classmethod
    def reset(cls):
        cls._bsd_repository_location = _BSD_REPOSITORY_LOCATION
        cls._bsd_download_location = _BSD_DOWNLOAD_LOCATION
        cls._bsd_database_location = _BSD_DATABASE_LOCATION
        cls._default_database_name = _BSD_DEFAULT_DATABASE_NAME

    @classmethod
    def is_volatile(cls):
        return False

    @classproperty
    def bsd_repository_location(cls):
        return conf_getter(cls=cls, name='_bsd_repository_location')

    @bsd_repository_location.setter
    def bsd_repository_location(cls, value):
        conf_setter(cls=cls, name='_bsd_repository_location', value=value)

    @classproperty
    def bsd_download_location(cls):
        return conf_getter(cls=cls, name='_bsd_download_location')

    @bsd_download_location.setter
    def bsd_download_location(cls, value):
        conf_setter(cls=cls, name='_bsd_download_location', value=value)

    @classproperty
    def bsd_database_location(cls):
        return conf_getter(cls=cls, name='_bsd_database_location')

    @bsd_database_location.setter
    def bsd_database_location(cls, value):
        conf_setter(cls=cls, name='_bsd_database_location', value=value)

    @classproperty
    def default_database_name(cls):
        return conf_getter(cls=cls, name='_default_database_name')

    @default_database_name.setter
    def default_database_name(cls, value):
        conf_setter(cls=cls, name='_default_database_name', value=value)


# noinspection PyMethodParameters,PyMethodParameters,PyPropertyDefinition
class TemperatureConfiguration(VirtualConfiguration):
    _temperature_database_location = _TEMPERATURE_DATABASE_LOCATION

    @classmethod
    def reset(cls):
        cls._temperature_database_location = _TEMPERATURE_DATABASE_LOCATION

    @classmethod
    def is_volatile(cls):
        return False

    @classproperty
    def temperature_database_location(cls):
        return conf_getter(cls=cls, name='_temperature_database_location')

    @temperature_database_location.setter
    def temperature_database_location(cls, value):
        conf_setter(cls=cls, name='_temperature_database_location', value=value)


###############################################################################################
#                                    Configuration parser                                     #
###############################################################################################


class WagasciConfigParser(GlobalConfiguration,
                          WagasciDatabaseConfiguration,
                          BsdDatabaseConfiguration,
                          TemperatureConfiguration):

    def _baseclasses(self):
        # type: (...) -> Optional[Tuple]
        base_classes = WagasciConfigParser.__bases__
        if self.__class__ != WagasciConfigParser:
            base_classes += tuple([bc for bc in self.__class__.__bases__ if bc != WagasciConfigParser])
        return base_classes

    def __init__(self, config_file_path=None):
        # type: (Optional[str]) -> None

        # Create ConfigParser default object
        self._config_parser = configparser.ConfigParser()

        # Set default values and create the section object attributes
        for base_class in self._baseclasses():
            section_name = inflection.underscore(base_class.__name__)
            setattr(self, section_name, base_class)

        # fill the ConfigParser object
        self._fill_config_parser()

        # check file access permissions
        if config_file_path:
            if not os.access(os.path.dirname(config_file_path), os.W_OK):
                raise OSError("The configuration file path is not writable "
                              "by the current user : %s" % config_file_path)
            # If the configuration file exists read it
            if os.path.exists(config_file_path):
                self._config_parser.read(config_file_path)
                for section in self._config_parser.sections():
                    if not hasattr(self, section):
                        raise AttributeError("Section name not recognized : %s" % section)
                    for key, val in self._config_parser.items(section=section):
                        setattr(getattr(self, section), key, val)
            # Write the configuration to file
            with open(config_file_path, 'w') as configfile:
                self._config_parser.write(configfile)

    def get_sections(self):
        # type: (...) -> Optional[List[str]]
        return [key for key in vars(self) if not key.startswith('_')]

    def get_section(self, name):
        # type: (str) -> Any
        return getattr(self, name)

    def prettyprint(self):
        for section in self.get_sections():
            print()
            print(section.upper().replace('_', ' '))
            pprint.pprint(self.get_section(section).to_dict())

    def _fill_config_parser(self):
        for section in self.get_sections():
            if not self.get_section(section).is_volatile():
                if not self._config_parser.has_section(section):
                    self._config_parser.add_section(section)
                for key, var in self.get_section(section).to_dict().items():
                    if isinstance(var, Enum):
                        var = str(var).split('.')[1]
                    self._config_parser.set(section, key, str(var))

    def write(self, config_file_path):
        self._fill_config_parser()
        with open(config_file_path, 'w') as configfile:
            self._config_parser.write(configfile)


###############################################################################################
#                                Configuration Global Object                                  #
###############################################################################################


def create_sections(cls):
    conf_file = conf_file_finder(filename='wagasci_conf.ini', project_path='../..')
    parser = WagasciConfigParser(conf_file)
    setattr(cls, 'parser', parser)
    for section in parser.get_sections():
        setattr(cls, section, dependency_injector.providers.Configuration(section))
        getattr(cls, section).override(getattr(parser, section).to_dict())
    return cls


@create_sections
class Configuration(dependency_injector.containers.DeclarativeContainer):
    """IoC container of configuration providers."""

    @classmethod
    def create_section(cls, name):
        # type: (str) -> None
        if not hasattr(cls, name):
            setattr(cls, name, dependency_injector.providers.Configuration(name))

    @classmethod
    def delete_section(cls, name):
        # type: (str) -> None
        if hasattr(cls, name):
            delattr(cls, name)

    @classmethod
    def get_sections(cls):
        # type: (...) -> Optional[List[str]]
        return [val.get_name() for val in vars(cls).values()
                if isinstance(val, dependency_injector.providers.Configuration)]


if __name__ == "__main__":
    Configuration.parser.prettyprint()
