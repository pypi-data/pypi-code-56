'''
Created on Apr 3, 2020

@author: Reynolds
'''

import datetime
import numpy as np

from wrtdk.parser.em.em3d.em.em import emv2, emv1
from wrtdk.parser.em.em3d.conf.conf import confv5, confv3
from wrtdk.parser.nmea.nmea import gpgga
from wrtdk.io.read.file_reader import file_reader
from wrtdk.parser.imu.microstrain import lord3dm_cv5

class apex_reader(file_reader):
    '''
    a class for reading in white river technologies 
    APEX EM sensing system proprietary DAT files. It
    returns the data in a dictionary. The class is 
    compatible with all marine and land based EM systems
    utilizing the CONF message style data format, versions
    3 and 5.
    '''
    DOLLAR_SIGN = 36
    LITTLE_T = 116
    BIG_C = 67
    ID_LEN = 6
    DATE_FRMT = '%d %m %Y %H %M %S'
    DEFAULT = '*'
    
    SOL = [BIG_C,LITTLE_T,DOLLAR_SIGN]
    
    def __init__(self,version=1,em3d=True):
        '''
        Constructor
        '''
        super().__init__()
        self.set_version(version=version)
        self._gparse = gpgga()
        self._iparse = lord3dm_cv5()
        self._clen = 0
        self.set_3d(em3d)
        self._rxs = 0
        self._axs = 0
        self._offset = 3
    
    def set_version(self,version=1):
        '''
        sets the version number. currently, 1 or 2
        are the available version numbers and defaults
        to version 1
        '''
        if version == 2:
            self._eparse = emv2()
            self._cparse = confv5()
            self._version = 2
        else:
            self._eparse = emv1()
            self._cparse = confv3()
            self._version = 1
            
    def set_3d(self,em3d=True):
        '''
        sets the 3D boolean. This should only be false
        for EMPACT DD
        '''
        self._3d = em3d
        if self._3d: self._txs = 6
        else: self._txs = 1
                    
    def get_version(self):
        '''
        returns the version number
        '''
        return self._version
    
    def _is_sol(self,b):
        '''
        returns whether a byte is a start of line character
        '''
        return b in self.SOL
    
    def _is_eol(self,b):
        '''
        checks whether a byte is an end of line character 
        '''
        return b == 10
    
    def _set_length(self,rx=0,ax=0):
        '''
        Sets the number of axes, receivers and the
        number of messages to count
        '''
        self._axs = ax
        self._rxs = rx
        self._len = self._offset + self._txs*self._rxs*self._axs
        
    def _get_header(self,buffer):
        ''' 
        returns the header information
        '''
        h = {}
        h['time'] = self._get_datetime(self._get_line(buffer,b'ACQ TIME:'))
        h['julian_time'] = self._get_julian(h['time'])
        h['zulu_time'] = self._get_zulu(h['time'])
        h['mode'] = self._get_line(buffer,b'OPERATION MODE:')
        h['operator'] = self._get_line(buffer,b'OPERATOR:')
        h['project'] = self._get_line(buffer,b'PROJECT:')
        h['grid'] = self._get_line(buffer,b'GRID')
        h['line'] = self._get_line(buffer,b'LINE')
        h['equipment_version'] = self._get_line(buffer,b'EQUIPMENT VER:')
        h['equipment_sn'] = self._get_line(buffer,b'EQUIPMENT SN')
        h['software_ver'] = self._get_line(buffer,b'ACQ SOFTWARE VER:')
        h['software_path'] = self._get_line(buffer,b'ACQ SOFTWARE PATH:')
        h['sft_cal_path'] = self._get_line(buffer,b'SFT PATH:')
        h['orientation_sys'] = self._get_line(buffer,b'ORIENTATION SYS:')
        h['orientation_sys_offset'] = self._get_line(buffer,b'ORIENTATION SYS OFFSET:')
        h['spatial_reg_sys'] = self._get_line(buffer,b'SPATIAL REG SYS:')
        h['spatial_reg_sys_offset'] = self._get_line(buffer,b'SPATIAL REG SYS OFFSET:')
        h['ground_tx_assembly_h'] = self._get_line(buffer,b'TX ASSEMBLY HEIGHT:')
        h['tx_assembly_z_coil_h'] = self._get_line(buffer,b'Z COIL ABOVE TX ASSEMBLY HEIGHT:')
        
        return h
    
    def _get_line(self,buffer,string):
        '''
        Returns a line in the header based on the search string and
        buffer bytes object
        '''
        pos = buffer.find(string)
        if pos == -1: return '*'
        
        eol = buffer.find(b'\n',pos)
        if eol == -1: return '*'
        
        return buffer[pos+len(string):eol+1].decode().strip()
        
    def _get_zulu(self,dt):
        try:
            return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return self.DEFAULT
    
    def _get_julian(self,dt):
        try:
            tt = dt.timetuple()
            return '%04d%03d' % (tt.tm_year,tt.tm_yday)
        except:
            return self.DEFAULT
    
    def _get_datetime(self,line):
        '''
        parses the header timestamp into a datetime object
        '''
        try:
            return datetime.datetime.strptime(line,self.DATE_FRMT)
        except Exception as e:
            print('Error parsing timestamp %s'%str(e))
            return '*'
    
    def _get_conf(self,buffer):
        '''
        Parses the first CONF message to set the EM data.
        If no messages of the proper type are found, it 
        returns a false boolean for whether a CONF message
        has been found. True if it does find a correct CONF
        message
        '''
        pos = 0
        # cycle through all conf messages in the first is corrupt
        while pos < len(buffer):
            # find the first messade
            pos = buffer.find(b'CONF',pos)
            
            # find the end of the message
            i = 1# counter from the current position
            while i+pos < len(buffer):# cycle through the entire buffer
                # check if the current byte starts the next message
                if (self._is_sol(buffer[i+pos]) and 
                    self._is_eol(buffer[i+pos-1])): break# if true then break.
                i += 1# increment the counter
            
            # parse the message
            self._cparse.parse(buffer[pos:pos+i])
            if not self._cparse.hasErrored():# check for errors
                self._clen = self._cparse.get_length()
                self._eparse.set_bins(self._cparse.get_bin_count())# set the bins
                return True# message found
            # increment the position
            pos = pos+1
            
        print('No CONF message found.')
        return False
    
    def _get_sol(self,buffer):
        '''
        Returns the start of line characters for the bytes
        object buffer. The last element in the start of line
        list is the length of the buffer so the entire last
        message can be called. Additionally returns the message 
        count for all messages found.
        '''
        sol = []# hold start of line indices
        length = len(buffer)# length of buffer
        for i,b in enumerate(buffer):# enumerate buffer length
            if self._is_sol(b) and self._is_eol(buffer[i-1]): sol.append(i)# add index if start of line
        sol.append(length)# add the end of the file
            
        # trim and count the messages
        count = [0] * self._eparse.get_output_length(txs=6,# count the messages
                                                     rxs=self._cparse.get_rxs(),
                                                     axs=self._cparse.get_axes())
        start = 0# start msg index
        end = 0# end msg index
        i = 0# position in sol indices
        while i < len(sol)-1:
            start = sol[i]# calculate position
            end = sol[i+1]-1# calculate end
            
            # sot by message start character
            if buffer[start] == self.LITTLE_T:# em
                if (self._is_eol(buffer[end])):# confirm em message
                    try:
                        count[self._eparse.get_em_index(buffer[start+2],
                                                    self._cparse.get_rxs(),
                                                    self._cparse.get_axes())] += 1
                    except Exception as e:
                        print(str(e),buffer[start-1:end+1])
                        return (sol,count)             
                    i+=1# increase position in sol list
                else: 
                    print('removed:',end-start,start,'/',length,buffer[start:end])
                    sol.remove(start)# remove item from list. no duplicates possible
            elif (buffer[start] == self.DOLLAR_SIGN and 
                  length - start > self.ID_LEN):# position/attitude
                if ((buffer[start:start+self.ID_LEN] == b'$GPGGA' or
                    buffer[start:start+self.ID_LEN] == b'$GNGGA') and 
                    self._is_eol(buffer[end])):# confirm
                    count[self._eparse.get_pos_index()] += 1
                    i+=1# increase position in sol list
                elif (buffer[start:start+self.ID_LEN] == b'$IMUAP' and 
                        self._is_eol(buffer[end]) ):
                    count[self._eparse.get_imu_index()] += 1
                    i+=1# increase position in sol list
                else: sol.remove(start)# remove item from list. no duplicates possible
            elif (buffer[start] == self.BIG_C and 
                  length - start > 4):# em configuration
                if (self._is_eol(buffer[end])  and 
                    buffer[start:start+4] == b'CONF'):
                    count[self._eparse.get_conf_index()] += 1
                    i+=1# increase position in sol list
                else: sol.remove(start)# remove item from list. no duplicates possible
            else: sol.remove(start)# remove item from list. no duplicates possible
        return (sol, count)
    
    def _get_axis(self,ax=0):
        '''
        returns the sensing axis from the integer
        '''
        if ax == 0: return 'x'
        elif ax == 1: return 'y'
        elif ax == 2: return 'z'
        else: return 'w'
        
    def _get_tx(self,tx=0):
        ''' 
        returns the Tx axis from the integer
        '''
        if tx == 0: return 'x+'
        elif tx == 1: return 'A'
        elif tx == 2: return 'y+'
        elif tx == 3: return 'B'
        elif tx == 4: return 'z+'
        else: return 'C'
            
    def _read(self,file):
        '''
        Reads the file into a byte array and then
        parses the individual messages if the file
        is the correct type. It returns a dictionary
        filled with the data: EM, CONF, HEADER, IMU
        and GNSS
        '''
        d = {}
        with open(file,'rb') as f:
            b = f.read()# read all the bytes
            if not self._get_conf(b): return d# get the first conf message
            
            # intialize the dictionary
            d['HEADER'] = self._get_header(b)# header info
            sol,c = self._get_sol(b)# get sol indices and count messages
            d['HEADER']['message_count'] = len(sol)-1
            d['CONF'] = {'count':    np.arange(c[self._eparse.get_conf_index()]),
                         'fiducial': np.zeros( (c[self._eparse.get_conf_index()]) ),
                         'number':   np.zeros( (c[self._eparse.get_conf_index()]) ),
                         'data':     np.zeros( (c[self._eparse.get_conf_index()],
                                                len(self._cparse.getData())) )}# conf messages
            d['GNSS'] = {'count':    np.arange(c[self._eparse.get_pos_index()]),
                         'fiducial': np.zeros( (c[self._eparse.get_pos_index()]) ),
                         'number':   np.zeros( (c[self._eparse.get_pos_index()]) ),
                         'data':     np.zeros( (c[self._eparse.get_pos_index()],
                                                len(self._gparse.getData())) )}# position data
            d['IMU'] = {'count':    np.arange(c[self._eparse.get_imu_index()]),
                        'fiducial': np.zeros( (c[self._eparse.get_imu_index()]) ),
                        'number':   np.zeros( (c[self._eparse.get_imu_index()]) ),
                        'data':     np.zeros( (c[self._eparse.get_imu_index()],
                                               3)) }# imu data
            d['EM'] = {}# em data
            for i in range(self._txs):# cycle through all transmitters
                tx = self._get_tx(i)
                d['EM'][tx] = {}
                start = self._eparse.get_em_index((i,0,0),
                                                  self._cparse.get_rxs(),
                                                  self._cparse.get_axes())
                stop = self._eparse.get_em_index((i,self._cparse.get_rxs()-1,self._cparse.get_axes()-1),
                                                 self._cparse.get_rxs(),
                                                 self._cparse.get_axes())
                rows = max(c[start:stop+1])
                d['EM'][tx] = {'count':    np.arange( rows ),
                               'fiducial': np.zeros( (rows,self._cparse.get_rxs()*self._cparse.get_axes()) ),
                               'number':   np.zeros( (rows,self._cparse.get_rxs()*self._cparse.get_axes()) ),
                               'data':     np.zeros( (rows,self._cparse.get_rxs()*self._cparse.get_axes(),
                                                      self._cparse.get_bin_count()) )}
                        
            # populate the data fields
            c = [0] * len(c)# reinitialize counter
            index,tx,loc,msgid = 0,'',0,b''
            for i in range(len(sol)-1):
                if b[sol[i]] == self.LITTLE_T:
                    self._eparse.parse(b[sol[i]:sol[i+1]])
                    if not self._eparse.hasErrored():
                        index = self._eparse.get_em_index(b[sol[i]+self._eparse.get_id_index()],
                                                          self._cparse.get_rxs(),
                                                          self._cparse.get_axes())
                        tx = self._get_tx(self._eparse.get_tx())
                        loc = self._eparse.get_rx()*self._cparse.get_axes()+self._eparse.get_axis()
                        d['EM'][tx]['data'][c[index],loc,:] = self._eparse.get_decay()
                        d['EM'][tx]['number'][c[index],loc] = i
                        d['EM'][tx]['fiducial'][c[index],loc] = self._eparse.get_fiducial()
                        #print(self._eparse)
                        c[index] += 1
                elif b[sol[i]] == self.DOLLAR_SIGN:
                    msgid = b[sol[i]:sol[i]+self.ID_LEN]
                    if (msgid == b'$GPGGA' or
                        msgid == b'$GNGGA') :
                        self._gparse.parse(b[sol[i]:sol[i+1]])
                        if not self._gparse.hasErrored():
                            index = self._eparse.get_pos_index()
                            d['GNSS']['number'][c[index]] = i
                            d['GNSS']['data'][c[index],:] = self._gparse.getData()
                            c[index] += 1
                    elif msgid == b'$IMUAP':
                        self._iparse.parse(b[sol[i]+self.ID_LEN:sol[i+1]-1])
                        if not self._iparse.hasErrored():
                            index = self._eparse.get_imu_index()
                            d['IMU']['data'][c[index],:] = self._iparse.get_euler()
                            c[index] += 1
                elif b[sol[i]] == self.BIG_C:
                    self._cparse.parse(b[sol[i]:sol[i+1]])
                    if not self._cparse.hasErrored():
                        index = self._eparse.get_conf_index()
                        d['CONF']['data'][c[index],:] = self._cparse.getData()
                        d['CONF']['number'][c[index]] = i
                        d['CONF']['fiducial'][c[index]] = self._cparse.get_fiducial()
                        c[index] += 1   
        return d