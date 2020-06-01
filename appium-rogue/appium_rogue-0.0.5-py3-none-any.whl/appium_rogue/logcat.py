# -*- coding: utf-8 -*-
from .environment import *


@attrs
class Request:
    method = attrib()
    scheme = attrib()
    domain = attrib()
    path = attrib()
    parameters = attrib()
    protocol = attrib()
    headers = attrib()
    size = attrib(default=None)


@attrs
class Response:
    method = attrib()
    scheme = attrib()
    domain = attrib()
    path = attrib()
    parameters = attrib()
    headers = attrib()
    body = attrib()
    elapsed = attrib(converter=int)
    code = attrib(converter=int)
    size = attrib(converter=int)


@attrs
class Context:
    request = attrib()
    response = attrib()


class _Logcat(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__running = threading.Event()
        self.__running.set()
        self.requests = {}
        self.contexts = {}
        self.loading = False
        self.onDown = False
        self.onPostReq = False
        self.onGetReq = False
        self.onRes = False
        self.readHeaders = False
        self.readBody = False
        self.scheme = None
        self.domain = None
        self.path = None
        self.protocol = None
        self.method = None
        self.headers = {}
        self.parameters = None
        self.body = ''
        self.elapsed = None
        self.code = None
        self.size = None
        self.ahcON = False
        self.adb = None
        with open('logcat.log', 'w', encoding='utf8') as f:
            return

    @property
    def cmd(self):
        return AndroidShellCMD.LOGCAT.format(udid=env.udid)

    def run(self):
        kill_logcat(self.cmd)
        self.adb = Popen(self.cmd, stdin=PIPE, stdout=PIPE, shell=True)
        while self.adb.poll() is None and self.__running.isSet():
            try:
                line = self.adb.stdout.readline().decode('utf-8', 'replace').replace('\n', '')
            except KeyboardInterrupt:
                break
            with open('logcat.log', 'a+', encoding='utf8') as f:
                f.write(colored(Logging.get_now_time() + ' ' + line + '\n', 'white'))
            # self.analysisHttpContexts(line)
            # self.determineLoading(line)

    def analysisHttpContexts(self, line):
        if self.ahcON:
            if not self.onGetReq and line.startswith('--> GET'):
                searchObj = re.search('([^ ]*)://([^/]*)(/[^?]*)\?([^ ]*) (.*)', line)
                self.scheme = searchObj.group(1)
                self.domain = searchObj.group(2)
                self.path = searchObj.group(3)
                self.parameters = searchObj.group(4)
                self.protocol = searchObj.group(5)
                self.method = 'get'
                self.onGetReq = True
                self.readHeaders = True
                self.headers = {}
                return
            if not self.onPostReq and line.startswith('--> POST'):
                searchObj = re.search('([^ ]*)://([^/]*)(/[^ ]*) (.*)', line)
                self.scheme = searchObj.group(1)
                self.domain = searchObj.group(2)
                self.path = searchObj.group(3)
                self.protocol = searchObj.group(4)
                self.method = 'post'
                self.onPostReq = True
                self.readHeaders = True
                self.headers = {}
                return
            if self.onGetReq:
                if self.readHeaders:
                    if ': ' in line:
                        self.headers[line.split(': ')[0]] = line.split(': ')[1]
                        return
                    self.readHeaders = False
                if line == '--> END GET':
                    self.onGetReq = False
                    key = self.path + '?' + self.parameters
                    if self.requests.get(key, None):
                        Logging.warn('[duplicate get request]:' + key)
                    self.requests[key] = Request(
                        self.method, self.scheme, self.domain, self.path,
                        {x.split('=')[0]: x.split('=')[1] for x in self.parameters.split('&')},
                        self.protocol, self.headers)
                    Logging.debug('[get request]:' + key)
                return
            if self.onPostReq:
                if self.readHeaders:
                    if ': ' in line:
                        self.headers[line.split(': ')[0]] = line.split(': ')[1]
                        return
                    else:
                        self.readHeaders = False
                        self.parameters = line
                if line.startswith('--> END POST'):
                    searchObj = re.search('[^\d]*(\d+)[^\d]*', line)
                    self.onPostReq = False
                    self.size = searchObj.group(1)
                    if self.requests.get(self.path, None):
                        Logging.warn('[duplicate post request]:' + self.path)
                    self.requests[self.path] = Request(
                        self.method, self.scheme, self.domain, self.path,
                        {x.split('=')[0]: x.split('=')[1] for x in self.parameters.split('&')},
                        self.protocol, self.headers, self.size)
                    Logging.debug('[post request]:' + key)
                    return
            if not self.onRes and line.startswith('<-- '):
                if '?' not in line:
                    searchObj = re.search('(\d*)  ([^ ]*)://([^/]*)(/[^ ]*) \((\d*)', line)
                    self.method = 'post'
                    self.parameters = None
                    self.code = searchObj.group(1)
                    self.scheme = searchObj.group(2)
                    self.domain = searchObj.group(3)
                    self.path = searchObj.group(4)
                    self.elapsed = searchObj.group(5)
                    self.onRes = True
                    self.readHeaders = True
                    self.headers = {}
                    self.body = ''
                    return
                else:
                    searchObj = re.search('(\d*)  ([^ ]*)://([^/]*)(/[^?]*)\?([^ ]*) \((\d*)', line)
                    self.method = 'get'
                    self.code = searchObj.group(1)
                    self.scheme = searchObj.group(2)
                    self.domain = searchObj.group(3)
                    self.path = searchObj.group(4)
                    self.parameters = searchObj.group(5)
                    self.elapsed = searchObj.group(6)
                    self.onRes = True
                    self.readHeaders = True
                    self.headers = {}
                    self.body = ''
                    return
            if self.onRes:
                if self.readHeaders:
                    if ': ' in line:
                        self.headers[line.split(': ')[0]] = line.split(': ')[1]
                        return
                    self.readHeaders = False
                    self.readBody = True
                if self.readBody:
                    self.body += line + '\n'
                    if line.startswith('<-- END HTTP'):
                        searchObj = re.search('\((\d*)-', line)
                        self.size = searchObj.group(1)
                        self.body = json.loads(self.body)
                        self.readBody = False
                        self.onRes = False
                        if self.method == 'post':
                            self.parameters = self.requests[self.path].parameters
                            self.contexts[self.path] = Context(
                                self.requests[self.path],
                                Response(self.method, self.scheme, self.domain, self.path,
                                         self.parameters, self.headers, self.body, self.elapsed,
                                         self.code, self.size))
                        else:
                            self.contexts[self.path + '?' + self.parameters] = Context(
                                self.requests[self.path],
                                Response(self.method, self.scheme, self.domain, self.path,
                                         self.parameters, self.headers, self.body, self.elapsed,
                                         self.code, self.size))
                return

    def determineLoading(self, line):
        if not (self.onGetReq or self.onRes or self.onPostReq):
            if not self.loading:
                if line == 'showLoading':
                    self.startLoading(line)
                elif line.startswith("s7zInited"):
                    self.startLoading(line)
                elif line == 'createWebView':
                    self.startLoading(line)
                elif line.startswith('onPageStarted'):
                    self.startLoading(line)
                elif line.startswith('onDown'):
                    self.startLoading(line)
                    self.onDown = True
            else:
                if line == 'hideLoading':
                    self.endLoading(line)
                elif line == 'onResume called before onPause':
                    self.endLoading(line)
                elif line == 'stopLoading':
                    self.endLoading(line)
                elif 'ReceiveDispatchResponseListener respond update cycle' in line:
                    if self.onDown:
                        self.onDown = False
                        self.endLoading(line)
                elif line.startswith('domready'):
                    self.endLoading(line)
                elif line.startswith('MONITOR_PERFORMANCE') and 'pageLoad' in line:
                    self.endLoading(line)

    def ahcOpen(self):
        self.ahcON = True

    def ahcClose(self):
        self.ahcON = False

    def startLoading(self, line):
        self.loading = True
        Logging.info('[start loading]:' + line)

    def endLoading(self, line):
        self.loading = False
        Logging.info('[end loading]:' + line)

    def stop(self):
        self.__running.clear()
        self.adb.terminate()

    def reset(self):
        self.__running.set()
        self.loading = False

    def isLoading(self):
        return self.loading


logcat = _Logcat()
