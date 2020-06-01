'''
Created on Dec 17, 2019

@author: Reynolds
'''

import sys

import numpy as np

class geophysical_data(object):
    '''
    classdocs
    '''

    def __init__(self,length=1):
        '''
        length corresponds to the number of systems
        '''
        self.geodata = [np.array([])] * length
        self.vmag = [np.array([])] * length
        self.imu = [np.array([])] * length
        self.lidar = [np.array([])] * length
        self.sonar = [np.array([])] * length
        self.gpgga = [np.array([])] * length
        self.gprmc = [np.array([])] * length
        
if __name__ == '__main__':
    a = geophysical_data()
    d = {'tfmag':np.array([]),
             'vmag':np.array([]),
             'imu':np.array([]),
             'lidar':np.array([]),
             'sonar':np.array([]),
             'gpgga':np.array([]),
             'gprmc':np.array([]) }
    
    print(sys.getsizeof(a),sys.getsizeof(d))
        