"""This module defines help classes to access responses to questionnaire items.
Data may be stored in various file formats.

*** Class Overview:

ItemResponseDataSet: container for all response data for selected group(s),
    to be used as input for statistical analysis.
    Response data input must be an iterable over response records.
    A Response Record is a 1D list with integer-coded responses from ONE subject,
    with one ordinal integer value for each Questionnaire Item.
    The input data for one group may be
    1) a single list of subject response lists,
    2) a single table_reader.Table instance, reading from one data file,
    3) a single table_reader.Tables instance, chaining input from several iterable objects.

Questionnaire: description of a questionnaire, usually with several items

Item: description of a single item (question and answer alternatives)

*** Main File Interface Function:

item_response_table: general function interface to ONE data file in any allowed format

*** Input File Formats:

xlsx: Data can be imported from Excel workbook (xlsx) files,
    with data stored in ONE worksheet.
    Item response data are stored in specified columns,
    as defined by keyword parameter 'fields' to the Table reader class.
    See module table_reader_xlsx for details.

sql: Data can be imported from sql database files.
    Item response data are stored in specified database fields,
    as defined by keyword parameter 'fields' to the Table reader class.
    See module table_reader_sql for details.
    (table_reader_sqlite3 is no longer used.)

csv: Data can be imported from a csv text file.
    Item response data are stored in specified columns,
    identified by 'fields' string labels in the first line of the file.
    See module table_reader_csv for details.

spss: Data can be imported from an SSPS (.sav) file.
    See module table_reader_spss for details.
    However, SSPS reader might not work with newer python versions.
    May be easier to first convert the file to .csv format


*** Usage Example:

q_file = string or Path identifying questionnaire text (utf8) file
r_file = string or Path identifying response file

group0_file = item_response_table(r_file1, fmt='xlsx')
group1A_file = item_response_table(r_file1A, ...)  another data file
group1B_file = item_response_table(r_file1B, ...)  another data file
etc.

ids = ItemResponseDataSet.load(questionnaire=Questionnaire.load(q_file),
        groups={'Group0': group0_file,
                'Group1': Tables(group1A_file, group1B_file,...)
                }
        )

This data-set can then be used as input to create an analysis model, e.g.,
irm = OrdinalItemResponseModel.initialize(ids, n_traits=3)
irm.learn()
See run_irt.py for a complete example.

*** Version History:

2019-07-23, functional version, may need some cleanup
2019-07-29, new version with general table_reader interface
2019-08-25, minor cleanup
"""
# **** How to handle duplicate subjectID ??? ********

import numpy as np
from pathlib import Path

import logging
from importlib import import_module
from itertools import chain

ircPackage = 'ItemResponseCalc.'
# = top ref to sub-modules for selective imports

STORAGE_FMT = {'sqlite3': ircPackage + 'table_reader_sqlite',
               'sql': ircPackage + 'table_reader_sql',
               'xlsx': ircPackage + 'table_reader_xlsx',
               'spss': ircPackage + 'table_reader_spss',
               'sav': ircPackage + 'table_reader_spss',
               'csv': ircPackage + 'table_reader_csv'
               }
# = mapping of file format code to suitable table_reader module
# to be imported only if actually needed

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------
class Item:
    """Information describing ONE questionnaire item.
    """
    def __init__(self, question, responses, reverse=False):
        """
        :param question: string with explicit question text
        :param responses: list of strings, one for each possible response
        :param reverse: boolean = True if responses should be indexed in reverse order
            NOTE: Response data files may or may not already have recoded
            the responses by ordinal indices in the desired analysis order.
        """
        self.question = question
        self.responses = responses
        self.reverse = reverse

    def __repr__(self):
        return (self.__class__.__name__ + '(\n\t'
                + ',\n\t'.join((f'{k}={repr(v)}' for (k,v) in self.__dict__.items()))
                + ')')

    @property
    def n_response_levels(self):
        return len(self.responses)


class Questionnaire:
    """Container for a questionnaire with several items,
    required to specify number of items and number of response levels for each item,
    even if the actual questions and response alternatives are not included.
    """
    def __init__(self, header=None, items=None, item_response_levels=None):
        """
        :param header: (optional) string describing the questionnaire
        :param items: (optional) list of Item instances
        :param item_response_levels: (optional) necessary only if items is None:
            list with
            item_response_levels[i] = integer number of response levels for i-th item
        """
        self.header = header
        self.items = items
        if items is None:
            self.item_response_levels = item_response_levels
        else:
            self.item_response_levels = [i.n_response_levels for i in self.items]

    def __repr__(self):
        return (self.__class__.__name__ + '(\n\t'
                + ',\n\t'.join((f'{k}={repr(v)}' for (k,v) in self.__dict__.items()))
                + '\n\t)')

    @property
    def n_items(self):
        return len(self.item_response_levels)

    @classmethod
    def load(cls, file, sep='\t'):
        """Read questions and answers from given file
        :param file: string or Path object identifying input file
        :param sep: (optional) string, separator between response alternatives
        :return: cls instance
        """
        strip = ' \n'  # chars to strip away from end of input lines
        with Path(file).open('rt', encoding='utf8') as f:  # *********** other txt encodings ??? *****
            header = f.readline()
            items = []
            while True:
                q = f.readline()
                a = f.readline()
                reverse = f.readline()
                if a == '':
                    break  # even if q is non-empty
                else:
                    items.append(Item(question=q.rstrip(strip),
                                      responses=(a.rstrip(strip)).split(sep),
                                      reverse='rev' in reverse))
        return cls(header.rstrip(strip), items)


# ------------------------------------------------------------
class ItemResponseDataSet:
    """All result data for one complete item response analysis,
    including one or several groups of subjects.
    There should be at least one group with complete individual response data,
    otherwise the analysis cannot reveal correlations between items.
    """
    def __init__(self, questionnaire, groups):
        """
        :param questionnaire: single Questionnaire object
        :param groups: dict with elements (g_name, g_subjects), where
            g_name = string identifying the group
            g_subjects = iterable, e.g., a list or responses or an instance of a table_reader.Table subclass,
                yielding a sequence of subject response_records, one for each subject.
                response_record = a 1D list with
                response_record[i] = integer ordinal index of response to i-th item
                encoded with origin == 1.
                NOTE: different from python index origin!
                Missing responses MUST be indicated as 0.
                The Table object can apply user-supplied recoding functions,
                in case other response encodings are used in the file.
        """
        assert questionnaire is not None, 'Must have a Questionnaire object'
        self.questionnaire = questionnaire
        if groups is None:
            groups = dict()
        self.groups = groups

    def __repr__(self):
        return (self.__class__.__name__ + '('
                + f'\n\t questionnaire= {self.questionnaire.__class__.__name__} '
                + f'object with {self.questionnaire.n_items} items,'
                + '\n\t groups= {\n\t\t'
                + ',\n\t\t'.join(f'{g_key}: {g.__class__.__name__} with about {len(g)} rows'
                                 for (g_key, g) in self.groups.items()) + '}'
                + ')')

    @property
    def n_response_levels(self):
        return self.questionnaire.item_response_levels

    @property
    def n_items(self):
        return len(self.n_response_levels)

    @property
    def n_groups(self):
        return len(self.groups)

    @property
    def item_response_count(self):
        """Total number of response counts for each item,
        summed across all groups.
        :return: c = list of response count arrays, with
            c[i] = 1D array for i-th item,
            with responses encoded with origin == 0, i.e.,
            c[i][l] = count of response == l+1 for this item
        """
        c = [np.zeros(n_i, dtype=int) for n_i in self.n_response_levels]
        # counter, NOT including space for missing response coded as zero
        for (g_key, g_response) in self.groups.items():
            # g_response is iterable of item-response vectors, one for each subject,
            # with responses encoded with origin == 1 for the lowest ordinal response alternative
            for r_s in g_response:
                for (item, r_si) in enumerate(r_s):
                    if 1 <= r_si <= len(c[item]):  # i.e., real non-missing response
                        c[item][r_si - 1] += 1  # count first response alternative at index == 0
                    elif r_si > len(c[item]):
                        logger.warning(f'Group {repr(g_key)}: Response={r_si} for item {item} out of range')
                    # else just a missing data value, not counted
        return c


# ---------------------------------------------- File Interface factory:
def item_response_table(file_path, fmt=None, **kwargs):
    """Create interface to input file with individual item response data.
    :param file_path: Path or string identifying input file
    :param fmt: (optional) file format code, if not defined by file suffix
    :param kwargs: keyword arguments to table_reader.Table of selected format
    :return: a Table object representing the given file,
        which can be used as an iterator yielding subject response records.
    """
    file_path = Path(file_path)
    assert file_path.exists(), f'{file_path.name} not found'
    assert file_path.is_file(), f'{file_path.name} is not a file'
    if fmt is None:
        fmt = file_path.suffix[1:]
    if fmt in STORAGE_FMT:
        m = import_module(STORAGE_FMT[fmt])
        return m.Table(file_path, **kwargs)
    else:
        raise RuntimeError(f'Unknown file format: {repr(fmt)}')


# -------------------------------------------------------- Module TEST:
# if __name__ == '__main__':
#
#     def recode_missing_as_0(row):
#         for i in range(len(row)):
#             if row[i] is None:
#                 row[i] = 0
#     # --------------------------------------------
#
#     HAQ_PATH = Path.home() / 'Documents/LeijonKTH/heartech/HA-QualityRegistry/IRT-IOI-HA/IOI-HA-Data'
#     # ioiha_data_path = HAQ_PATH / 'IRT-IOI-HA' / 'IOI-HA-data'
#     # to ioi-ha data sets OTHER THAN the Swedish Quality Registry
#
#     print('*** Test Load Questionnaire:\n')
#     q = Questionnaire.load(HAQ_PATH / 'IOI-HA-English.txt')
#     print(q)
#     # ------------------------------------------------------------------
#
#     print('\n*** Testing table_reader_xlsx with Hickson data set:\n')
#
#     test_file = HAQ_PATH / 'Hickson' / 'Short_Eartrak AUS.xlsx'
#
#     irf = item_response_table(test_file,
#                               fields=[f'Q0{i}' for i in range(1, 8)],
#                               field_types=int,
#                               header_row=1,
#                               missing_values=['.', ' '])
#     print('printing a few records:')
#     for (i,r) in enumerate(irf):
#         print(r)
#         if i > 10:
#             break
#     print('printing first few records again:')
#     for (i,r) in enumerate(irf):
#         print(r)
#         if i > 5:
#             break
#
#     all_r = [r for r in irf]
#     print('number of records=', len(all_r))
#     print(f'len(irf) = ', len(irf))
#
#     # check subject duplicates:
#     irs = item_response_table(test_file,
#                               fields=['A'],
#                               header_row=0)
#     subjects = set()
#     dupl_subjects = set()
#     dupl_records = []
#     for (i,r) in enumerate(irs):
#         if r[0] in subjects:
#             print(f'Duplicate subject ID={repr(r[0])} found in row {i+2}')
#             dupl_subjects.add(r[0])
#             dupl_records.append(i)
#         else:
#             subjects.add(r[0])
#     print(f'Found {len(subjects)} unique subject IDs')
#     print(f'Found {len(dupl_subjects)} duplicate subject IDs in {len(dupl_records)} records')
#     print(dupl_subjects)
#
#     # ----------------------------------------- Use Hickson xlsx in data set:
#     print('\n*** Testing usin Hickson file in an ItemResponseDataSet object:\n')
#
#     irf = item_response_table(test_file,
#                               fields=[f'Q0{i}' for i in range(1, 8)],
#                               field_types=int,
#                               header_row=1,
#                               missing_values=['.', ' '],
#                               recode_fcns=recode_missing_as_0)
#
#     ids = ItemResponseDataSet(questionnaire=Questionnaire(item_response_levels=[5,5,5,5,5,5,5]),
#                               groups={'HicksonEarTrak': irf})
#
#     print(ids)
#     print('response_count=\n', ids.item_response_count)
#     print('total counts: ', [np.sum(c_i) for c_i in ids.item_response_count])
#
#     # ----------------------------------------- test Kramer SPSS data set:
#
#     print('\n*** Testing table_reader_spss with Kramer data set:\n')
#
#     kramer_file = item_response_table(file_path=HAQ_PATH / 'Kramer' / 'moeder_final - kopieforArne.sav',
#                                       fmt='spss',
#                                       fields=[f'ioi_v{i}' for i in range(1, 8)],
#                                       field_types=int,
#                                       missing_values=[9.0],
#                                       recode_fcns=recode_missing_as_0)
#
#     print(f'Using kramer_file with {len(kramer_file)} records')
#     print('printing a few records:')
#     for (i, r) in enumerate(kramer_file):
#         if i > 10:
#             break
#         print(r)
#
#     kramer_file2 = item_response_table(file_path=HAQ_PATH / 'Kramer' / 'NLSH-Kramer-T2IOI-HA.sav',
#                                        fmt='spss',
#                                        fields=[f'ioi_v{i}' for i in range(1, 8)],
#                                        field_types=int,
#                                        missing_values=[9.0],
#                                        recode_fcns=recode_missing_as_0)
#
#     print(f'Using kramer_file with {len(kramer_file2)} records')
#     print('printing a few records:')
#     for (i, r) in enumerate(kramer_file2):
#         if i > 10:
#             break
#         print(r)
#
#     ids = ItemResponseDataSet(questionnaire=Questionnaire(item_response_levels=[5,5,5,5,5,5,5]),
#                               groups={'Kramer': kramer_file})
#
#     print(ids)
#     print('response_count=\n', ids.item_response_count)
#     print('total counts: ', [np.sum(c_i) for c_i in ids.item_response_count])
#
#
# # ------------------------------------------------------- Check using Swedish data set:
#     print('\n*** Testing table_reader_sqlite with haq data set:\n')
#
#     def accept_record(r):
#         """Inclusion_crit for accepting a record
#         :param r: dict with all record fields
#         :param f: list of record field keys to be used
#         :return: boolean == True if record is acceptable
#         """
#         n_missing = sum(r_i is None for r_i in r)
#         within_range = all((r_i is None) or 1 <= r_i <= 5
#                            for r_i in r)
#         return n_missing <= 3 and within_range
#     # -------------------------------------------------------------------
#
#     HAQ_PATH = Path.home() / 'Documents/LeijonKTH/heartech/HA-QualityRegistry/ircData'
#     db_file = str(HAQ_PATH / 'development.sqlite3')
#
#     SELECT_FROM = ("prescriptions where " +
#                     "Respondent = 't' " +
#                     "AND article_company IS NOT NULL " +
#                     "AND date >= '2016-01-01' AND date <= '2016-01-30' "
#                    )
#
#     haq = item_response_table(file_path=db_file,
#                               select_from=SELECT_FROM,
#                               fields=[f'Q{i}' for i in np.arange(3,10)],
#                               accept_row=accept_record,
#                               recode_fcns=recode_missing_as_0)
#     # *** missing data is already coded as 0
#
#     print(f'len(haq) = ', len(haq))
#     print('*** First few records selected for analysis:')
#     n_rec = 10
#     for r in haq:
#         print(r)
#         n_rec -= 1
#         if n_rec <= 0:
#             break
#
#     print('\n*** Testing ItemResponseDataSet with sqlite dataset:\n')
#     ids = ItemResponseDataSet(questionnaire=Questionnaire(item_response_levels=[5,5,5,5,5,5,5]),
#                               groups={'HAQregistry': haq})
#
#     print(ids)
#
#     print('response_count=\n', ids.item_response_count)
#     print('total counts: ', [np.sum(c_i) for c_i in ids.item_response_count])
#
#     # -------------------------------------------------------------------
#     print('\n*** Testing ItemResponseDataSet with three sources:\n')
#
#     ids3 = ItemResponseDataSet(questionnaire=Questionnaire(item_response_levels=[5,5,5,5,5,5,5]),
#                                groups={'AU': irf,
#                                                   'NL': kramer_file,
#                                                   'SE': haq})
#
#     print(ids3)
#
#     print('response_count=\n', ids3.item_response_count)
#     print('total counts: ', [np.sum(c_i) for c_i in ids3.item_response_count])

# ------------------------------------------- plot response distributions
