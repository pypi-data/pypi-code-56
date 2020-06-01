import time
import pkg_resources

import telnetlib

import xml.etree.ElementTree as ET
# from prettytable import PrettyTable
import requests
from threading import RLock

import logging
import logging.handlers
from digimat.jobs import JobManager


from .message import LutronMessageSYSTEM
from .message import LutronMessageMONITORING

from .collections import LutronObjectCollectionHVAC
from .collections import LutronObjectCollectionOUTPUT


class LutronXmldb(object):
    def __init__(self, gw):
        assert gw.__class__.__name__=='Lutron'
        self._gw=gw
        self._xml=None
        self._reset()

    def _reset(self):
        self._areas=None
        self._hvacs=None
        self._outputs=None

    @property
    def gw(self):
        return self._gw

    @property
    def logger(self):
        return self.gw.logger

    @property
    def xml(self):
        return self._xml

    @property
    def root(self):
        return self._root

    def _defaultFileName(self):
        return 'lutron-%s.xml' % self.gw.host

    def save(self, fpath=None):
        try:
            if not fpath:
                fpath=self._defaultFileName()
            self._xml.write(fpath)
            self.logger.info('xmldb saved to file %s' % fpath)
            return True
        except:
            self.logger.exception('save')

    def _store(self, xml):
        self._xml=None
        self._root=None
        try:
            self._root=xml.find('Areas').find('Area')
            self._project=self._root.get('Name')
            self.logger.info('Found project [%s]' % self._project)
            self._xml=xml
            self._reset()
            return True
        except:
            pass

    def loadFromFile(self, fpath=None):
        try:
            if not fpath:
                fpath=self._defaultFileName()
            self.logger.info('Loading xmldb from file %s...' % fpath)
            xml=ET.parse(fpath)
            if self._store(xml):
                return True
        except:
            pass

    def loadFromURL(self, url):
        try:
            self.logger.info('Loading xmldb from %s...' % url)
            r=requests.get(url)
            if r:
                xml=ET.ElementTree(ET.fromstring(r.text))
                if self._store(xml):
                    return True
        except:
            pass

    def load(self, port=80):
        url='http://%s:%d/DbXmlInfo.xml' % (self.gw.host, port)
        return self.loadFromURL(url)

    def _findAreas(self, root=None, areas=[]):
        try:
            if not root:
                root=self._root.find('Areas')
            for item in root.findall('Area'):
                areas.append(item)
                subitem=item.find('Areas')
                if subitem:
                    self._findAreas(subitem, areas)
        except:
            pass
        return areas

    def areas(self):
        if not self._areas:
            self._areas=self._findAreas()
        return self._areas

    def outputs(self, filterType=None, create=False):
        if not self._outputs:
            outputs=[]
            try:
                for area in self.areas():
                    try:
                        for item in area.find('Outputs').findall('Output'):
                            outputs.append(item)
                    except:
                        pass
            finally:
                self._outputs=outputs

        if self._outputs and filterType:
            filterType=filterType.lower()
            return [item for item in self._outputs if filterType in item.get('OutputType').lower()]

        return self._outputs

    def output(self, integrationId):
        try:
            for item in self.outputs():
                if int(item.get('IntegrationID'))==integrationId:
                    return item
        except:
            pass

    def declareOutputs(self):
        items=[]
        for item in self.outputs():
            integrationId=item.get('IntegrationID')
            items.append(self.gw.outputs.create(integrationId))
        return items

    def hvacs(self):
        if not self._hvacs:
            hvacs=[]
            try:
                for item in self._xml.find('HVACs').findall('HVAC'):
                    hvacs.append(item)
            finally:
                self._hvacs=hvacs

        return self._hvacs

    def hvac(self, integrationId):
        try:
            for item in self.hvacs():
                if int(item.get('IntegrationID'))==integrationId:
                    return item
        except:
            pass

    def declareHvacs(self):
        items=[]
        for item in self.hvacs():
            integrationId=item.get('IntegrationID')
            items.append(self.gw.hvacs.create(integrationId))
        return items

    def dump(self):
        for item in self.outputs():
            print(item.attrib)

        for item in self.hvacs():
            print(item.attrib)


class LutronLogger(object):
    def __init__(self, title="LUTRON"):
        self._title=title

    def create(self):
        return logging.getLogger(self._title)

    def tcp(self, level=logging.DEBUG, host='localhost'):
        logger=self.create()
        logger.setLevel(level)
        handler = logging.handlers.SocketHandler(host, logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        logger.addHandler(handler)
        return logger

    def null(self):
        logger=self.create()
        logger.setLevel(logging.ERROR)
        handler=logging.NullHandler()
        logger.addHandler(handler)
        return logger


class Lutron(object):

    USER_PROMPT = b'login: '
    PW_PROMPT = b'password: '
    PROMPT = b'GNET> '

    def __init__(self, host, user='lutron', password='lutron', port=23, readOnly=False, logger=None):
        if logger is None:
            logger=LutronLogger().tcp()
        self._logger=logger

        self._host=host
        self._user=user
        self._password=password
        self._port=int(port)

        self._hvacs=LutronObjectCollectionHVAC(self)
        self._outputs=LutronObjectCollectionOUTPUT(self)

        self._debug=False
        self._readOnly=readOnly
        self._telnet=None
        self._open=False
        self._rxBuffer=''
        self._timeoutTelnetInhibit=0
        self._timeoutRx=0
        self._timeoutPing=0
        self._activityCounter=0
        self._lockTelnet=RLock()
        self._db=LutronXmldb(self)
        self.start()

    def debug(self, state=True):
        self._debug=state

    def nodebug(self):
        self.debug(False)

    def isReadOnly(self):
        if self._readOnly:
            return True
        return False

    def setReadOnly(self, enable=True):
        self._readOnly=enable

    def isDebug(self):
        if self._debug:
            return True
        return False

    def getVersion(self):
        try:
            distribution=pkg_resources.get_distribution('digimat.lutron')
            return distribution.parsed_version
        except:
            pass

    @property
    def version(self):
        return self.getVersion()

    @property
    def logger(self):
        return self._logger

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def db(self):
        return self._db

    #  ---------------------------------------------

    @property
    def hvacs(self):
        return self._hvacs

    def hvac(self, integrationId):
        return self.hvacs.create(integrationId)

    @property
    def outputs(self):
        return self._outputs

    def output(self, integrationId):
        return self.outputs.create(integrationId)

    #  ---------------------------------------------

    @property
    def jobs(self):
        return self._jobs

    def isOpen(self):
        if self._telnet and self._open:
            return True
        return False

    def open(self):
        if self._telnet:
            return self._telnet

        try:
            if time.time()>=self._timeoutTelnetInhibit:
                result=False

                self._timeoutTelnetInhibit=time.time()+5.0
                self.logger.info('Opening Lutron telnet link to %s:%d' % (self._host, self._port))
                t=telnetlib.Telnet(self._host, self._port, timeout=2.0)

                self.logger.info('Opening session (user %s)' % self._user.encode('ascii'))
                if t.read_until(self.USER_PROMPT, timeout=2):
                    t.write(self._user.encode('ascii') + b'\r\n')
                    if t.read_until(self.PW_PROMPT, timeout=2):
                        t.write(self._password.encode('ascii') + b'\r\n')
                        if t.read_until(self.PROMPT, timeout=2):
                            result=True

                if result:
                    self.logger.info('session successfully opened!')
                    self._telnet=t
                    self._timeoutRx=time.time()+15.0

                    self.logger.info('configuring monitoring...')
                    m=LutronMessageMONITORING(self)
                    m.prompt(False)
                    m.all(False)
                    m.button(True)
                    m.led(True)
                    m.zone(True)
                    m.occupancy(True)
                    # m.scene(True)
                    m.hvac(True)

                    m=LutronMessageSYSTEM(self)
                    m.getOSrevision()
                    m.getTime()
                    m.getDate()

                    self._open=True

                    return self._telnet
                else:
                    self.logger.error('unable to open link session!')
                    try:
                        t.close()
                    except:
                        pass
        except:
            try:
                t.close()
            except:
                self.logger.error('unable to open link to gateway')
                # self.logger.exception('open()')

    def close(self):
        self._open=False
        try:
            if self._telnet:
                self.logger.info('telnet:close()')
                self._telnet.close()
        except:
            pass

        self._telnet=None

    def _send(self, cmd):
        if cmd:
            t=self.open()
            if t:
                with self._lockTelnet:
                    try:
                        self.logger.debug('--> %s', cmd)
                        t.write(cmd.encode('ascii') + b'\r\n')
                        self.wakeup()
                    except:
                        self.logger.exception('send')
                        self.close()

    def _receive(self):
        t=self.open()
        if t:
            with self._lockTelnet:
                try:
                    data=t.read_eager()
                    if data:
                        self._rxBuffer+=data.decode('ascii')
                        self._dispatch()
                        return True
                except EOFError:
                    self.close()
                except:
                    self.logger.exception('receive')

    def _dispatch(self):
        with self._lockTelnet:
            if self._rxBuffer:
                self.wakeup()
                try:
                    pos=self._rxBuffer.find('\r\n')
                    if pos>=0:
                        msg=self._rxBuffer[0:pos].strip()
                        self._rxBuffer=self._rxBuffer[pos+2:]
                        if msg:
                            self.logger.debug('<-- %s' % msg)
                            self._timeoutRx=time.time()+15
                            mtype=msg[0]

                            # EVENT
                            if mtype=='~':
                                data=msg[1:].split(',')
                                if data:
                                    topic=data[0]
                                    args=data[1:]
                                    if args:
                                        if not self._dispatchEvent(topic, *args):
                                            self.logger.warning('unhandled event %s' % msg)
                                    else:
                                        self._dispatchEvent(topic)
                            else:
                                self.logger.warning('unsupported message [%s]' % msg)

                except:
                    self.logger.exception('dispatch')
                return True

    def _dispatchEvent(self, topic, *args):
        try:
            # self.logger.debug('EVENT %s' % (topic))
            if topic=='HVAC':
                integrationId=args[0]
                obj=self._hvacs.get(integrationId)
                if obj:
                    return obj._dispatchEvent(*args[1:])
            elif topic=='OUTPUT':
                integrationId=args[0]
                obj=self._outputs.get(integrationId)
                if obj:
                    return obj._dispatchEvent(*args[1:])
            elif topic=='MONITORING':
                # NOP
                return True
            elif topic=='SYSTEM':
                # NOP
                return True
            elif topic=='ERROR':
                self.logger.error('%s%s' % (topic, args))
                # TODO: ??
                return True
        except:
            self.logger.exception('dispatchEvent %s %s' % (topic, args))

    def ping(self):
        m=LutronMessageSYSTEM(self)
        m.getTime()
        self._timeoutPing=time.time()+3.0

    def wakeup(self):
        self._activityCounter=64

    def _manager(self):
        now=time.time()

        self._receive()
        self._dispatch()

        self._hvacs.manager()
        self._outputs.manager()

        if now>=self._timeoutRx:
            if now>=self._timeoutPing:
                self.ping()
            if now-self._timeoutRx>=60:
                self.close()

        # Small booster, allowing to be more reactive
        # during data burst, and more sleepy when idle
        try:
            if self._activityCounter>0:
                # bypass default job manager sleep (0.1)
                self.sleep(0.01)
                self._activityCounter-=1
                return True
        except:
            pass

        return False

    def start(self):
        try:
            if self._jobs:
                return
        except:
            pass

        self._jobs=JobManager(self.logger)
        self._jobLutron=self._jobs.addJobFromFunction(self._manager)
        self._jobLutron.setDaemon()
        self._jobs.start()

        self.open()

    def stop(self):
        try:
            self._jobs.stop()
        except:
            pass
        self._jobLutron=None
        self._jobs=None

    def isRunning(self):
        try:
            return self._jobLutron.isRunning()
        except:
            pass
        return False

    def sleep(self, delay=1.0):
        try:
            self._jobLutron.sleep(delay)
        except:
            self.logger.exception('sleep')
            time.sleep(delay)

    def __del__(self):
        self.stop()

    def dump(self, matching=None):
        self._hvacs.dump(matching)
        self._outputs.dump(matching)

    def serveForEver(self):
        self.start()
        try:
            while self.isRunning():
                self.sleep(.250)
        except KeyboardInterrupt:
            pass
        self.stop()

    def __repr__(self):
        return '<%s:%s(%d objects)>' % (self.__class__.__name__, self.host, len(self._objects))


if __name__ == "__main__":
    pass
