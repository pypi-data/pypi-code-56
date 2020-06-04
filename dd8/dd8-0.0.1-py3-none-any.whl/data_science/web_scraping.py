# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:06:50 2019

@author: yuanq
"""

# Protocol for robots.txt can be found at http://www.robotstxt.org
# Sitemap standard is defined at http://www.sitemaps.org/protocol.html

# Road Map
# 1. check robots.txt
# 2. check sitemap
# 3. estimating size of website
#    - search for 'site:example.webscraping.com'; number of results will 
#      provide rought indication on size of website
#    - can try to use google api to automate this process
#      (https://developers.google.com/api-client-library/python/start/get_started)
# 4. get web technologies to determine scraping methods
# 5. get web owner to determine if domain is known to block crawlers
# 6. download web pages
# 7. crawl web pages

#import requests
#import urllib.request
#import time
#from bs4 import BeautifulSoup
#import re
#
#url = 'http://web.mta.info/developers/turnstile.html'
#response = requests.get(url)
#
#soup = BeautifulSoup(response.text, 'html.parser')
#results = soup.findAll('a')
#lst_results = list(results)
#
#for i in range(len(lst_results)):
#    
#    if re.findall('turnstile_[0-9]+.txt',str(lst_results[i])):
#        counter = i
#        break
#
#print(counter)

import builtwith as bw
import whois
import urllib
import urllib3
from bs4 import BeautifulSoup
import re

import dd8
import dd8.utility.utils as utils

logger = utils.get_basic_logger(__name__, dd8.LOG_PRINT_LEVEL, dd8.LOG_WRITE_LEVEL)


def get_url(str_url):
    """
    Wrapper for `urllib.request.urlopen` with error handling. Returns 
    `http.client.HTTPResponse` object which can work as a context manager.
    
    Parameters
    ----------
    str_url : str
        URL to open.
        
    Return
    ------
    http.client.HTTPResponse
        Context manager for given URL, `None` if error encountered.
    """
    response = None
    try:
        response = urllib.request.urlopen(str_url)        
    except urllib.error.HTTPError as e:
        logger.error(e)
    except urllib.error.URLError as e:
        logger.error('Server not found!')
    finally:
        return response

class HTML(object):
    pass

class Webpage(object):
    """
    Represents a particular `Webpage` on a `Website`. Lazy loading is used and
    website is only accessed when `read` method of a `Webpage` object is called.
    
    Attributes
    ----------
    url : str
        URL of the webpage.
    web_tech : dict
        dictionary of lists the form {'webpage_component' : list_of_technologies}.
        For example, {'programming-language' : ['Lua']}.
    whois : whois.parser.WhoisCom
        dictionary of server details of webpage. For example, {'domain_name' :
        list_of_domain_names}.    
    html
    
    Methods
    -------
    read(parser='html.parser')
        Reads and return HTML of the given URL.   
    """    
    def __init__(self, str_url):
        self.url = str_url        
        
    @property
    def url(self):
        return self.__str_url
    
    @url.setter
    def url(self, str_url):
        self.__str_url = str_url
    
    @property
    def web_tech(self):
        return bw.parse(self.url)
    
    @property
    def whois(self):
        return whois.whois(self.url)

    @property
    def html(self):
        pass

    @property
    def read(self, parser='html.parser'):
        """
        Reads and return HTML of the given url.
        
        Parameters
        ----------
        parser : str, optional
            parser to be used by BeautifulSoup to parse the webpage (default is
            html.parser)
                html.parser - included with Python 3
                lxml - requires installation but more flexible and faster
                html5lib - requires installation and slower than both html.parser
                    and lxml but more flexible
        """
#        if self.__bln_verbose:
#            print('Downloading: ' + self.__str_url)
        
        headers = {'User-agent': 'wswp'}
        http = urllib3.PoolManager()
        response = http.request('GET', self.__str_url, headers = headers)            
#        print(response.status)
        if response.status == 200:
            html = response.data.decode('utf-8') 
        else:
            if response.status >= 500 and response.status < 600:
                response = http.request('GET', self.__str_url, retries=5)            
                if response.status != 200:
#                    if self.__bln_verbose:
#                        print('Download Error: ' + str(response.status))
                    html = None
                else:
                    html = response.data.decode('utf-8')
            else:
#                if self.__bln_verbose:
#                        print('Download Error: ' + str(response.status))
                html = None
        return html




class Website(object):
    def __init__(self, str_domain_url):
        self.url = str_domain_url
        self.domain = self.url
        
    @property
    def url(self):
        return self.__str_original_url
    
    @url.setter
    def url(self, str_url):
        self.__str_original_url = str_url
    
    @property
    def domain(self):
        return self.__str_domain_url
    
    @domain.setter
    def domain(self, str_domain_url):
        __ = str_domain_url.split('//')
        self.__str_domain_url = '//'.join(__[:-1]) + '//' +__[-1].split('/')[0]
        
    @property
    def robots(self):
        return Webpage(self.domain+'/robots.txt').html


class WebScrape():
    def __init__(self, str_url, 
                 bln_scrape_sitemap = False, 
                 bln_verbose = False):
        self.__str_url = str_url
        self.__bln_verbose = bln_verbose
    
    def __del__(self):
        pass
    
    def __len__(self):
        pass
    
    def __repr__(self):
        pass
    
    def get_web_tech(self):        
        return bw.parse(self.__str_url)

    def get_web_owner(self):
        return whois.whois(self.__str_url)    
    
    def get_sitemap_urls(self, str_sitemap_url):
        sitemap = self.get_web_page(str_sitemap_url)
        print(sitemap)
        links = re.findall('<loc>(.*?)</loc>', sitemap)
        return links
    
    def get_web_page(self, 
                     str_user_agent = 'wswp',
                     int_retries = 5):
        
    # https://stackoverflow.com/questions/630453/put-vs-post-in-rest
    
        if self.__bln_verbose:
            print('Downloading: ' + self.__str_url)
        
        headers = {'User-agent': str_user_agent}
        http = urllib3.PoolManager()
        response = http.request('GET', self.__str_url, headers = headers)            
        print(response.status)
        if response.status == 200:
            html = response.data.decode('utf-8') 
        else:
            if response.status >= 500 and response.status < 600:
                response = http.request('GET', self.__str_url, retries=int_retries)            
                if response.status != 200:
                    if self.__bln_verbose:
                        print('Download Error: ' + str(response.status))
                    html = None
                else:
                    html = response.data.decode('utf-8')
            else:
                if self.__bln_verbose:
                        print('Download Error: ' + str(response.status))
                html = None
        return html
        

if __name__ == '__main__':

#    scrape = WebScrape('https://www.careers.gov.sg')
#    print(scrape.get_web_tech())
    #scrape = WebScrape('http://www.bloomberg.com/')
    #print(scrape.get_web_tech())
    #print(scrape.get_web_page())
    
    #links = scrape.get_sitemap_urls('https://www.bloomberg.com/feeds/bbiz/sitemap_index.xml')
    #print(links)
    
#    ws = Website('https://www.bloomberg.com/asia')
    wp = Webpage('https://www.bloomberg.com/asia')
    