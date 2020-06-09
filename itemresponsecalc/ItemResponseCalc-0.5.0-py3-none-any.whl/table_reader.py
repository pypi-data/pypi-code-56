"""Interface to read tabular data from a file,
e.g., a flat database or an Excel sheet or csv file.
This file is a base module defining a superclass for all types of data files.

*** Main Classes
Table --- superclass for variants of concrete readers of tabulated data.

Tables --- iterable chaining several sub-iterables with tabulated data.
"""
# **** use reader as context manager?

from itertools import chain

import logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------
def default_accept_all(r):
    """Default for Table property accept_row.
    :param r: list with one record from database
    :return: always True, without any checking
    """
    return True


# ---------------------------------------------------------------
class Table:
    """Superclass for all types of concrete table-storage access methods,
    allowing access to files with data stored in rows and columns.
    Typical usage:
        table = Table(...args)
        for row in table:
            do something with the row
   """
    def __init__(self, table_id,
                 fields=None,
                 field_types=int,
                 # keyed=False,
                 missing_values=None,
                 sample_factor=1,
                 accept_row=None,
                 recode_fcns=None):
        """
        :param table_id: string, file path, or other object defining concrete storage for reading
            as interpreted by sub-class
        :param fields: sequence of labels for fields to be returned in each record
            if None, ALL fields are returned
        :param field_types: list of required value types, or a single such type
            if single type, it is applied for ALL returned field values
            NOTE: MUST be callable objects that allow direct type cast, e.g.,
            field_types = int; will be used as int(row[field])
        :param keyed: boolean, if True: yield record as dictionary, otherwise as a list
        :param missing_values: list of field values as stored in the file, to be treated as missing data
            replaced by None before output.
            Field values are tested before any recoding or type-cast.
        :param sample_factor: (optional) scalar integer for down-sampling among records
            Only one record is returned for every sample_factor records in the file
        :param recode_fcns: (optional) function or list of functions to be applied to each record before output
        :param accept_row: (optional) single function to determine if a record is to be accepted
        NOTE: test for missing values, type-cast, and recoding are applied in the order
            defined in method process_row.
        """
        self.table_id = table_id
        self.fields = fields
        # ******** allow duplicates in self.fields ???
        if field_types is not None and type(field_types) is not list:
            field_types = len(self.fields) * [field_types]
        self.field_types = field_types
        if missing_values is None:
            missing_values = []
        self.missing_values = missing_values
        if accept_row is None:
            accept_row = default_accept_all
        self.accept_row = accept_row
        if recode_fcns is None:
            recode_fcns = []
        if type(recode_fcns) is not list:
            recode_fcns = [recode_fcns]
        self.recode_fcns = recode_fcns
        self.sample_factor = sample_factor

    def __repr__(self):
        return (self.__class__.__name__ + '(\n\t'
                + ',\n\t'.join((f'{k}={repr(v)}' for (k,v) in self.__dict__.items()))
                + ')')

    def __len__(self):
        """Number of (down-sampled) data records in file,
        not including header,
        exact or crudely estimated.
        This default method simply reads and counts all rows.
        Subclasses may implement faster method.
        :return: scalar integer
        """
        n = 0
        for _ in self:
            n += 1
        return n

    def __iter__(self):
        """Must be implemented by subclass
        :return: iterator over rows
        """
        raise NotImplementedError

    def process_row(self, row):
        """Check and convert ONE row as required by self properties
        :param row: list with elements corresponding to self.fields
        :return: row modified in place, or None if not accepted
        """
        # ****** raise NotAcceptedError if any error, using try-except in __iter__ ???
        self._check_missing(row)
        try:
            self._type_cast(row)
        except ValueError:
            logger.warning(f'Type error in {row}; not included')
            return None
        for fcn in self.recode_fcns:
            if fcn is not None:
                fcn(row)
        if self.accept_row(row):
            return row
        else:
            return None

    # def preview(self, max_records=10):  # ************* needed ?
    #     """Generator of raw data rows from the file.
    #     Must be implemented by sub-class.
    #     :param max_records: limit on the number of records
    #     :param keyed: boolean: if True, return data as dict  # ************ ???
    #     :return: iterator over data rows, as stored without any type casting or other checks
    #     """
    #     raise NotImplementedError

    # ----------------------------------------------------- Private:
    def _check_missing(self, row):
        """Check and convert any missing data in row
        :param row: list with selected field values from one record
        :return: None, row elements recoded in place
        """
        for i in range(len(row)):
            if row[i] in self.missing_values:
                row[i] = None

    def _type_cast(self, row):
        """Change type of row elements if required,
        change to None, if desired type-cast was not possible.
        :param row: list with selected field values from one record
        :return: None, row elements recoded in place
        """
        if self.field_types is not None:
            for (i, (r_i, type_i)) in enumerate(zip(row, self.field_types)):
                if r_i is not None:
                    try:
                        row[i] = type_i(r_i)
                    except ValueError:
                        logger.warning(f'Cannot convert {repr(r_i)} to {type_i} in {row}')
                        row[i] = None
    # ---------------------------------------------------------------


class Tables:
    """Iterable chaining sub-iterables
    """
    def __init__(self, *table_list):
        """
        :param table_list: list of iterables, e.g., lists or table_reader.Table objects.
        """
        self.table_list = table_list

    def __len__(self):
        """Total number of data records in all included sub-tables,
        exact or crudely estimated.
        :return: scalar integer
        """
        return sum(len(t) for t in self.table_list)

    def __iter__(self):
        """iterator of records in all included sub-tables
        :return: iterator over response records
        """
        return chain(*self.table_list)

