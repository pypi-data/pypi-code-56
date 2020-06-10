EXCEL_TYPE = ['.xls', '.xlsx', '.xlsm']
TXT_TYPE = ['.txt', '.csv']
__version__ = '1.0.3'

from .filetransform import (excel_to_csv, csv_to_excel, excel_to_csv_in_list,
                            csv_to_excel_in_list, csv_to_excel_in_path, excel_to_csv_in_path)
from .filesplit import (split_file, mml_split_file, split_by_column, split_by_row, split_by_size)
from .fileunion import (union_in_path_to_csv, union_in_list_to_csv, union_sheets_to_csv, union_file,
                        union_in_path_to_sheets, union_in_list_to_sheets)
from .parser import union_file, split_file, transform_file
