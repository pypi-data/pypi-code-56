"""Interface to read tabular data stored in an sqlite3 database
e.g., the Swedish Quality Registry, provided by Peter Nordqvist, Hearing Bridge, Sweden.

*** MAIN CLASS:
Table --- iterable interface to an sqlite database,
    accessing fields by their names as used in the database.

NOTE: the database file is always accessed in READ-ONLY mode!

VERSION HISTORY:
2019-07-11, first functional version
2019-07-28, change to Table subclass
"""
# **** use sqlite3.Rows instead of row_dict ??? ***************

# ***** Can accept_row fcn detect and skip duplicate subjectID records ??? ***********

import numpy as np
# # from collections import Counter, OrderedDict
# import warnings

import sqlite3

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
                 file_path,
                 select_from,
                 fields=None,
                 **kwargs):
        """
        :param file_path: Path or string with path to sqlite3 database file
        :param select_from: string to fill SELECT statement for records to include, e.g.,
            select_from = "prescriptions WHERE Respondent = 't' AND date >= '2016-01-01' "
            will find records using the SQL statement
            "SELECT * from prescriptions WHERE Respondent = 't' AND date >= '2016-01-01' "
        :param fields: list of key strings for selected fields of each database record
        :param kwargs: additional keyword properties for super-class, e.g.,
            field_types, keyed, accept_row, missing_values, recode_fcns
        """
        super().__init__(table_id=file_path, fields=fields, **kwargs)
        self.select_from = select_from

    def __iter__(self):
        """Generator for all records SELECTed in property select_from,
        AND also accepted and pre-processed
        as defined by self.accept_row, self.recode_fcns,
        yielding list with selected field values from those records.
        """
        con = sqlite3.connect('file:' + str(self.table_id) + '?mode=ro', uri=True)
        # *** NOTE: READ ONLY!
        con.row_factory = sqlite3.Row
        query = 'SELECT * FROM ' + self.select_from
        for (rec_n, rec) in enumerate(con.execute(query)):
            if rec_n % self.sample_factor == 0:
                if self.fields is None:
                    r = list(rec)
                else:
                    r = [rec[f] for f in self.fields]
                r = self.process_row(r)
                if r is not None:
                    yield r
        con.close()
        # ******** must close manually, even though connector is environment manager!

    def __len__(self):
        """Total number of records, disregarding accept_row
        :return: scalar integer
        """
        con = sqlite3.connect('file:' + str(self.table_id) + '?mode=ro', uri=True)
        # con.row_factory = sqlite3.Row
        # count = 'COUNT(*)'
        query = "SELECT COUNT(*) FROM " + self.select_from
        count_cursor = con.execute(query)
        n_records = count_cursor.fetchone()[0]
        con.close()
        return n_records // self.sample_factor

    def preview(self, max_records=10):
        """Generator for records SELECTed in property select_from,
        without any further filtering or recoding.
        """
        con = sqlite3.connect('file:' + str(self.table_id) + '?mode=ro', uri=True)
        # *** NOTE: READ ONLY!
        con.row_factory = sqlite3.Row
        query = 'SELECT * FROM ' + self.select_from
        # result = []
        for (rec_n, rec) in enumerate(con.execute(query)):
            if rec_n > max_records:
                break
            # result.append(dict(rec))
            yield dict(rec)
        con.close()
        # ******** must close manually, even though connector is environment manager!
        # return result

# ----------------------------------- Internal help functions:

# def row_as_dict(cursor, row):  # sqlite3.Row can also return fields by name
#     """row_factory for sqlite connector object, reading each row as a dict
#     """
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return d


# ---------------------------------------------- Module TEST:
