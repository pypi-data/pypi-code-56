import time
import logging
import threading
import yaml
from xlsxhelper import get_worksheet, get_cells
from .browser import Browser

CMD_STARTING_ROW = 5

logger = logging.getLogger(__name__)


def run_xlsx_config(config_xlsx_path, sheet=None, variables_xlsx_path=None, variables_sheet=None, instance_start_delay=5):
    worksheet = get_worksheet(config_xlsx_path, sheet)
    xlsxdata = get_cells(worksheet, only_data=True)
    config = {}
    config["webdriver"] = xlsxdata[1][1]
    config["width"] = xlsxdata[2][1]
    config["height"] = xlsxdata[3][1]
    config["commands"] = xlsxdata[CMD_STARTING_ROW:]
    if variables_xlsx_path:
        variables = []
        variables_worksheet = get_worksheet(variables_xlsx_path, variables_sheet)
        variables_table = get_cells(variables_worksheet, only_data=True)
        header = variables_table[0]
        for row_index in range(1, len(variables_table)):
            row = {}
            for col_index in range(len(variables_table[row_index])):
                row[header[col_index]] = variables_table[row_index][col_index]
            variables.append(row)
    else:
        variables = []
    if len(variables) > 1:
        browsers = []
        threads = []
        for context in variables:
            browser = Browser(config)
            thread = threading.Thread(target=browser.run, args=[context])
            thread.setDaemon(True)
            thread.start()
            browsers.append(browser)
            threads.append(thread)
            time.sleep(instance_start_delay)
        for thread in threads:
            thread.join()
    else:
        browser = Browser(config)
        browser.run(variables[0])
