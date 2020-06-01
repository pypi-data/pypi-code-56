'''
Created on Dec 4, 2019

@author: Reynolds
'''

import os, sys

from configparser import ConfigParser

class wrt_settings(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._error = False
        self._settings = {}
        self._parser = ConfigParser()
        
    def read(self,file):
        try:
            print('Reading %s ... ' % file,end='')
            if not os.path.exists(file): raise Exception('WRT Configuration file does not exist')
            self._parser.read(file)
            print('Done')
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
            self.write(file)# write the defaults
            
    
    def _parse(self):
        self.set('system_sensor',self._get_dict_value('SYSTEM','SENSOR',0,1704))
        self.set('system_ids',self._get_dict_value('SYSTEM','ids',0,['0'])) 
        self.set('system_id',int(self.get('system_ids')[0]))
        
        self.set('software_mode',self._get_dict_value('SETTINGS','mode',0,'operation'))
        
        self.set('sen_freq',self._get_dict_value('TOTALFIELD','freq',0,100))
        self.set('sen_time',self._get_dict_value('TOTALFIELD','time',0,10.0))
        self.set('sen_demean',self._get_dict_value('TOTALFIELD','demean',0,False))
        self.set('sen_filt',self._get_dict_value('TOTALFIELD','filter',0,'none'))
        self.set('sen_filt_win',self._get_dict_value('TOTALFIELD','window',0,15))
        self.set('sen_cutoff',self._get_dict_value('TOTALFIELD','filter',0,'none'))
        
    def set(self,key,value):
        try:
            self._settings[key] = value
        except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
            
    def get(self,key=''):
        try:
            return self._settings[key]
        except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
            return None
            
    def write(self,file):
        print(file)
    
    def errored(self):
        error = self._error
        self._error = False
        return error
    
    def _get_dict_value(self,section,value,index,default=-1):
        ''' returns a value from a dictionary '''
        try:
            if type(default) == type(float(0)):
                return float(self._parser[section][value][index].strip())
            elif type(default) == type(int(0)):
                return int(self._parser[section][value][index].strip())
            elif type(default) == type(''):
                return self._parser[section][value][index].strip()
            elif type(default) == type(True):
                return self._parser[section][value][index].strip() in ['true','True']
            elif type(default) == type([]):
                return self._parser[section][value]
            else: return default
        except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
            return default
        
    def _cslist(self,l):
        ''' creates a comma separated list '''
        string = ''
        for ll in l:
            if type(ll) == type(' '): string += ll + ','
            else: string += str(ll) + ','
        return string[:-1]