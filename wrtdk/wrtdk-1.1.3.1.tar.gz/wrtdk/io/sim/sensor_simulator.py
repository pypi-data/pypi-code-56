'''
Created on Apr 8, 2020

@author: Reynolds
'''

import threading, time, os

class simulator(threading.Thread):
    '''
    classdocs
    '''

    def __init__(self,port=[]):
        '''
        Constructor
        '''
        super().__init__()
        self._port = port
        self._msgs = []
        self._dt = []
        self._current = 0
        self._running = False
        self._error = False
        
    def _append(self,msg,dt):
        self._msgs.append(msg)
        self._dt.append(dt)
        
    def read(self,filename):
        print('Reading %s ... ' % filename)
        if not os.path.exists(filename): 
            self._error = True
            print('Error. %s does not exist' % filename)
        
    def run(self):
        threading.Thread.run(self)
        
        if self._error: return
        
        if not self._port: 
            print('No port was entered')
            return
        
        self._running = True
        while self._running:
            try:
                self._port.write(self._msgs[self._current])
                time.sleep(self._dt[self._current])
                self._current += 1
                if self._current >= len(self._msgs): self._current = 0
            except Exception as e:
                print(str(e))
                time.sleep(1)
                continue