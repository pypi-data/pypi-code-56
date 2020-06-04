# -*- coding: utf-8 -*-
"""
Created on Mon May 25 01:03:10 2020

@author: LIM YUAN QING
"""

import os
import json
import requests
from requests.auth import HTTPBasicAuth
import datetime

import sentinelsat as sentinel
import planet

import dd8
import dd8.utility.utils as utils


logger = utils.get_basic_logger(__name__, dd8.LOG_PRINT_LEVEL, dd8.LOG_WRITE_LEVEL)

class Satellite(object):
    """
    Abstract base class for satellite image sources. Provides consistent 
    interfacing for searching and downloading of satellite images.
   
    Attributes
    ----------
    
   
    Methods
    -------
    """
    def __init__(self):
        self.__geojson = None
        self.__dic_filters = dict()
    
    @property
    def geojson(self):
        return self.__geojson
    
    @geojson.setter
    def geojson(self, geojson):
        self.__geojson = geojson
        
    @property
    def geojson_geometry(self):
        if self.geojson:
            for item in self.geojson['features']:
                if 'geometry' in item:
                    return item['geometry']
        return None
    
    @property
    def filters(self):
        return self.__dic_filters
    
    def read_geojson(self, str_full_filepath):
        self.geojson = sentinel.read_geojson(str_full_filepath)
        
    def add_date_range_filter(self, str_start, str_end):
        try:
            self.__dic_filters['date'] = {'start' : str_start,
                                          'end' : str_end}
            return True
        except:
            return False
    
    def add_cloud_cover_filter(self, dbl_max_cover_allowed,
                               dbl_min_cover_allowed=0.0):
        try:
            self.__dic_filters['cloud'] = {'lower' : dbl_min_cover_allowed,
                                           'upper' : dbl_max_cover_allowed}
            return True
        except:
            return False
    
    def query(self):
        pass

class Sentinel(Satellite):
    """
    Extends `Satellite` class. The `Sentinel` class provides an interface to 
    obtain data from the Sentinel-2 mission through Copernicus Open Access Hub. 
    
    The Copernicus Sentinel-2 mission comprises a constellation of two polar-
    orbiting satellites placed in the same sun-synchronous orbit, phased at 180° 
    to each other. It aims at monitoring variability in land surface conditions, 
    and its wide swath width (290 km) and high revisit time (10 days at the 
    equator with one satellite, and 5 days with 2 satellites under cloud-free 
    conditions which results in 2-3 days at mid-latitudes) will support monitoring 
    of Earth's surface changes. The coverage limits are from between latitudes 
    56° south and 84° north.
    
    Attributes
    ----------
    geojson
    geojson_geometry
    filters
    well_known_text
    
    Methods
    -------
    add_date_range_filter(str_start, str_end)
        filter satellite images by date range
    add_cloud_cover_filter(dbl_max_cover_allowed, dbl_min_cover_allowed=0.0)
        filter satellite images by percentage cloud cover detected
    query(str_platform_name='Sentinel-2')
        execute query with user-specified filters
    """
    def __init__(self, str_username, 
                     str_password, 
                     str_url = 'https://scihub.copernicus.eu/dhus'):
        """
        Initialize a Sentinel instance. 

        Parameters
        ----------
        str_username : str
            username as registered at https://scihub.copernicus.eu/dhus/#/self-registration
        str_password : str
            password as registered at https://scihub.copernicus.eu/dhus/#/self-registration
        str_url : str, optional
            url as specified at Copernicus API Hub (default is `https://scihub.copernicus.eu/dhus`)        
        """        
        super().__init__()
        self.__api = sentinel.SentinelAPI(str_username, 
                                          str_password, 
                                          str_url)
        self.__products = None
    
    @property
    def well_known_text(self):
        if self.geojson:
            return sentinel.geojson_to_wkt(self.geojson)
        return None
    
    @property
    def products(self):
        return self.__products
    
    @products.setter
    def products(self, products):
        self.__products = products
    
    def query(self, str_platform_name='Sentinel-2'):
        self.products = self.__api.query(self.well_known_text,
                                    date=(self.filters['date']['start'],
                                          self.filters['date']['end']),
                                    platformname=str_platform_name,
                                    cloudcoverpercentage=(self.filters['cloud']['lower'],
                                                          self.filters['cloud']['upper']))
        
        return self.prod
    
        return self.__api.download_all(products)
        
class Planet(object):
    STR_API_KEY_ENV_NAME = 'PL_API_KEY'
    # https://www.youtube.com/watch?v=txhjhjWqF7c&t=114s
    # http://geojson.io/#map=14/-23.8135/133.8975
    def __init__(self, str_key = ''):
        if str_key == '':
            if self.STR_API_KEY_ENV_NAME in os.environ:
                self.__str_api_key = os.getenv(self.STR_API_KEY_ENV_NAME)
            else:
                self.__str_api_key = ''
        else:
            self.__str_api_key = str_key
        self.__api = planet.api.ClientV1(api_key=self.__str_api_key)
        self.__dic_filters = dict()
        self.__search_result = None
        
    @property
    def geojson_geometry(self):
        if 'geometry' in self.__dic_filters:
            return self.__dic_filters['geometry']['config']
        else:
            return None
        
    @property
    def combined_filter(self):
        try:
            filters = [self.__dic_filters[k] for k in self.__dic_filters.keys()]
            return {'type' : 'AndFilter',
                    'config' : filters
                    }
        except:
            return None
    
    @property
    def search_result(self):
        #return json.dumps(self.__search_result.json(), indent=1)
        #return self.__search_result.json()
        return self.__search_result
        
    @search_result.setter
    def search_result(self, result = None):
        if result:
            self.__search_result = result
    
    @property
    def search_result_dump(self):
        return json.dumps(self.search_result.json(), indent=1)
    
    @property
    def search_result_ids(self):
        return [feature['id'] for feature in self.search_result.json()['features']]    
#    
#    @geojson_geometry.setter
#    def geojson_geometry(self, geojson_geometry_new):
#        self.__geojson_geometry = geojson_geometry_new
        
    def add_geometry_filter(self, geojson_geometry):
        try:
            geometry_filter = {
                    'type' : 'GeometryFilter',
                    'field_name' : 'geometry',
                    'config' : geojson_geometry
                    }
            self.__dic_filters['geometry'] = geometry_filter
            return True
        except:
            return False
        
    def add_date_range_filter(self, str_start, str_end):
        try:
            date_range_filter = {
                    'type' : 'DateRangeFilter',
                    'field_name' : 'acquired',
                    'config' : {'gte' : str_start,
                                'lte' : str_end
                                }
                    }
            self.__dic_filters['date'] = date_range_filter
            return True
        except:
            return False
        
    def add_cloud_cover_filter(self, dbl_max_cover_allowed):
        try:
            cloud_cover_filter = {
                    'type' : 'RangeFilter',
                    'field_name' : 'cloud_cover',
                    'config' : {'lte' : dbl_max_cover_allowed}
                    }
            self.__dic_filters['cloud'] = cloud_cover_filter
            return True
        except:
            return False
        
    def quick_search(self, str_interval = 'day', 
                     lst_item_types = ['PSScene4Band'],                     
                     str_search_url = 'https://api.planet.com/data/v1/quick-search'):
        search_request = {
                    'interval' : str_interval,
                    'item_types' : lst_item_types,
                    'filter' : self.combined_filter                
                    }
        self.search_result = requests.post(str_search_url, 
                                 auth = HTTPBasicAuth(self.__str_api_key, ''),
                                 json = search_request)
        return self.search_result
    
    def download_image_id(self, str_id, str_item_type='PSScene4Band'):
        url = 'https://api.planet.com/data/v1/item-types/{str_item_type}/items/{str_id}/assets'.format(
                    str_item_type=str_item_type, str_id=str_id)
        result = requests.get(url, auth=HTTPBasicAuth(self.__str_api_key, ''))
        links = result.json()[u'analytic']['_links']
        self_link = links['_self']
        activation_link = links['activate']
        print('self_link: ' + self_link)
        print('activation_link: ' + activation_link)
        activation_result = requests.get(activation_link, 
                                         auth=HTTPBasicAuth(self.__str_api_key,''))
        
        return (self_link, self.__str_api_key)
        
        
        