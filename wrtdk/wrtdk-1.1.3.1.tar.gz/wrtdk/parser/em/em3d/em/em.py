'''
Created on Nov 19, 2019

@author: reynolds
'''
import os, sys, struct
from wrtdk.parser.parser import parser

class em(parser):
    
    PREAMBLE = b't'
    
    def __init__(self,count2mv=1):
        super().__init__()
        self._set = False
        self._count2mv = count2mv
        self._fmt = ''
        self.reset()
        
    def __str__(self):
        return '%s[tx:%d,rx:%d,ax:%d,fid:%d]'%(type(self).__name__,
                       self._tx,
                       self._rx,
                       self._ax,
                       self._ct)
        
    def reset(self):
        self._rx = self._minus1()
        self._tx = self._minus1()
        self._ax = self._minus1()
        self._ct = self._minus1()
        self._chksum = self._minus1()
        if not self.is_set(): self._tg = self._arr(0)
        
    def is_set(self):
        return self._set
        
    def set_bins(self,length=0):
        self._bins = length
        self._tg = self._arr(self._bins)
        self._set = True
    
    def get_em_index(self,b,rxs,axs):
        if not isinstance(b,tuple): tx,rx,ax = self.get_id_bits(b)
        elif len(b) is not 3: raise Exception('EMIndexException','The input tuple is not the proper length')
        else: tx,rx,ax = b
        #print('tx: %d rx: %d ax: %d %s'%(tx,rx,ax,self))
        return 3+tx*rxs*axs+ax*rxs+rx
    
    def get_tx(self):
        return self._tx
    
    def get_rx(self):
        return self._rx
    
    def get_axis(self):
        return self._ax
        
    def get_fiducial(self):
        return self._ct
    
    def get_imu_index(self):
        return 2
    
    def get_pos_index(self):
        return 1
    
    def get_conf_index(self):
        return 0
    
    def get_id_bits(self,b):
        return (0,0,0)
    
    def get_id_index(self):
        return 0
        
    def get_output_length(self,txs,rxs,axs):
        return 3+txs*rxs*axs
    
    def get_decay(self):
        return self._tg
    
    def get_decay_mv(self):
        return [i * self._count2mv for i in self._tg]
    
    def checksum(self):
        return 0
    
    def getData(self):
        ''' returns the data from the em message if set
        0) Tx
        1) Rx
        2) Ax
        3) Count
        4-end) millivolt bin data 
        '''
        if not self.is_set(): return []
        return [self._tx,self._rx,self._ax,self._ct]+self.get_decay_mv()

class emv1(em):
    '''
    classdocs
    '''
    
    TX_MASK = 0b11100000
    RX_MASK = 0b00011100
    AX_MASK = 0b00000011
    COUNT_TO_MV = .1526

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(count2mv=self.COUNT_TO_MV)
                
    def set_bins(self,length=0):
        super().set_bins(length=length)
        self._len = 1+1+1+self._bins*2+1
        self._fmt = '>cBB%dhx'%self._bins
    
    def get_id_bits(self, b):
        return ( ((b & self.TX_MASK) >> 5) - 1,
                 (b & self.RX_MASK) >> 2,
                 (b & self.AX_MASK) )
        
    def get_id_index(self):
        return 1
        
    def parse(self,msg):
        self.reset()
        
        try:
            if not self.is_set(): raise Exception('EMFormatException','Bin length is not set yet')
            elif msg[-1] != 10: raise Exception('EMFormatExcpetion',
                                            'Message is not terminated with new line feed')
            
            m = struct.unpack(self._fmt,msg)
            
            if m[0] != self.PREAMBLE: 
                raise Exception('EMFormatException','Message is not the proper format')
            
            self._tx,self._rx,self._ax = self.get_id_bits(m[1])
            self._ct = m[2]
            
            for i in range(self._bins): self._tg[i] = m[3+i]
                
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))    
    
class emv2(em):
    '''
    Identical to emv1 except with a checksum byte
    '''
    
    TX_MASK = 0b11100000
    RX_MASK = 0b00011100
    AX_MASK = 0b00000011
    COUNT_TO_MV = .1526

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(count2mv=self.COUNT_TO_MV)
                
    def get_id_bits(self, b):
        return ( ((b & self.TX_MASK) >> 5)-1,#this number is 1 indexed
                 (b & self.RX_MASK) >> 2,# zero indexed
                 (b & self.AX_MASK) )# zero indexed
        
    def get_id_index(self):
        return 2
    
    def checksum(self,byte_values):
        '''
        calculate a checksum value of a section of bytes
        '''
        total=0
        for b in byte_values:
            total+=b
        return total & 255
    
    def set_bins(self, length=0):
        super().set_bins(length=length)
        self._len = 1+1+1+1+self._bins*2+1
        self._fmt = '>cBBB%dhx'%self._bins
    
    def parse(self,msg):
        self.reset()
        
        try:
            if not self.is_set(): raise Exception('EMFormatException','Bin length is not set yet')
            elif msg[-1] != 10: raise Exception('EMFormatExcpetion',
                                            'Message is not terminated with new line feed')
            
            m = struct.unpack(self._fmt,msg)
            
            if m[0] != self.PREAMBLE: raise Exception('EMFormatException','Message is not the proper format')
            #checksum
            self._chksum = int(m[1])
            if self._chksum != self.checksum(msg[2:-1]):
                raise Exception('CONFVersionException',
                                'Checksum did not match')
            #cubestate
            self._tx,self._rx,self._ax = self.get_id_bits(m[2])
            #fiducial
            self._ct = m[3]
            
            for i in range(self._bins): self._tg[i] = m[4+i]
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))    