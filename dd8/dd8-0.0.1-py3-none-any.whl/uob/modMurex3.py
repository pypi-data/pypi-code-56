# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 08:15:17 2019

@author: yuanq
"""

import sys
import pandas as pd
import csv
import dateutil
import xml.etree.ElementTree as ET
import time

import dd_package.modGlobal3 as glob
import dd_package.mmodUtils3 as utils

import dd8

logger = utils.get_basic_logger(__name__, dd8.LOG_PRINT_LEVEL, dd8.LOG_WRITE_LEVEL)

str_mx_inputs_path = glob.MX_INPUTS_PATH
viewer_mapping = pd.read_csv(str_mx_inputs_path + 'layout_mapping.csv')
dic_mx_headers = {header:viewer_mapping[header].dropna().tolist() 
                    for header in viewer_mapping.columns}



class MxScript(object):
    def __init__(self, lst_xml_full_paths,
                 str_read_client_full_path=''):
        self.xml_paths = []
        self.read_client = None
        
        if type(lst_xml_full_paths) != list:
            if type(lst_xml_full_paths) == str:
                self.xml_paths = [lst_xml_full_paths]
        else:
            self.xml_paths = lst_xml_full_paths
            
        if self.xml_paths:
            if str_read_client_full_path:
                self.read_client = str_read_client_full_path
            else:
                if len(self.xml_paths) == 1:
                    self.read_client = glob.MX_READ_CLIENT
                else:
                    self.read_client = glob.MX_PARALLEL_READ_CLIENT
                    
    def run(self):
        client = utils.File(self.read_client)
        client = client.get_file_directory().replace('/', '\\')
        
        cmds = []
        cmd = [self.read_client.replace('/','\\')]
        counter = 1
        for script in self.xml_paths:
            if counter > 6:
                cmds.append(cmd)
                cmd = [self.read_client.replace('/','\\')]
                counter = 1
            cmd.append('/MXJ_SCRIPT_READ_FROM:' + script.replace('/','\\'))
            counter += 1
        cmds.append(cmd)
        
        output = []           
        tm = utils.TaskManager()
        for cmd in cmds:                
            pid = set(tm.get_pid_by_name('javaw.exe'))
            proc = utils.subprocess.Popen(cmd, shell=True, cwd=client)
            o, e = proc.communicate()
            pid = set(tm.get_pid_by_name('javaw.exe')) - pid
            output.append((pid,o,e))
            time.sleep(10)
        
        return output

class MxLayout(object):
    def __init__(self, str_zip_path):
        self.__str_zip_path = str_zip_path
        str_datetime = self.__str_zip_path.split('/')[-1].split('.')[0]
        str_datetime = str_datetime.replace(' -', '').replace('_', ':')
        self.__dte_creation = dateutil.parser.parse(str_datetime)
        self.__lst_viewers = []
        self.__bln_mds_viewer_exists = False
        self.__df_market_data_set = None
        
    def add_viewer(self, obj_mx_viewer):
        self.__lst_viewers.append(obj_mx_viewer)
        
    def unzip_layout(self, str_destination_folder_path, 
                     bln_keep_zip_file=False):
        files = utils.unzip_file(self.__str_zip_path, str_destination_folder_path)
        for file in files:
            viewer = MxViewer(file)
            self.__lst_viewers.append(viewer)
            if viewer.get_name() == 'MARKET_DATA_SET':
                self.__bln_mds_viewer_exists = True
                self.__df_market_data_set = viewer.get_data()
        return self.__lst_viewers
    
    def get_path(self):
        return self.__str_zip_path

    def get_creation_datetime(self):
        return self.__dte_creation
    
    def get_viewers(self):
        return self.__lst_viewers
    
    def mds_viewer_exists(self):
        return self.__bln_mds_viewer_exists
    
    def get_market_data_set(self):
        pass
    
    def get_portfolios(self):
        pass
    
    def get_simulation_date(self):
        pass
    
    

class MxViewer(object):
    def __init__(self, str_csv_path=None):
        self.__str_csv_path = str_csv_path
        self.__obj_file = utils.File(self.__str_csv_path)
        self.__str_csv_name = self.__obj_file.get_file_name()
        self.__df_data = None
        self.__str_viewer_name = None
        if self.__obj_file.file_exists:
            logger.debug(self.__str_csv_path + ' found.')
            if self.__obj_file.get_file_size() != 0:
                with open(self.__str_csv_path, 'rt') as f:
                    reader = csv.reader(f)
                    self.__lst_header = next(reader)
                    
                self.__lst_header = [col.strip().replace('\ufeff', '') 
                                        for col in self.__lst_header[0].split(';')]
                self.__str_viewer_name = self.match_header(self.__lst_header)
                __ = 'MxViewer object successfully instantiated...\n'
                __ += 'viewer name: ' + str(self.__str_viewer_name) + '\n'
                __ += 'file path: ' + self.__str_csv_path + '\n'
                logger.info(__)
            else:
                logger.error(self.__str_csv_path + ' has 0 file size.')
        else:
            logger.error(self.__str_csv_path + ' does not exist.')
        
    def match_header(self, lst_header):
        for key, value in dic_mx_headers.items():
            if set(lst_header) == set(value):
                self.__str_viewer_name = key
                logger.debug('viewer found - ' + self.__str_viewer_name)
                return self.__str_viewer_name
        logger.debug('no viewer found for header: ' + str(lst_header))
        return None
    
    def get_name(self):
        return self.__str_viewer_name
    
    def get_data(self):
        self.__df_data = pd.read_csv(self.__obj_file.file_path, delimiter=';')
        self.__df_data.columns = self.__lst_header
        self.prepare_data()
        return self.__df_data
    
    def get_path(self):
        return self.__str_csv_path
    
    def store_data(self):
        pass
    
    def prepare_data(self):
        if self.__str_viewer_name != None:
            if self.__str_viewer_name == 'BUCKETED_VEGA':
                self.__df_data.columns = self.__df_data.iloc[0]
                self.__df_data.drop(0, inplace=True)
                self.__df_data.reset_index(inplace=True, drop=True)
                self.__df_data.rename(columns={'Maturity Set/ Total Vega<SGD>': 'Total'},
                                      inplace=True)
                self.__df_data.columns = [name.strip().upper() for name in self.__df_data.columns]
                self.__df_data['BBG CODE'] = self.__df_data['BBG CODE'].str.upper()
                self.__df_data.set_index('BBG CODE', inplace=True)
            elif self.__str_viewer_name == 'PL_SUMMARY':
                pass
            elif self.__str_viewer_name == 'PL_SUMMARY_FX':
                pass
            elif self.__str_viewer_name == 'CASHFLOW':
                self.__df_data.columns = self.__df_data.iloc[0]
                self.__df_data = self.__df_data.iloc[1:]
            else:
                self.__str_viewer_name = None
        else:
            logger.error('Please set up viewer...')



class MxMXML(object):
    def __init__(self):
        self.xml = ET.Element('MXClientScript')
        
    def gen_login_info(self, str_user_name=None,
                       str_password=None,
                       str_group_name=None,
                       str_group_type=None,
                       str_platform_name=None,
                       str_nickname=None,
                       str_direct_access=None,
                       str_mx_command=None):
        if not str_user_name:
            str_user_name = glob.MX_LOGIN_YQ
            
        if not str_password:
            str_password = glob.MX_PW_YQ
            
        if not str_group_name:
            str_group_name = glob.MX_EQWR_GROUP_NAME
            
        if not str_group_type:
            str_group_type = glob.MX_GROUP_TYPE
            
        if not str_platform_name:
            str_platform_name = glob.MX_PLATFORM_NAME
            
        if not str_nickname:
            str_nickname = glob.MX_NICKNAME
            
        if not str_direct_access:
            str_direct_access = glob.MX_SIM_BY_TRADE
            
        if str_direct_access == 'Portfolio simulation by trade\\':
            command_code = glob.MX_DIRECT_ACCESS_CODE_BY_TRADE
        elif str_direct_access == 'Porfolio simulation by position\\':
            command_code = glob.MX_DIRECT_ACCESS_CODE_BY_POS
            
        xml_login = ET.SubElement(self.xml, 'LoginInfo')
        
        str_output = '''<LoginInfo>
                            <UserName>{username}</UserName>
                            <Password>{password}</Password>
                            <GroupName>{group_name}</GroupName>
                            <GroupType>{group_type}</GroupType>
                            <PlatformName>{platform_name}</PlatformName>
                            <NickName>{nickname}</NickName>
                            <DirectAccess Code="COMMAND_{code}">{direct_access}</DirectAccess>
                            <MXCommand>{mx_command}</MXCommand>
                        </LoginInfo>
                    '''.format(username=str_user_name,
                    password=str_password,
                    group_name=str_group_name,
                    group_type=str_group_type,
                    platform_name=str_platform_name,
                    nickname=str_nickname,
                    code=command_code,
                    direct_access=str_direct_access,
                    mx_command=str_mx_command)
        self.__lst_output.append(str_output)
        return str_output
    
    def gen_xml_file(self, folder_path):
        pass
    
def get_murex_viewer(str_viewer_name,
                     str_date=None,
                     str_inputs_path=glob.MX_INPUTS_PATH):
    logger.info('get_murex_viewer called: viewer_name={viewer_name}, date={date}, \
                inputs_path={inputs_path}'.format(viewer_name=str_viewer_name, 
                date=str_date, inputs_path=str_inputs_path))
    
    folder = utils.Folder(str_inputs_path)
    lst_file_paths = folder.get_files()
    lst_file = []
    
    try:
        for path in lst_file_paths:
            if '.csv' in path:
                f = utils.File(path)
                if str_date:
                    if (f.get_creation_date().date() == utils.parse(str_date).date()):
                        viewer=MxViewer(path)
                        if viewer.get_name() == str_viewer_name:
                            if lst_file:
                                if f.get_creation_date() > lst_file[0]:
                                    lst_file[0] = f.get_creation_date()
                                    lst_file[1] = viewer
                            else:
                                lst_file.append(f.get_creation_date())
                                lst_file.append(viewer)
                else:
                    viewer=MxViewer(path)
                    if viewer.get_name() == str_viewer_name:
                        if lst_file:
                            if f.get_creation_date() > lst_file[0]:
                                lst_file[0] = f.get_creation_date()
                                lst_file[1] = viewer
                        else:
                            lst_file.append(f.get_creation_date())
                            lst_file.append(viewer)
        logger.info('get_murex_viewer ran without error.')
        return lst_file[1]
    except Exception as e:
        logger.info('get_murex_viewer ran with error: ' + str(e))
        return False
        
if __name__ == '__main__':
    pass