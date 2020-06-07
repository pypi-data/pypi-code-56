#!c:/SDK/Anaconda2/python.exe
import os
import sys
import argparse
import clipboard
from configset import configset
from pydebugger.debug import debug
from make_colors import make_colors
import requests
from bs4 import BeautifulSoup as bs
from parserheader import parserheader
import re
from pywget import wget
import traceback
try:
    from . import js_exe
except:
    import js_exe
if sys.version_info.major == 3:
    import urllib.request, urllib.parse, urllib.error
else:
    import urllib as urllibx
    class urllib:
        def request(self):
            pass
        def parse(self):
            pass
        def error(self):
            pass
    urllib.request = urllibx
    urllib.parse = urllibx
    urllib.error = urllibx


class zippyshare(object):
    def __init__(self, url = None, download_path = os.getcwd(), altname = None):
        super(zippyshare, self)
        self.debug = False
        
        if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'zippyshare.ini')):
            configname = os.path.join(os.path.dirname(__file__), 'zippyshare.ini')
        else:
            configname = os.path.join(os.path.dirname(__file__), 'zippyshare.ini')
        self.config = configset(configname)        
        if url:
            self.url = url
            url_download = self.generate(self.url)
            self.download(url_download, download_path, altname)
        
        
    def generate(self, url):
        #header = self.parseheader()
        debug(url = url)
        #print("url =", url)
        www = re.findall('https:/.(.*?).zippyshare', url)[0]
        #print("www =", www)
        debug(www = www, debug = self.debug)
        header = {}
        while 1:
            try:
                a = requests.get(url, headers = header)
                break
            except:
                pass
        b = bs(a.content, 'lxml')
        try:
            js_script = b.find("div", {'class': 'center',}).find_all("script")[1]
        except:
            js_script = b.find("div", {'class': 'right',}).find_all("script")[0]
        #clipboard.copy(str(js_script))
        debug(js_script = js_script)
        js_content = ""
        a_script = re.findall("\(.*?\)", str(js_script))
        debug(a_script = a_script)
        b_script = re.split("\(|\)|%|\+", str(a_script[1]))
        debug(b_script = b_script)
        js_content1 = int(b_script[1].strip())
        debug(js_content1 = js_content1)
        js_content2 = int(b_script[2].strip())
        debug(js_content2 = js_content2)
        js_content3 = int(b_script[3].strip())
        debug(js_content3 = js_content3)
        js_content4 = int(b_script[4].strip())
        debug(js_content4 = js_content4)
        #js_content = ((js_content1 % js_content2) + (js_content3 + js_content4))
        #debug(js_content = js_content)
        js_content = """
        var a = %d %% %d;
        var b = %d %% %d;
        var x = a + b;
        
        """%(js_content1, js_content2, js_content3, js_content4)
        #print "js_content =", js_content
        js_content = js_exe.generator(js_content, "x")
        debug(js_content = js_content)
        meta_file = b.find('meta', {'name': 'twitter:title',}).get('content').strip()
        meta_file = urllib.parse.quote(meta_file)
        debug(meta_file = meta_file, debug = self.debug)
        
        code_download_html = b.find('div', {'id': 'lrbox',}).find_all('script')[2].text
        debug(code_download_html = code_download_html, debug = self.debug)
        code_download = re.findall('document.getElementById\(\'dlbutton\'\).href = "/d/(.*?)/+', code_download_html)
        debug(code_download = code_download, debug = self.debug)
        code_download = code_download[0]
        debug(code_download = code_download)
        
        #url_download = 'https://' + str(www) + ".zippyshare.com/d/" + str(code_download) + '/' + str(time_id) + '/' + str(meta_file)
        url_download = 'https://' + str(www) + ".zippyshare.com/d/" + str(code_download) + '/' + str(js_content) + '/' + str(meta_file)
        debug(url_download = url_download, debug = self.debug)
        return url_download
    
    def download(self, url, download_path = os.getcwd(), altname = None, prompt = False):
        try:
            import idm
            dm = idm.IDMan()
            dm.download(url, download_path, altname, confirm= prompt)
        except:
            if os.getenv('debug'):
                traceback.format_exc()
            if altname:
                download_path = os.path.join(download_path, altname)
            wget.download(url, download_path)
        
    def parseheader(self, header_text = None):
        default  = """
    HTTP/1.1 200 Connection established
Server: nginx
Date: Thu, 12 Sep 2019 10:03:26 GMT
Content-Type: text/html;charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Set-Cookie: JSESSIONID=8FFFF1380195C68BA0E0C2C960AD8B32; Path=/; HttpOnly
Set-Cookie: zippop=1; Domain=.zippyshare.com; Expires=Thu, 12-Sep-2019 22:03:26 GMT; Path=/
Content-Language: en
Expires: Thu, 12 Sep 2019 10:03:25 GMT
Cache-Control: no-cache
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Encoding: gzip
    """
        if not header_text: 
            header_text = self.config.read_config('header', 'text', value= default)
            debug(header_text = header_text, debug = self.debug)
        p = parserheader()
        header = p.parserHeader(header_text)
        debug(header = header, debug = self.debug)

    def usage(self):
        parser = argparse.ArgumentParser(formatter_class= argparse.RawTextHelpFormatter)
        parser.add_argument('URL', action = 'store', help = 'Zippyshare url, example: "https://www48.zippyshare.com/v/pedPCo05/file.html", type "c" for get url from clipboard')
        parser.add_argument('-p', '--download-path', action = 'store', help = 'Download path to save file')
        parser.add_argument('-n', '--name', action = 'store', help = 'Alternative Save as name')
        parser.add_argument('-P', '--prompt', action = 'store_true', help = 'Prompt Before download')
        parser.add_argument('-d', '--debug', action = 'store_true', help = 'Debugger process')
        parser.add_argument('-c', '--clipboard', action = 'store_true', help = 'Copy generated link to clipboard')
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            args = parser.parse_args()
            debug(debugger = args.debug)            
            if self.config.read_config('debug', 'debug', value= False):
                self.debug = eval(self.config.read_config('debug', 'debug', value= False))
                debug(self_debug = self.debug)
            self.debug = args.debug
            debug(self_debug = self.debug)            
            if args.URL == 'c':
                args.URL = clipboard.paste()
            url_download = self.generate(args.URL)
            if args.download_path:
                self.download(url_download, args.download_path, args.name, args.prompt)
            else:
                print(make_colors("GENERATED:", 'w', 'r') + " " + make_colors(url_download, 'b', 'ly', attrs= ['blink']))
                if args.clipboard:
                    clipboard.copy(url_download)                

if __name__ == '__main__':
    c = zippyshare()
    c.usage()