from tabledbmapper.logger import DefaultLogger
from tabledbmapper.sql_builder import builder


class Engine:
    """
    SQL Execution Engine
    """

    # Database connection
    _conn = None

    # Logger
    _logger = None

    def __init__(self, host, user, password, database, charset="utf8"):
        """
        Init SQL Execution Engine
        :param host: host
        :param user: user
        :param password: password
        :param database: database
        :param charset: charset
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self._logger = DefaultLogger()

    def set_logger(self, logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._logger = logger
        return self

    def query(self, sql, parameter):
        """
        Query list information
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        pass

    def count(self, sql, parameter):
        """
        Query quantity information
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        pass

    def exec(self, sql, parameter):
        """
        Execute SQL statement
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        pass


class TemplateEngine:
    """
    SQL template execution engine
    Using the jinja2 template engine
    """

    # SQL Execution Engine
    _engine = None

    def __init__(self, engine):
        """
        Init SQL Execution Engine
        :param engine: SQL Execution Engine
        """
        self._engine = engine

    def set_logger(self, logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._engine.set_logger(logger)
        return self

    def query(self, sql_template, parameter):
        """
        Query list information
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Query results
        """
        sql, param = builder(sql_template, parameter)
        return self._engine.query(sql, param)

    def count(self, sql_template, parameter):
        """
        Query quantity information
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Query results
        """
        sql, param = builder(sql_template, parameter)
        return self._engine.count(sql, param)

    def exec(self, sql_template, parameter):
        """
        Execute SQL statement
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        sql, param = builder(sql_template, parameter)
        return self._engine.exec(sql, param)
