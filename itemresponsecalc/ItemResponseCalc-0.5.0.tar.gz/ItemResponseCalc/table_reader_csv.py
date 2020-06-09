"""Interface to read Item Response Data stored in a .csv file.

*** MAIN CLASS:
Table --- iterable read-only interface to a csv file,
    accessing fields by their names as defined in the first row of the file.

NOTE: This Table class assumes csv dialect = 'excel'.
The first row in the file MUST include strings corresponding to the Table fields property.

Among all possible csv format parameters,
the Table allows only delimiter and quotechar to be assigned by the user.
csv.quoting is always csv.QUOTE_NONNUMERIC, i.e. all numeric fields are read as float values.
"""
import csv
from . import table_reader


# -----------------------------------------------------------------
class Table(table_reader.Table):
    """Reader for tabular data stored in CSV file,
    using python standard csv library
    """
    def __init__(self, file_path, fields=None, delimiter=',', quotechar='"', **kwargs):
        super().__init__(file_path, fields, **kwargs)
        self.delimiter = delimiter
        self.quotechar = quotechar

    def __iter__(self):
        """Generator of file rows for read-only access.
        :return: iterator object over file rows, except header
        """
        with self.table_id.open('r', newline='') as f:
            reader = csv.reader(f, delimiter=self.delimiter,
                                quotechar=self.quotechar,
                                quoting=csv.QUOTE_NONNUMERIC)
            if self.fields is None:
                field_index = None
            else:
                header = next(reader)
                # = first row
                field_index = [header.index(f_i) for f_i in self.fields]
            for (row_n, row) in enumerate(reader):
                if row_n % self.sample_factor == 0:
                    if field_index is not None:
                        row =[row[f_i] for f_i in field_index]
                    # else keep all fields
                    row = self.process_row(row)
                    if row is not None:
                        yield row

    def preview(self, max_records=10):
        """Generator of rows for read-only access.
        :return: iterator object over file rows, except header
        """
        with self.table_id.open('r', newline='') as f:
            reader = csv.reader(f, delimiter=self.delimiter, quotechar=self.quotechar)
            for (row_n, row) in enumerate(reader):
                if row_n > max_records:
                    break
                yield row
        # return result


# ------------------------------------------------------------ TEST:
# if __name__ == '__main__':
#     from pathlib import Path
#
#     HAQ_PATH = Path.home() / 'Documents/LeijonKTH/heartech/HA-QualityRegistry'
#     # top-dir for everything to be used here
#
#     ioiha_data_path = HAQ_PATH / 'IRT-IOI-HA' / 'IOI-HA-data'
#     # to ioi-ha data sets OTHER THAN the Swedish Quality Registry
#
#     ioiha_kramer = ioiha_data_path / 'Kramer'
#
#     kramer_file = ioiha_kramer / 'moeder_final - kopieforArne.sav'
#     kramer_file = ioiha_data_path / 'Kramer' / 'NLSH-Kramer-T2IOI-HA.sav'
#     kramer_file = kramer_file.with_suffix('.csv')
#
#     print('Testing kramer_file preview:')
#     reader = Table(kramer_file).preview(10)
#     row0 = next(reader)
#     print('header= ', row0)
#     for (n, line) in enumerate(reader):
#         print(line)
#
#     # spss = Table(kramer_file)
#     # print('spss.header = ', spss.header)
#     #
#     # data = spss.preview(10)
#     # print('spss.preview(10) =\n', data)
#
#     # -------------------------------- test with missing-values recoding:
#     print('Testing kramer_file Table: ')
#     csvt = Table(kramer_file,
#                  # fields=['ioi_v1', 'ioi_v2', 'ioi_v3'],
#                  fields=[f'T2IOIHA{i+1}' for i in range(7)],
#                  missing_values=[9999999.0],
#                  field_types=str)
#     print('repr(csvt)= ', csvt)
#
#     for (n, row) in enumerate(csvt, start=1):
#         if n > 10:
#             break
#         print(f'row #{n} = {row}')
#
#     # -------------------------------------------------------------------
#     print('\n*** final test with missing_values, type_cast, recode_fcn ***\n')
#
#     def recode_missing(row):
#         for i in range(len(row)):
#             if row[i] is None:
#                 row[i] = 0
#
#     def recode_fields14(row):
#         """IOI-HA items 1,2,3,4 coded as 0-4,
#         recode to 1-5,
#         BEFORE recoding missing-data as zero.
#         """
#         for i in [1, 4]:
#             if row[i-1] is not None:
#                 row[i-1] += 1
#     # --------------------------------------------
#
#     csvt = Table(kramer_file,
#                  # fields=['ioi_v1', 'ioi_v2', 'ioi_v3'],
#                  fields=[f'T2IOIHA{i+1}' for i in range(7)],
#                  missing_values=[9999999.0],
#                  field_types=int,
#                  recode_fcns=[recode_fields14, recode_missing])
#
#     print('repr(csvt)= ', csvt)
#     for (n, row) in enumerate(csvt, start=1):
#         # if any(r_i is not None and (r_i <= 0 or r_i >= 5) for r_i in row):
#         if any(r_i is not None and (r_i > 5) for r_i in row):
#             print(f'row #{n} = {row}')
#         if n < 10:
#             print(f'row#{n} = {row}')
#
#     print(f'len(csvt)={len(csvt)}')
#     n_all_zero = sum(all(r_i == 0 for r_i in r)
#                      for r in csvt)
#     print(f'Number of all-zero records = {n_all_zero}')
#
