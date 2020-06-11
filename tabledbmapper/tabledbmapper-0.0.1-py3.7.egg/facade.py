from tabledbmapper.manager.mvc.dao import DAO
from tabledbmapper.manager.mvc.service import Service
from tabledbmapper.sql_builder import builder
from tabledbmapper.engine import TemplateEngine
from tabledbmapper.manager.manager import Manager as Manage
from tabledbmapper.manager.xml_config import parse_config_from_string, parse_config_from_file


class Engine:
    """
    SQL Execution Engine
    """
    @staticmethod
    def get_template_engine(engine):
        return TemplateEngine(engine)


class Manager:
    """
    Summary of Manager operations
    """
    @staticmethod
    def get_by_config(template_engine, xml_config):
        """
        Initialize Manager
        :param template_engine: SQL template execution engine
        :param xml_config: XML profile information
        """
        return Manage(template_engine, xml_config)

    @staticmethod
    def get_by_string(template_engine, xml_string):
        """
        Get manager using string
        :param template_engine: SQL template execution engine
        :param xml_string: xml Character string
        :return: Manager
        """
        config = parse_config_from_string(xml_string)
        return Manage(template_engine, config)

    @staticmethod
    def get_by_file(template_engine, xml_path):
        """
        Get manager using XML file
        :param template_engine: SQL template execution engine
        :param xml_path: XML file path
        :return: Manager
        """
        config = parse_config_from_file(xml_path)
        return Manage(template_engine, config)


class MVC:
    """
    Summary of MVC operations
    """
    @staticmethod
    def get_dao(manager):
        """"
        Initialize Dao layer
        :param manager: Database manager
        :return DAO
        """
        return DAO(manager)

    @staticmethod
    def get_service(dao):
        """
        Initialize service layer
        :param dao: Dao layer
        :return Service
        """
        return Service(dao)


class Builder:
    """
    Summary of builder operations
    """
    @staticmethod
    def sql_builder(template, parameter):
        """
        Build SQL string
        :param template: Init jinja2 template
        :param parameter: Parameter
        :return: Jinja2 template return
        """
        return builder(template, parameter)


class Config:
    """
    Summary of Config operations
    """
    @staticmethod
    def parse_from_string(xml_string):
        """
        Parsing XML configuration string
        :param xml_string: XML configuration string
        :return: Profile information dictionary
        """
        return parse_config_from_string(xml_string)

    @staticmethod
    def parse_from_file(file_path):
        """
        Parsing XML configuration file
        :param file_path: Profile path
        :return: Profile information dictionary
        """
        return parse_config_from_file(file_path)


class TableDBMapper:
    """
    Summary of common operations
    """
    # SQL Execution Engine
    Engine = Engine
    # Manager
    Manager = Manager
    # MVC
    MVC = MVC
    # Build SQL string
    Builder = Builder
    # Config
    Config = Config
