'''
Created on Dec 17, 2019

@author: Reynolds
'''

import os, time

class file_reader(object):
    '''
    classdocs
    '''
    
    def _elapsed_time(self,now):
        return time.time() - now
    
    def read(self,filename):
        now = time.time()
        if not os.path.exists(filename):
            print('%s does not exist. %fs'%(filename,self._elapsed_time(now)))
            return {}
        
        print('Reading %s ...' % filename)
        
        d = self._read(filename)
        
        if d: print('Done. %fs'%self._elapsed_time(now))
        else: print('Error: %fs'%self._elapsed_time(now))
            
        return d
        
    def _read(self,filename):
        pass