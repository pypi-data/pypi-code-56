# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 23:47:40 2019

@author: LIM YUAN QING
"""

import sys
import win32com.client
import struct
import pathlib
import logging
import os
import re
import signal
import platform
import pandas as pd
import cchardet
import zipfile
import io
import datetime
import subprocess
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from win32api import GetUserName
import inspect
import psutil

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from dd8 import get_basic_logger, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL, IS_PRODUCTION

#==================================================
#+                                                +
#+              Completed - Start                 +
#+                                                +
#==================================================

logger = get_basic_logger(__name__, LOG_PRINT_LEVEL, LOG_WRITE_LEVEL)

def dec_calculate_time(func):
    """
    Decorator to print time taken for a function to run.
    
    Parameters
    ----------
    func : function
        function object for which run time is to be determined
        
    Returns
    -------
    function
        original function logging added to log run time at debug logging level
    """
    def inner_func(*args, **kwargs):
        begin = datetime.datetime.now()
        output_to_return = func(*args, **kwargs)
        end = datetime.datetime.now()
        logger.debug(func.__name__ +  ' ran for ' + str(end-begin) + ' seconds.')
        return output_to_return
    return inner_func

def dec_conditional_decorator(decorator, bln_condition):
    """
    Decorator to conditionally decorate a function.
    
    Parameters
    ----------
    decorator : function
        decorator function object to be conditionally executed
    bln_condition : bool
        to determine if function should be decorated
        
    Returns
    -------
    function
        decorated function if `bln_condition` is `True`
    """
    def inner_decorator(func):
        if bln_condition:
            return decorator(func)
        else:
            return func        
    return inner_decorator

class TaskManager(object):
    def __init__(self):
        self.__msg = None
        self.__err = None
        self.tasks = None
        
        self.refresh()
        
    def refresh(self):
        try:
            self.__msg, self.__err = subprocess.Popen('tasklist', stdout=subprocess.PIPE).communicate()
            lst_output = []
            for line in self.__msg.split(b'\n'):
                lst_row = []
                for col in re.sub('\s\s+', ' ', line.decode('utf-8')).split():
                    str_col = col.strip()
                    lst_row.append(str_col)
                lst_output.append(lst_row)
                
            lst_output[1] = [str(lst_output[1][0]) + ' ' + str(lst_output[1][1]),
                              str(lst_output[1][2]),
                              str(lst_output[1][3]) + str(lst_output[1][4]),
                              str(lst_output[1][5]),
                              str(lst_output[1][6]) + str(lst_output[1][7])]
            
            i = 3
            for line in lst_output[3:-1]:
                lst_output[i] = lst_output[i][:-2] + [str(lst_output[i][-2]) + ' ' + str(lst_output[i][-1])]
                if len(lst_output[i])>5:
                    lst_output[i] =  [' '.join(lst_output[i][:-4])] + lst_output[i][-4:]
                i+=1
         
            df_output = pd.DataFrame(lst_output[3:-1], columns=lst_output[1])
            df_output.dropna(how='all', inplace=True)
            self.tasks = df_output            
            return True
        except:
            return False

    def get_tasks(self, bln_refresh = True):
        if bln_refresh:
            self.refresh()
        
        return self.tasks
    
    def kill_task_by_pid(self, pid, bln_forcefully=False):
        p = psutil.Process(pid)
        try:
            if bln_forcefully:
                p.kill()
#                os.kill(pid, signal.SIGKILL)
            else:
                p.terminate()
#                os.kill(pid, signal.SIGTERM)
            logger.info('Process {pid} successfully killed.'.format(pid=pid))
            return True
        except Exception as e:
            logger.error('Error occurred while killing process {pid} - {err_msg}'.format(pid=pid, err_msg=str(e)))
            return False
        
    def kill_task_by_name(self, name, bln_forcefully=False):
        
        if bln_forcefully:
            os.system('taskkill /F /IM {process_name}'.format(process_name=name))
        else:
            os.system('taskkill /IM {process_name}'.format(process_name=name))
        return True
    
    def get_pid_by_name(self, name, bln_refresh = True):
        if bln_refresh:
            self.refresh()
        return self.tasks[self.tasks['Image Name']==name]['PID'].tolist()
    
    def run_cmd(self, lst_cmd, bln_shell=False):
        proc = subprocess.Popen(lst_cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=bln_shell)
        output, error = proc.communicate()
        return output.decode('ascii'), error.decode('ascii')
        
    
                
class Folder():
    def __init__(self, str_full_folder_path):
        self.folder_path = str_full_folder_path.replace('/','\\')
        self.folder_exists = directory_exists(self.folder_path)
        if not self.folder_exists:
            logger.error(self.folder_path + ' does not exist.')     
    
    def __repr__(self):
        pass
    
    def __len__(self):
        pass
    
    def get_files(self, lst_file_extensions = None):
        __ = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(self.folder_path):
            for file in f:
                if lst_file_extensions:
                    if File(os.path.join(r, file)).get_file_extension() in lst_file_extensions:
                        __.append(os.path.join(r, file))
                else:
                    __.append(os.path.join(r, file))
        return __
    
    def get_sub_directories(self):
        __ = []

        # r=root, d=directories, f = files
        for r, d, f in os.walk(self.folder_path):
            for folder in d:
                __.append(os.path.join(r, folder))
        
        return __

class File(object):
    def __init__(self, str_file_path):
        self.file_path = str_file_path.replace('\\','/')
        self.file_exists = file_exists(self.file_path)
        self.__file_name_idx = self.file_path.rfind('/')
        self.__file_ext_idx = self.file_path.rfind('.')
        if not self.file_exists:
            logger.error(self.file_path + ' does not exist.')
            
    def __repr__(self):
        pass
    
    def __len__(self):
        pass
    
    def delete_file(self):
        try:
            if self.file_exists:
                os.remove(self.file_path)
                logger.debug(self.file_path + ' deleted.')
            else:                
                logger.debug(self.file_path + ' does not exist.')    
            
            return True
        except:
            logger.debug('Failed to delete ' + self.file_path)
            return False
    
    def file_exists(self):
        return self.file_exists
    
    def directory_exists(self):
        return directory_exists(self.get_file_directory())
    
    def get_file_extension(self):
        return self.file_path[self.__file_ext_idx:]
    
    def get_file_directory(self):
        return self.file_path[:self.__file_name_idx+1]
    
    def get_file_name(self):
        return self.file_path[self.__file_name_idx+1:self.__file_ext_idx]
    
    def get_file_size(self):
        return os.stat(self.file_path).st_size
    
    def get_creation_date(self, str_time_format='%Y-%m-%d %H:%M:%S'):
        return get_creation_date(self.file_path, str_time_format)
    
    def get_modified_date(self, str_time_format='%Y-%m-%d %H:%M:%S'):
        return get_modified_date(self.file_path, str_time_format)
    
    def rename(self, str_new_full_path):
        try:
            os.rename(self.file_path, str_new_full_path)
            return True
        except:
            return False

def file_exists(str_file_path):
    path = pathlib.Path(str_file_path)
    return path.is_file()

def directory_exists(str_directory_path):
    path = pathlib.Path(str_directory_path)
    return path.is_dir()

def find_file(str_file_name_with_ext,
              str_drive = ''):
    if not str_drive:
        __ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        drives = ['%s:' % d for d in __ if os.path.exists('%s:' % d)]
    else:
        drives = [str_drive]
        
    for drive in drives:
        for p, d, f in os.walk(os.path.join(drive, os.path.sep)):
            if str_file_name_with_ext in f:
                return os.path.normpath(os.path.join(p, str_file_name_with_ext))
    return None

def get_operating_system():
    return platform.system()

def get_modified_date(str_file_path, str_time_format=None):
    if str_time_format:
        return datetime.datetime.fromtimestamp(os.path.getmtime(str_file_path)).strftime(str_time_format)
    else:
        return datetime.datetime.fromtimestamp(os.path.getmtime(str_file_path))

def get_creation_date(str_file_path, str_time_format=None):
    '''
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    '''
    if get_operating_system() == 'Windows':
        __ = os.path.getctime(str_file_path)
    else:
        stat = os.stat(str_file_path)
        try:
            __ = stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            __ = stat.st_mtime
            
    if str_time_format:
        return datetime.datetime.fromtimestamp(__).strftime(str_time_format)
    else:
        return datetime.datetime.fromtimestamp(__)

@dec_conditional_decorator(dec_calculate_time, (not IS_PRODUCTION))
def get_dataframe_info(df_input):
    buf = io.StringIO()
    pd.DataFrame(df_input).info(buf=buf)
    
    info = buf.getvalue()
    info = [row.split() for row in info.split('\n') if row]
    count = float(info[1][1])
    
    
    info = info[3:-2]
    for i in range(len(info)):
        if len(info[i])>4: 
            info[i] = ['_'.join(info[i][:-3]), info[i][-3], info[i][-2], info[i][-1]]
    
    df_variables = pd.DataFrame(info, 
                                columns=['variable','non_null_count','non_null','data_type'])
    df_variables.set_index('variable', inplace=True)
    df_variables['missing_values_perc'] = (count - pd.to_numeric(df_variables['non_null_count']))/count
    
    return df_variables

class BasicObserver():
    
    def __init__(self, str_path_to_watch,
                   str_file_pattern_to_watch,
                   str_file_pattern_to_ignore,
                   bln_ignore_directories,
                   bln_case_sensitive,
                   bln_recursive,
                   fnc_on_created,
                   fnc_on_deleted,
                   fnc_on_modified,
                   fnc_on_moved):
        self.__event_handler = PatternMatchingEventHandler(str_file_pattern_to_watch,
                                                    str_file_pattern_to_ignore,
                                                    bln_ignore_directories,
                                                    bln_case_sensitive)
        self.__event_handler.on_created = fnc_on_created
        self.__event_handler.on_deleted = fnc_on_deleted
        self.__event_handler.on_modified = fnc_on_modified
        self.__event_handler.on_moved = fnc_on_moved
        
        self.__observer = Observer()
        self.__observer.schedule(self.__event_handler, str_path_to_watch,
                                 recursive = bln_recursive)

    def start(self):
        try:
            self.__observer.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.__observer.stop()
            self.__observer.join()
            sys.exit()
        
    def get_event_handler(self):
        return self.__event_handler
    
    def get_observer(self):
        return self.__observer  

def get_installed_distributions():
    try:
        from pip._internal.utils.misc import get_installed_distributions
    except ImportError:  # pip<10
        from pip import get_installed_distributions
    else:
        logger.debug('pip not found')

    return sorted(["%s==%s" % (i.key, i.version)
                   for i in get_installed_distributions()])

def get_mod_directory(str_mod_name=None):
    if not str_mod_name:
        str_mod_name = __file__
    return os.path.dirname(os.path.abspath(str_mod_name))

def get_zipfile_member_names(str_input_file_path):
    with zipfile.ZipFile(str_input_file_path, 'r') as f:
        return f.namelist()

def unzip_file(str_input_file_path, str_output_directory):
    obj_zip = zipfile.ZipFile(str_input_file_path, 'r')
    obj_zip.extractall(str_output_directory)
    obj_zip.close()
    return [str_output_directory + str_file_name 
            for str_file_name in get_zipfile_member_names(str_input_file_path)]

def get_user_name():
    return GetUserName()

def gen_date(str_start, 
             int_relative_days=0, 
             int_relative_months=0, 
             int_relative_years=0,
             bln_entire_series = False,
             str_format = '%Y%m%d',
             bln_excl_weekends=False,
             lst_excl_str_dates = None):
    
    def gen_weekend_offset(dte_input, bln_forward):
        int_weekday = dte_input.weekday()
        if int_weekday == 5:
            return bln_forward*2 + (not bln_forward)*1
        elif int_weekday == 6:
            return bln_forward*1 + (not bln_forward)*2
        else:
            return 1
    
    if type(str_start) == str:
        str_start = parse(str_start)
    
    if lst_excl_str_dates:
        lst_excl_str_dates = [parse(dte) for dte in lst_excl_str_dates 
                                  if type(dte)==str]
    else:
        lst_excl_str_dates = []
    
    new_date = str_start + relativedelta(years=int_relative_years, 
                                             months=int_relative_months, 
                                             days = int_relative_days) 
    if new_date >= str_start:
        bln_forward = True
    else:
        bln_forward = False
        
    if bln_excl_weekends:
        while (is_weekend(new_date) or (new_date in lst_excl_str_dates)):
            if bln_forward:
                new_date += relativedelta(days=gen_weekend_offset(new_date,True))                    
            else:
                new_date -= relativedelta(days=gen_weekend_offset(new_date,False))    
    else:
        while (new_date in lst_excl_str_dates):
            if bln_forward:
                new_date += relativedelta(days=1)
            else:
                new_date -= relativedelta(days=1)        
    
    if bln_entire_series:
        current_date = str_start
        output = [current_date.strftime(str_format)]
        while current_date != new_date:
            if bln_forward:
                current_date += relativedelta(days=1)
            else:
                current_date -= relativedelta(days=1)
            
            if bln_excl_weekends:
                while (is_weekend(current_date) or (current_date in lst_excl_str_dates)):
                    if bln_forward:
                        current_date += relativedelta(days=gen_weekend_offset(current_date,True))                    
                    else:
                        print(current_date)
                        current_date -= relativedelta(days=gen_weekend_offset(current_date,False))    
            else:
                while (current_date in lst_excl_str_dates):
                    if bln_forward:
                        current_date += relativedelta(days=1)
                    else:
                        current_date -= relativedelta(days=1)              
            output.append(current_date.strftime(str_format))
        
        return output
    else:
        return new_date.strftime(str_format)        
            

def is_weekend(dte_input):
    return (dte_input.weekday() == 5) or (dte_input.weekday() == 6)

def get_sys_bit():
    """
    Get system bits
    
    Returns
    -------
    integer
        number of bits
    """
    return 8 * struct.calcsize("P")

def is_32_bit():
    """
    Check if operating system is 32-bit
    
    Returns
    -------
    boolean
        True if operating system is 32-bit
    """
    return get_sys_bit() == 32

def is_64_bit():
    """
    Check if operating system is 64-bit
    
    Returns
    -------
    boolean
        True if operating system is 64-bit
    """
    return get_sys_bit() == 64
    
def is_date(str_date):
    """
    Check if string is date.
    
    Parameters
    ----------
    str_date : string
        string to check
    
    Returns
    -------
    boolean
        True if string is possibly a date
    """
    try:
        parse(str_date)
        return True
    except ValueError:
        return False
    
def merge_dicts(*args):
    """
    Merge n dictionaries.
    
    Parameters
    ----------
    *args : dictionary
        variable arguments of dictionary type to be merged into 1 dictionary
        
    Returns
    -------
    dictionary
        dictionary that is the result of merging input dictionaries
    """
    combined = dict()
    for dictionary in args:
        combined.update(dictionary)
    return combined

def get_filepaths(str_directory):
    return [str_directory + file for file in os.listdir(str_directory)]

def zip_file(str_zip_full_path, str_file_full_path):
    try:
        str_zip_full_path_new = str_zip_full_path + ('.zip' not in str_zip_full_path) * '.zip'
        obj_zipfile = zipfile.ZipFile(str_zip_full_path_new, 'a', zipfile.ZZIP_DEFLATED)
        obj_zipfile.write(str_file_full_path, str_file_full_path.split('\\')[-1])
        obj_zipfile.close()
        return True
    except:
        return False

def pandasDFToExcel(df, strFilePath, strSheet, blnHeader, blnIndex):
    """Saves Pandas dataframe to excel"""
    strFilePath = str(strFilePath)
    strSheet = str(strSheet)
    if os.path.exists(strFilePath):
        objExcel = win32com.client.DispatchEx('Excel.Application')
        objWb = objExcel.Workbooks.Open(Filename = strFilePath)
        objWb.Sheets(strSheet).Cells.ClearContents()
        objWb.Save()
        objExcel.Quit()
        del objExcel
        
    objExcel = pd.ExcelWriter(strFilePath)
    df.to_excel(objExcel, strSheet, header = blnHeader, index = blnIndex)
    objExcel.save()
    del objExcel

def in_str(strSubString, strFullString, blnCaseSensitive):
    if blnCaseSensitive:
        return (str(strSubString) in str(strFullString))
    else:
        return (str(strSubString).upper() in str(strFullString).upper())
    
def in_str_multi(lstSubStrings, strFullString, blnCaseSensitive):
    if blnCaseSensitive:
        return any(str(subString) in str(strFullString) for subString in lstSubStrings)
    else:
        return any(str(subString).upper() in str(strFullString).upper() for subString in lstSubStrings)
        
def is_numeric(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def fibonacci_number(n):
    dic = {}
    for i in range(1, n+1):
        if i == 1 or i ==2:
            dic[i] = 1
        else:
            dic[i] = dic[i-1] + dic[i-2]
            
    return dic[n]

def convert_encoding(data, newCoding = 'UTF-8'):
    encoding = cchardet.detect(data)['encoding']
    if newCoding.upper() != encoding.upper():
        data = data.decode(encoding, data).encode(newCoding)
        
    return data

#==================================================
#+                                                +
#+              Completed - End                   +
#+                                                +
#==================================================

class FunctionInspection(object):
    def __init__(self, function):
        self.function = function
        self.signature = self.get_signature()
        
    def get_signature(self):
        return inspect.signature(self.function)
    
    def get_kwargs(self):
        return [kwa.split('=')[0] for kwa in tuple(self.get_signature()) if '=' in kwa]


class HTMLDocument(object):
    def __init__(self, html_lang='en',
                 html_dir='ltr',
                 meta_charset='utf-8'):
        pass
    
    
    def add_to_head(self, str_name, str_html):
        pass
    
    def add_to_body(self, str_name, str_html):
        pass
    
    def remove_from_head(self, str_name):
        pass
    
    def remove_from_body(self, str_name):
        pass
    

def gen_plural(str_word, int_count=2):
    if int_count>1:
        last_alpha = str_word[-1]
        if last_alpha == 'y':
            return str_word[:-1] + 'ies'
        elif last_alpha == 'f':
            return str_word[:-1] + 'ves'
        else:
            return str_word + 's'
    else:
        return str_word


def export_dataframe_to_csv(df, int_num_rows_per_file, str_path, suffix='_',
                            **kwargs):
    file = File(str_path)
    counter = 1
    start = 0
    end = start + int_num_rows_per_file
    lst_file_paths = []
    while start < df.shape[0]:
        str_file_path = (file.get_file_directory() + file.get_file_name() +
                                   suffix + '{count}' + file.get_file_extension()).format(count=counter)
        df.iloc[start:end].to_csv(str_file_path, **kwargs)
        lst_file_paths.append(str_file_path)
        start += int_num_rows_per_file
        end = min(df.shape[0], start+int_num_rows_per_file)
        counter += 1
    return lst_file_paths

def execute_cmd(lst_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True):
    proc = subprocess.Popen(lst_command, stdout=stdout, stderr=stderr, shell=shell)
    o, e = proc.communicate()
    return (o.decode('ascii'), e.decode('ascii'), str(proc.returncode), str(proc.pid))




if __name__ == '__main__':
    # test gen_date
    print(gen_date(str_start='13 Jun 2019', 
                   int_relative_days=0, 
                   bln_excl_weekends=True,
                   bln_entire_series=False,
                   lst_excl_str_dates=['10 Jun 2019']))