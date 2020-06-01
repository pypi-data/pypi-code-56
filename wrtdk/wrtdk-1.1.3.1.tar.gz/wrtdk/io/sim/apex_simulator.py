'''
Created on Apr 8, 2020

@author: Reynolds
'''

import time

from wrtdk.io.sim.simulator import simulator

class apex_simulator(simulator):
    '''
    classdocs
    '''
    
    DOLLAR_SIGN = 36
    LITTLE_T = 116
    BIG_C = 67
    SOL = [BIG_C,LITTLE_T,DOLLAR_SIGN]
    DOLLAT_MSGS = [b'$GPGGA',b'$GNGGA',b'$IMUAP']

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        
    def _is_sol(self,b):
        return b in self.SOL
    
    def _is_eol(self,b):
        return b == 10
    
    def _is_pos_msg(self,buffer):
        return buffer in self.DOLLAT_MSGS
    
    def _is_conf_msg(self,buffer):
        return buffer == b'CONF'
        
    def read(self, filename):
        t0 = time.time()
        simulator.read(self, filename)
        
        if not self._error:
            with open(filename,'rb') as f:
                buffer = f.read()
                length = len(buffer)
                
                sol = []
                for i,b in enumerate(buffer):
                    if self._is_sol(b) and self._is_eol(buffer[i-1]):
                        sol.append(i)
                sol.append(length)
                
                i = 0
                while i < len(sol)-1:
                    start = sol[i]
                    end = sol[i+1]-1
                    
                    if buffer[start] == self.LITTLE_T:
                        if self._is_eol(buffer[end]):
                            self._msgs.append(buffer[start:end+1])
                            self._dt.append(0.001)
                            i+=1
                        else: sol.remove(start)
                    elif buffer[start] == self.DOLLAR_SIGN and length - start > 6:
                        if self._is_eol(buffer[end]) and self._is_pos_msg(buffer[start:start+6]):
                            self._msgs.append(buffer[start:end+1])
                            self._dt.append(0.001)
                            i += 1
                        else: sol.remove(start)
                    elif buffer[start] == self.BIG_C and length - start > 4:
                        if self._is_eol(buffer[end]) and self._is_conf_msg(buffer[start:start+4]): 
                            self._msgs.append(buffer[start:end+1])
                            self._dt.append(0.001)
                            i += 1
                        else: sol.remove(start)
                    else: sol.remove(start)
                self._dt = self._dt[1::] + [4]
                self._len = len(self._msgs)
                print('Done. %.2fs'%(time.time()-t0))
                return True
            print('Error. %.2fs'%(time.time()-t0))
            return False
        print('Error. %.2fs'%(time.time()-t0))
        return False