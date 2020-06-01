# coding: utf-8

from pymssql import connect
import sys
import datetime as dt
import pandas as pd
import logging


def _config_logger(file_path, file_name):
    logger = logging.getLogger('exportacao1')
    logger.setLevel(logging.DEBUG)
    formato = '%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s'

    ch = logging.StreamHandler()  # StreamHandler logs to console
    ch.setLevel(logging.DEBUG)
    ch_format = logging.Formatter(formato)
    ch.setFormatter(ch_format)
    logger.addHandler(ch)

    # fh = logging.FileHandler("{0}.log".format(file_path + file_name))
    # fh.setLevel(logging.DEBUG)
    # fh_format = logging.Formatter(formato)
    # fh.setFormatter(fh_format)
    # logger.addHandler(fh)

    return logger


def _shutdownLogger():
    logging.shutdown()


class AuditQuerysObj:

    def __init__(self):
        self._user = None
        self._query = None
        self._rows = None
        self._seconds = None

    def inicia(self, user, query, rows, seconds):
        self._user = user
        self._query = query
        self._rows = rows
        self._seconds = seconds

    def set_user(self, user):
        self._user = user

    def set_query(self, query):
        self._query = query

    def set_rows(self, rows):
        self._rows = rows

    def set_seconds(self, seconds):
        self._seconds = seconds

    def to_string(self):
        return 'AuditQuerysObj [user: {}, query: {}, rows: {}, seconds: {}]'.format(self._user, self._query, self._rows,
                                                                                    self._seconds)


class MsSqlUtils:
    def __init__(self):
        '''Contrutor fo this class'''
        self._server = None
        self._port = None
        self._user = None
        self._password = None
        self._database = "db_dw"
        self._timeout = 0
        self._login_timeout = 60
        self._charset = "UTF-8"
        self._as_dict = True
        self._appname = "pythonDW"
        self._autocommit = False
        self._conn = None
        self._auditQuerysObj = None
        self._f_logger = None

    def set_parameters(self, server, port, user, password, database,
                   timeout=0, login_timeout=60, charset="UTF-8",
                   as_dict=True, appname="pythonDW", autocommit=False
                   ):
        self._server = server
        self._port = port
        self._user = user
        self._password = password
        self._database = database
        self._timeout = timeout
        self._login_timeout = login_timeout
        self._charset = charset
        self._as_dict = as_dict
        self._appname = appname
        self._autocommit = autocommit

    def set_credentials(self, user, password):
        self._user = user
        self._password = password

    def set_database(self, database):
        self._database = database

    def set_hostname_port(self, hostname, port):
        self._server = hostname
        self._port = port

    def __open_connect(self, as_dict):
        self._f_logger.info('Estabelecendo conexão com o banco')
        try:
            self.conn = connect(server=self._server, port=self._port, database=self._database,
                                user=self._user, password=self._password, timeout=self._timeout,
                                login_timeout=self._login_timeout, charset=self._charset, as_dict=as_dict,
                                appname=self._appname, autocommit=self._autocommit
                                )
        except Exception as e:
            self._f_logger.error('Não foi possivel estabelecer conexão com o banco de dados')
            self._f_logger.error('Mensagem de erro de retorno')
            self._f_logger.log(40, e)
            _shutdownLogger()
            sys.exit(0)

        self._f_logger.info('Conexão estabelecida com sucesso')

    def __close_connect(self):
        self._f_logger.info('Fechando conexão')
        self.conn.close()

    def __get_cursor(self):
        self._f_logger.info('Obtendo cursor')
        try:
            cursor = self.conn.cursor()
        except Exception as e:
            self._f_logger.error('Erro ao obter cursor')
            self._f_logger.error('Mensagem de erro de retorno')
            self._f_logger.log(40, e)
            _shutdownLogger()
            sys.exit(0)
        self._f_logger.info('Cursor obtido com sucesso')
        return cursor

    def __exec_query(self, cursor, query):
        self._f_logger.info('Adicionando query')

        try:

            cursor.execute(query)
            self._f_logger.info('Consultando, aguarde...')
            resultado = cursor.fetchall()

        except Exception as e:
            self._f_logger.error('Erro ao executar query')
            self._f_logger.error('Mensagem de erro de retorno')
            self._f_logger.log(40, e)
            _shutdownLogger()
            sys.exit(0)

        self._f_logger.info('Retorno obtido')
        self._f_logger.info('Fechando cursor')
        cursor.close()
        return resultado

    def fetch_all(self, query, as_dict=False):
        self._f_logger = _config_logger("./", "log")

        self.__open_connect(as_dict)
        cursor = self.__get_cursor()
        a = dt.datetime.now()
        resultado = self.__exec_query(cursor, query)
        b = dt.datetime.now()
        segundos = (b - a).total_seconds()
        self._f_logger.info('Leitura do Banco e processamento demorou : {} segundos'.format(segundos))
        qtd_linhas = len(resultado)
        self._f_logger.info('Rows: {} '.format(qtd_linhas))
        self.__close_connect()

        self._auditQuerysObj = AuditQuerysObj()
        self._auditQuerysObj.inicia(self._user, query, qtd_linhas, segundos)

        self._f_logger.info('Auditoria: {}'.format(self._auditQuerysObj.to_string()))
        return resultado

    def fetch_all_to_df(self, query):
        resultado = self.fetch_all(query, True)
        self._f_logger.info('Convertendo => Dict to DataFrame')
        a = dt.datetime.now()
        pd_result = pd.DataFrame.from_dict(resultado)
        b = dt.datetime.now()
        segundos = (b - a).total_seconds()
        self._f_logger.info('Conversão demorou : {} segundos'.format(segundos))
        return pd_result
