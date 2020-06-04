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
import urllib3
from bs4 import BeautifulSoup
import re

class Website(object):
    def __init__(self, str_domain_url):
        self.__str_original_url = None
        self.__str_domain_url = None
        
        self.url = str_domain_url
        self.domain = self.url
        
    @property
    def url(self):
        """
        Get the original URL used to instantiate the `Website` object. Setting
        the URL to a new value will update its domain automatically.
        """
        return self.__str_original_url
    
    @url.setter
    def url(self, str_url):
        self.__str_original_url = str_url
        self.domain = self.url
    
    @property
    def domain(self):
        return self.__str_domain_url
    
    @domain.setter
    def domain(self, str_domain_url):
        _ = self.url.split('//')
        __ = str_domain_url.split('//')
        new_domain_url = '//'.join(__[:-1]) + '//' +__[-1].split('/')[0] 
        if '//'.join(_[:-1]) + '//' +_[-1].split('/')[0] == new_domain_url:
            self.__str_domain_url = new_domain_url
        
    @property
    def robots(self):
        """
        Get HTML of robots.txt of the website.
        """
        return Webpage(self.domain+'/robots.txt').html

class Webpage(object):
    def __init__(self, str_url):
        self.__str_url = None
        self.__str_html = None
        
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
        return self.__str_html    
    @html.setter
    def html(self, str_html):
        self.__str_html = str_html

    def request(self):
        headers = {'User-agent': 'wswp'}
        http = urllib3.PoolManager()
        response = http.request('GET', self.__str_url, headers = headers)
        if response.status == 200:
            self.html = response.data.decode('utf-8') 
        else:
            if response.status >= 500 and response.status < 600:
                response = http.request('GET', self.__str_url, retries=5)            
                if response.status != 200:
                    self.html = None
                else:
                    self.html = response.data.decode('utf-8')
            else:
                self.html = None
        if self.html:
            return True
        else:
            return False

def get_links(str_html, str_filter_regex=None):
    """
    Returns a list of links from given html.
    
    Parameters
    ----------
    str_html : str
        HTML from which to search for links.
    str_filter_regex : str, optional
        Regular expression pattern to filter links founds from given HTML 
        (the default is `None`, which implies all links found in given HTML will
        be returned by function.
    
    Return
    ------
    list
        links found within given HTML
    """
    links_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',
                           re.IGNORECASE)
    links = links_regex.findall(str_html)  
    if str_filter_regex:
        filter_regex = re.compile(str_filter_regex)
        return [link for link in links if filter_regex.match(link)]   
    else:
        return links

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
    
#    ws = Website('https://careers.pageuppeople.com/688/cwlive/en/listing/')
    wp = Webpage('https://www.bloomberg.com/asia')
    wp.request()
    html = wp.html
    links = get_links(str(html))
    links = [link for link in links if 'news' in link]