"""Interface to read tabular data stored in MySQL database

*** MAIN CLASS:
Table --- iterable interface to an sqlite database,
    accessing fields by their names as used in the database.


NOTE: the database file is always accessed in READ-ONLY mode!

VERSION HISTORY:
2020-02-02, first functional version
"""
import numpy as np

import mysql.connector

from ItemResponseCalc import table_reader

# import logging
# logger = logging.getLogger(__name__)


# ---------------------------------------------------------------

class Table(table_reader.Table):
    """Table interface to sqlite3 database.
Provides generator function for all user records,
User can select which database records to include for analysis.
User can select which record fields are to be returned for analysis.
"""
    def __init__(self,
                 table_id,
                 connect_kwargs,
                 fields=None,
                 select_where='',
                 select_args=(),
                 **kwargs):
        """
        :param table_id: name of table in the SQL database
        :param connect_kwargs: dict with all input arguments for mysql.connect()
        :param select_where: string part of SELECT statement for records to include, e.g.,
            select_where = "Respondent = 1 AND date >= '2016-01-01' "
        :param select_args: (optional) tuple with arguments to select_where format string
        :param fields: list of key strings for selected fields of each database record
        :param kwargs: additional keyword properties for super-class, e.g.,
            field_types, keyed, accept_row, missing_values, recode_fcns
        """
        super().__init__(table_id=table_id, fields=fields, **kwargs)
        self.connect_kwargs = connect_kwargs
        self.select_where = select_where
        self.select_args = select_args

    def __iter__(self):
        """Generator for all records SELECTed in select_where, select_args
        AND also accepted and pre-processed
        as defined by self.accept_row, self.recode_fcns,
        yielding each row as a list with values of fields specified in self.fields
        """
        if self.fields is None:
            self.fields = '*'  # = all in database
        query = ('SELECT ' + ', '.join(self.fields)
                 + ' FROM ' + self.table_id
                 + ' WHERE ' + self.select_where)
        # *********** set time-out if connect fails ********************
        cnx = mysql.connector.connect(**self.connect_kwargs)
        cur = cnx.cursor()
        cur.execute(query, self.select_args)
        for (rec_n, rec) in enumerate(cur):
            if rec_n % self.sample_factor == 0:
                r = self.process_row(list(rec))  # ***************
                # r = rec
                if r is not None:
                    yield r
        cur.close()
        cnx.close()

    def __len__(self):
        """Total number of records, disregarding accept_row
        :return: scalar integer
        """
        query = ('SELECT COUNT(*) FROM '  + self.table_id
                 + ' WHERE ' + self.select_where)
        # *********** set time-out if connect fails ********************
        cnx = mysql.connector.connect(**self.connect_kwargs)
        cur = cnx.cursor()
        cur.execute(query, self.select_args)
        n_records = cur.fetchone()[0]
        cur.close()
        cnx.close()
        return n_records // self.sample_factor

    # def preview(self, max_records=10):  # ******** needed ?
    #     """Generator for records SELECTed in property select_where,
    #     without any further filtering or recoding.
    #     """
    #     query = ('SELECT * FROM ' + self.table_id
    #              + ' WHERE ' + self.select_where)
    #     cnx = mysql.connector.connect(**self.connect_kwargs)
    #     cur = cnx.cursor()
    #     cur.execute(query, self.select_args)
    #     column_names = cur.column_names
    #     for (rec_n, rec) in enumerate(cur):
    #         if rec_n > max_records:
    #             break
    #         # result.append(dict(rec))
    #         yield dict((k, v) for (k, v) in zip(column_names, rec))
    #     cur.fetchall()  # remaining
    #     cur.close()
    #     cnx.close()
    #     # return result


# ---------------------------------------------- Module TEST:

# if __name__ == '__main__':
#     import datetime as dt
#
#     haq_config = dict(user='leijon',
#                       password='*********',
#                       host='172.16.0.7',
#                       port='1111',
#                       database='hbdb')
#     table = 'prescriptions'
#
#     SELECT_WHERE = ("respondent = 1 " +
#                     "AND article_company IS NOT NULL " +
#                     "AND date BETWEEN %s AND %s"
#                     )
#     where_args = (dt.date(2019, 1, 1), dt.date(2019, 12, 31))
#
#     fields = ['id', 'civil_registration_number'] + [f'Q{i}' for i in np.arange(3, 10)]
#     ioiha_query = 'SELECT ' + ', '.join(fields) + ' FROM ' + table + ' where ' + SELECT_WHERE
#     print('query: ', ioiha_query)  # , where_args)
#
#     # --------------------------------- Test Table
#     haq_table = Table(table_id=table,
#                       connect_kwargs=haq_config,
#                       select_where=SELECT_WHERE,
#                       select_args=where_args,
#                       fields=fields)
#
#     # print('len(haq_table)= ', len(haq_table))
#     print('\n*** haq_table.preview(10)=\n')
#     for r in haq_table.preview(10):
#         print(r)
#
