'''
Created on Nov 19, 2019

@author: reynolds
'''

import os, sys, struct

import numpy as np

from wrtdk.parser.parser import parser

class conf(parser):
    PREAMBLE = b'CONF'
    
    def __init__(self,version=5,length=27):
        super().__init__()
        self._version = version
        self._mlen = length
        self.reset()
        
    def reset(self):
        self._chksum = self._minus1()
        self._chkver = self._minus1()
        self._conver = self._minus1()
        self._sysid  = self._minus1()
        self._fid    = self._minus1()
        self._svnver = self._minus1()
        self._states = self._minus1()
        self._txcnt  = self._minus1()
        self._systmt = self._minus1()
        self._samplt = self._minus1()
        self._samplc = self._minus1()
        self._thold  = self._minus1()
        self._rxsc   = self._minus1()
        self._axsc   = self._minus1()
        self._bnsc   = self._minus1()
        self._bins   = []
        
    def getData(self):
        '''
        0) checksum
        1) checksum version
        2) conf version
        3) system id
        4) fiducial
        5) svn revision
        6) max tx states
        7) tx on count. NOT THE NUMBER OF TXS
        8) System Timer 
        9) Sample Timer
        10) Timer Holdoff
        11) Rx Cube Count
        12) Axes Count
        13) Bin Count
        14:14+Bin Count) Bins
        '''
        return [self._chksum,
                self._chkver,
                self._conver,
                self._sysid,
                self._fid,
                self._svnver,
                self._states,
                self._txcnt,
                self._systmt,
                self._samplc,
                self._thold,
                self._rxsc,
                self._axsc,
                self._bnsc] + self._bins
                
    def get_fiducial(self):
        return self._fid
        
    def get_bins(self):
        return self._bins
    
    def get_bins_micros(self):
        return  (np.diff( np.array([0] + self._bins) )/2.0 + 
                          np.array([0] + self._bins[:-1]) ) * self.get_sample_time_micros() + self.get_holdoff_micros()
                          
    def get_sample_time_micros(self):
        return float(self._samplt)
    
    def get_holdoff_micros(self):
        return float(self._thold) * float(self._samplt)
    
    def get_length(self):
        return self._mlen + 2 * self._bnsc + 1
    
    def get_version(self):
        return self._version
    
    def get_axes(self):
        return self._axsc
    
    def get_rxs(self):
        return self._rxsc
    
    def get_bin_count(self):
        return self._bnsc
    
    def checksum(self,byte_values):
        return 0
    
    def __str__(self):
        return '%s[error:%b,bins:%d,rxs:%d,axes:%d]' % (type(self).__name__,self._error,self._bns.self._axs)
    
class confv3(conf):
    '''
    classdocs
    '''
    
    _LENGTH = 24
    _VERSION = 3

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(self._VERSION,self._LENGTH)
        self.reset()
        
    def parse(self,msg):
        try:
            m = struct.unpack('>4sHHBBBBHHxxHBBBB',msg[0:self._mlen])
            if m[0] != self.PREAMBLE: 
                raise('CONFFormatException',
                      'This is not an em configuration message')
            
            self._fid = m[1]
            self._svnver = m[2]
            self._conver = m[3]
            if self._conver != self._version: 
                raise Exception('CONFVersionException',
                                'This is not the proper version.')
            self._states = m[5]
            self._txcnt = m[6]
            self._systmt = m[7]
            self._samplc = m[9]
            self._thold = m[10]
            self._rxsc = m[11]
            self._axsc = m[12]
            self._bnsc = m[13]
        except Exception as e:
            self._error = True
            self.reset()
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))  
        
class confv5(conf):
    '''
    classdocs
    '''
    
    _LENGTH = 27
    _VERSION = 5

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(self._VERSION,self._LENGTH)
        self.reset()
    
    def checksum(self,byte_values):
        '''
        calculate a checksum value of a section of bytes
        '''
        total=0
        for b in byte_values: 
            total+=b
        return total & 255
    
    def parse(self,msg):
        self.reset()
        
        try:
            if msg[-1] != 10: 
                raise Exception('CONFEndOfLineException',
                                              'CONF Message does not end with a line feed')
            
            m = struct.unpack('>4s4B2H4B2HBH4B',msg[0:self._mlen])
            if m[0] != self.PREAMBLE: 
                raise('CONFFormatException',
                      "Did not begin with CONF")
            self._chksum = m[1]
            self._conver = m[2]
            if self._conver != self._version: 
                raise Exception('CONFVersionException',
                                'CONF version %d instead of CONF version %d'%(self._conver,self._version))
                
            if self.checksum(msg[5:-1]) != self._chksum:
                raise Exception('CONFVersionException',
                                'Checksum did not match: %d vs %d'%(self._chksum,self.checksum(msg[5:-1])))
            #check sum version
            self._chkver = m[3]
            self._sysid = m[4]
            self._fid = m[5]
            self._svnver = m[6]
            
            self._states = m[9]
            self._txcnt = m[10]
            self._systmt = m[11]
            self._samplt = m[12]
            self._samplc = m[14]
            self._thold = m[15]
            self._rxsc = m[16]
            self._axsc = m[17]
            self._bnsc = m[18]
            
            frmt='>%dH'%(self._bnsc)
            self._bins = list(struct.unpack(frmt,msg[self._mlen:self._mlen+2*self._bnsc]))
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))  