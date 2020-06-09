"""Interface to read Item Response Data stored in an SPSS (.sav) file.
NOT RECOMMENDED, better to use SPSS to export file in another format

*** MAIN CLASS:
Table --- iterable interface to an SPSS file,
    accessing fields by their names as used in the database.

*** NOTE: MacOS savReaderWriter needs user-assigned Region and Preferred Language
in System Preferences to match an existing locale setting.
Otherwise,
locale.setlocale(locale.LC_ALL, '') will raise an exception
when savReaderWriter tries to open and/or close an SPSS file.
"""
# *********************** check savReader.close locale again ******************

import savReaderWriter
# ***** NOTE symbolic links in /usr/local/lib are NEEDED,
# not correctly installed by PIP package installer

from . import table_reader


# -----------------------------------------------------------------
class Table(table_reader.Table):
    """Reader for tabular data stored in SPSS file,
    using package savReaderWriter
    """
    # superclass __init__ is sufficient, no new parameters

    # def get_header(self):
    #     """Connect to the file and read file header
    #     :return: list with header name strings from the file
    #     """
    #     with self.open_reader(return_header=True) as spss_reader:
    #         return spss_reader.next()
    #
    # def open_reader(self, return_header=False):
    #     """Open file for read-only access.
    #     :param return_header: boolean
    #     :return: iterator object over file rows,
    #         typically used in a with statement.
    #         The reader.next() method yields each row as stored in the file
    #         without any type cast or other checks
    #     """
    #     return savReaderWriter.SavReader(self.file_path,
    #                                      returnHeader=return_header,
    #                                      selectVars=self.fields,
    #                                      ioUtf8=True)

    def __iter__(self):
        """Generator of rows for read-only access.
        :return: iterator object over file rows, except header
        """
        with savReaderWriter.SavReader(self.table_id,
                                       returnHeader=False,
                                       selectVars=self.fields,
                                       ioUtf8=True) as reader:
            for (row_n, row) in enumerate(reader):
                if row_n % self.sample_factor == 0:
                    row = self.process_row(row)
                    if row is not None:
                        yield row

    def preview(self, max_records=10):
        """Generator of rows for read-only access.
        :return: iterator object over file rows, except header
        """
        # result = []
        with savReaderWriter.SavReader(self.table_id,
                                       returnHeader=True,
                                       # selectVars=self.fields,
                                       ioUtf8=True) as reader:
            for (row_n, row) in enumerate(reader):
                if row_n > max_records:
                    break
                yield row
        # return result


# -----------------------------------------------------------------------------
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
#     kramer_file = ioiha_kramer / 'NLSH-Kramer-T2IOI-HA.sav'
#
#     # help(savReaderWriter.SavReader)
#
#     with savReaderWriter.SavReader(kramer_file, returnHeader=True,
#                                    # rawMode=True,
#                                    # selectVars=['ioi_v1', 'ioi_v2'],
#                                    ioUtf8=True) as reader:
#         header = reader.next()
#         print('header= ', header)
#         for (n, line) in enumerate(reader):
#             print(line)
#             if n > 10:
#                 break
#
#     # spss = Table(kramer_file)
#     # print('spss.header = ', spss.header)
#     #
#     # data = spss.preview(10)
#     # print('spss.preview(10) =\n', data)
#
#     # -------------------------------- test with missing-values recoding:
#     spss = Table(kramer_file,
#                  # fields=['ioi_v1', 'ioi_v2', 'ioi_v3'],
#                  fields=[f'T2IOIHA{i+1}' for i in range(7)],
#                  missing_values=[9999999.0],
#                  field_types=str)
#     print('repr(spss)= ', spss)
#
#     for (n, row) in enumerate(spss, start=1):
#         if n > 10:
#             break
#         print(f'row #{n} = {row}')
#
#     print('\n *** spss.preview(10)=\n', spss.preview(10))
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
#     spss = Table(kramer_file,
#                  # fields=['ioi_v1', 'ioi_v2', 'ioi_v3'],
#                  fields=[f'T2IOIHA{i+1}' for i in range(7)],
#                  missing_values=[9999999.0],
#                  field_types=int,
#                  recode_fcns=[recode_fields14, recode_missing])
#     for (n, row) in enumerate(spss, start=1):
#         # if any(r_i is not None and (r_i <= 0 or r_i >= 5) for r_i in row):
#         if any(r_i is not None and (r_i > 5) for r_i in row):
#             print(f'row #{n} = {row}')
#
#     print(f'len(spss)={len(spss)}')
#     n_all_zero = sum(all(r_i == 0 for r_i in r)
#                      for r in spss)
#     print(f'Number of all-zero records = {n_all_zero}')
#
