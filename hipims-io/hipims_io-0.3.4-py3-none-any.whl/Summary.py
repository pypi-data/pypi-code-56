#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
summary
To do:
    To generate, store, write, and read summary information of a flood model
-----------------    
Created on Fri Jun  5 15:44:18 2020

@author: Xiaodong Ming
"""
import numpy as np
from hipims_io.InputHipims import _get_cell_id_array
from hipims_io import spatial_analysis as sp
from hipims_io import rainfall_processing as rp
class Summary:
    """ Summary information of a flood case
    """
    # default parameters
    general_attr = {'name':None,
                    'location':None,
                    'birthday':None}
    grid_attr = {'area':0, # domain area in meter
                 'shape':(1, 1), # tuple of int, grid size rows and cols
                 'cellsize':1,
                 'num_cells':0, # number of valid cells
                 'outline': [0, 0] # XY coords of outline points
                 }
    model_attr = {'case_folder':None, # string
                  'num_GPU':1,
                  'run_time':(0, 3600, 600, 3600),
                  'gauges_pos': [[0, 0], [1, 1]]} 
                             # start, end, write_interval, backup_interval 
    boundary_attr = {'num_boundary':1,
                     'boundary_infor':'outline'}
    rain_attr = {'num_source':0,
                 'average':0,
                 'sum':0,
                 'max':0,
                 'spatial_res':1000, # meter
                 'temporal_res':0 # second
                 }
    initial_condition = {'h0':0, 'hUx0':0, 'hUy0':0}
    grid_params = {'manning':0, 'sewer_sink':0,
                   'cumulative_depth':0, 'hydraulic_conductivity':0,
                   'capillary_head':0, 'water_content_diff':0}
    def __init__(self, data_in): 
        if type(data_in) is str: # a jason file
            pass
        else: # a case_obj or dem_obj
            if hasattr(data_in, 'case_folder'): # a Input hipims object
                dem_array = data_in.DEM.array
                dem_header = data_in.DEM.header
                gauges_pos = data_in.attributes['gauges_pos']
                self.assign_model_attr(case_folder=data_in.case_folder,
                                       num_GPU=data_in.num_of_sections,
                                       run_time=data_in.times,
                                       gauges_pos=gauges_pos)
                rain_source = data_in.attributes['precipitation_source']
                rain_mask = data_in.attributes['precipitation_mask']+dem_array*0
                cellsize = data_in.DEM.header['cellsize']
                self.assign_rain_attr(rain_source, rain_mask, cellsize)
            elif hasattr(data_in, 'extent'): # a Raster object
                dem_array = data_in.array
                dem_header = data_in.header
            self.assign_grid_attr(dem_array, dem_header)
            
    def __str__(self):
        """
        To show object summary information when it is called in console
        """
        self.display()
        return  self.__class__.__name__
    __repr__ = __str__
    
    def assign_grid_attr(self, dem_array, dem_header):
        """ assign grid_attr
        """
        cellsize = dem_header['cellsize']
        shape = dem_array.shape
        valid_id, outline_id = _get_cell_id_array(dem_array)
        num_cells = ~np.isnan(valid_id)
        num_cells = num_cells.sum()
        rows, cols = np.where(~np.isnan(outline_id))
        X, Y = sp.sub2map(rows, cols, dem_header)
        grid_attr = {'area':num_cells*cellsize**2,
                     'shape':shape,
                     'cellsize':cellsize,
                     'num_cells':num_cells,
                     'outline': [X, Y]
                     }
        self.grid_attr = grid_attr     
        
    def assign_model_attr(self, **kw):
        """ assign case_folder, num_GPU, run_time, gauge_pos
        """
        for key, value in kw.items():
            self.model_attr[key] = value
    
    def assign_rain_attr(self, rain_source, rain_mask, cellsize):
        """ define rain_attr
        """
        times = rain_source[:,0]
        temporal_res = (times.max()-times.min())/times.size # seconds
        num_cells = rain_mask[~np.isnan(rain_mask)]
        num_source = np.unique(num_cells).size
        spatial_res = np.sqrt(num_cells.size*cellsize/num_source)
        data_sum = rp.get_time_series(rain_source, rain_mask, method='sum')
        rain_total = np.trapz(data_sum[:,1], x=times/3600, axis=0) # mm
        rain_mean = rain_total/(times.max()-times.min())*3600 # mm/h
        data_max = rp.get_time_series(rain_source, rain_mask, method='max')
        self.rain_attr['num_source'] = num_source
        self.rain_attr['max'] = np.max(data_max[:,1]).round(2)
        self.rain_attr['sum'] = rain_total.round(2)
        self.rain_attr['average'] = rain_mean.round(2)
        self.rain_attr['spatial_res'] = spatial_res.round()
        self.rain_attr['temporal_res'] = temporal_res.round()

    def display(self):
        print('-----------------------Grid information-----------------------')
        print(self.grid_attr)
        print('-----------------------Model attribute------------------------')
        print(self.model_attr)
        print('-----------------------Rainfall information-------------------')
        print(self.rain_attr)
    