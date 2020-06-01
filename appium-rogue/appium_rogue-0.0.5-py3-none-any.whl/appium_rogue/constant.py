# -*- coding: utf-8 -*-
from .log import *

WAIT_TIME = 20
CITM = 'citm'
SMOKE = 'smoke'
skippedFuncNameList = ['find_with_raise', 'return_result', 'return_success', 'check_finished']
STALE = 'stale'

CRITICAL = "critical"
BLOCKER = "blocker"
NORMAL = 'normal'


class CASELEVEL:
    P0 = 'P0'
    P1 = 'P1'


class LogLevel:
    VERBOSE = 'verbose'
    DEBUG = 'debug'
    INFO = 'info'
    WARN = 'warn'
    ERROR = 'error'


class Framework:
    CASE_DIR = 'app_ui_test/cases'


class ENV:
    ENV_TEST = 'test'
    ENV_PRODUCTION = 'prod'


class CITMProxy:
    DEFAULT = 'http://127.0.0.1:8080'


class App:
    SQB = 'sqb'


class Appium:
    HOST = '127.0.0.1'
    PORT = '4725'
    IMPLICITLY_WAIT = '1'


class Deprecated_Account:
    username = '10900000001'
    password = '123456'
    default_merchant = None


class Platform:
    ANDROID = 'Android'
    IOS = 'iOS'


class AutomationName:
    APPIUM = 'appium'
    UI_AUTOMATOR2 = 'uiautomator2'
    XCUITEST = 'XCUITest'


class ElementAttribute:
    ACCESSIBILITY_ID = 'accessibility id'
    ID = 'id'
    TEXT = 'text'
    CLASS_NAME = 'class name'
    NAME = 'name'
    INDEX = 'index'
    CHECKED = 'checked'
    ENABLED = 'enabled'
    SELECTED = 'selected'
    BOUNDS = 'bounds'


class AndroidShellCMD:
    GET_APP_VERSION = 'adb -s {udid} shell dumpsys package {appPackage}|grep -oe "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*"'
    GET_APP_VERSION_2 = 'adb -s {udid} shell dumpsys package {appPackage}|grep -oe "[0-9]*\.[0-9]*\.[0-9]*"'
    GET_APP_VERSION_3 = 'adb -s {udid} shell dumpsys package {appPackage}|grep versionName|cut -d "=" -f 2'
    GET_SYSTEM_VERSION = 'adb -s {udid} shell getprop ro.build.version.release'
    GET_SDK_VERSION = 'adb -s {udid} shell getprop ro.build.version.sdk'
    OPEN_PROXY = 'adb -s {udid} shell am start -n tk.elevenk.proxysetter/.MainActivity -e host {host} -e port 8080 -e ssid Shouqianba -e key wosai2015ID007'
    CLOSE_PROXY = 'adb -s {udid} shell am start -n tk.elevenk.proxysetter/.MainActivity -e host {host} -e port 8080 -e ssid Shouqianba -e key wosai2015ID007 -e clear true'
    FIND_IME = 'adb -s {udid} shell dumpsys package io.appium.android.ime|grep -o versionName'
    LOGCAT = "adb -s {udid} logcat -v raw"
    SURFACEFLINGER = "adb -s {udid} shell dumpsys SurfaceFlinger|grep -ie 'layer .*)'| grep -v com.github.uiautomator |grep -v com.android.settings | grep -v DockedStackDivider|grep -v InputMethod|grep -v PopupWindow|grep -v Toast|grep -A 99 ImageWallpaper|grep -v ImageWallpaper|grep -B 99 StatusBar|grep -v StatusBar|cut -d '(' -f2|cut -d '/' -f2|cut -d ')' -f1|cut -d '#' -f1"
    SURFACEFLINGER_HUAWEI = "adb -s {udid} shell dumpsys SurfaceFlinger|grep -A 99 'layers:'|grep -B 99 'state:' | grep -ie '.*#.*' | grep -v com.github.uiautomator | grep -v NavigationBar | grep -v StatusBar |grep -v Toast| grep -v Layer| cut -d '(' -f2|cut -d '/' -f2|cut -d ')' -f1|cut -d '#' -f1"
    SURFACEFLINGER_Q = "adb -s {udid} shell dumpsys SurfaceFlinger --list |  grep '^{appPackage}' | cut -d '(' -f2|cut -d '/' -f2|cut -d ')' -f1|cut -d '#' -f1"
    HIDE_FLOATING_MENU = "adb -s {udid} shell am broadcast -a io.appetizer.agent.FloatingMenu --ez enabled false"
    UPLOAD_FOR_ANALYSIS = "adb -s {udid} shell am broadcast -a io.appetizer.agent.UploadForAnalysis"
    FORCE_STOP_APP = "adb -s {udid} shell am force-stop {appPackage}"
    GET_SCREEN_RESALUTION= "adb -s {udid} shell wm size | cut -d ':' -f2 |sed 's/ //g' "
    URLSCHEME = "adb -s {udid} shell am start -n {appPackage}/.ui.intent.IntentHandlerActivity -d {urlscheme}"

class AndroidPowerShellCMD:
    GET_APP_VERSION = "adb -s {udid} shell dumpsys package {appPackage}| where {{$_ -match '[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*'}}"
    GET_APP_VERSION_2 = "adb -s {udid} shell dumpsys package {appPackage}| where {{$_ -match '[0-9]*\.[0-9]*\.[0-9]*'}} | %{{($_ -split '=')[1]}}"
    GET_APP_VERSION_3 = 'adb -s {udid} shell dumpsys package {appPackage}| where {{$_ -match "versionName"}} | %{{($_ -split "=")[1]}}'
    GET_SYSTEM_VERSION = 'adb -s {udid} shell getprop ro.build.version.release'
    GET_SDK_VERSION = 'adb -s {udid} shell getprop ro.build.version.sdk'
    OPEN_PROXY = 'adb -s {udid} shell am start -n tk.elevenk.proxysetter/.MainActivity -e host {host} -e port 8080 -e ssid Shouqianba -e key wosai2015ID007'
    CLOSE_PROXY = 'adb -s {udid} shell am start -n tk.elevenk.proxysetter/.MainActivity -e host {host} -e port 8080 -e ssid Shouqianba -e key wosai2015ID007 -e clear true'
    FIND_IME = 'adb -s {udid} shell dumpsys package io.appium.android.ime | where {{$_ -match "versionName"}}'
    LOGCAT = "adb -s {udid} logcat -v raw"
    SURFACEFLINGER_HUAWEI = "adb -s {udid} shell dumpsys SurfaceFlinger --list | where {{$_ -match '^{appPackage}'}} | where {{$_.split('\\r\\n')}} | ForEach-Object{{(($_ -split '#')[0]).Trim()}}| ForEach-Object{{(($_ -split '/')[1]).Trim()}}"
    HIDE_FLOATING_MENU = "adb -s {udid} shell am broadcast -a io.appetizer.agent.FloatingMenu --ez enabled false"
    UPLOAD_FOR_ANALYSIS = "adb -s {udid} shell am broadcast -a io.appetizer.agent.UploadForAnalysis"
    FORCE_STOP_APP = "adb -s {udid} shell am force-stop {appPackage}"
    GET_SCREEN_RESALUTION= "adb shell wm size | where {$_.split('\\r\\n')} | ForEach-Object{(($_ -split ':')[1]).Trim()}"


class IOSShellCMD:
    GET_SYSTEM_VERSION = 'ideviceinfo -u {udid}|grep ProductVersion|grep -oe "[0-9]*\.[0-9]*\.[0-9]*"'
    GET_APP_VERSION = 'mobiledevice get_app_prop -t 2 -u {udid} {appPackage} CFBundleShortVersionString'


class MacShellCMD:
    GET_WIFI_IP = "Get-NetIPAddress | where {($_.InterfaceAlias -eq '以太网') -and ($_.AddressFamily -eq 'IPv4')} | select -exp ipaddress"
    GET_U2_PORT = "lsof -iTCP -sTCP:LISTEN -nP|grep -v 5037|grep adb|grep -oe '127.0.0.1:[0-9]*'|awk -F ':' '{print $2}'"
    FIND_CHARLES = "lsof -iTCP -sTCP:LISTEN -nP|grep Charles|cut -d ':' -f2|cut -d ' ' -f1"
    FIND_LOGCAT = "ps aux|grep '{logcat}'|grep -v grep"
    KILL_LOGCAT = "kill `ps aux|grep '{logcat}'|grep -v grep|awk '{{print $2}}'`"
    FIND_CHROMEDRIVER = "ps aux|grep '/usr/bin/chromedriver --url-base=wd/hub --port=8000 --adb-port=5037 --verbose'|grep -v grep"
    KILL_CHROMEDRIVER = "kill `ps aux|grep '/usr/bin/chromedriver --url-base=wd/hub --port=8000 --adb-port=5037 --verbose'|grep -v grep|awk '{{print $2}}'`"
    ADB_DEVICES = "adb devices|grep -e .|grep -v List|awk '{print $1}'"
    IOS_DEVICES = 'idevice_id -l'
    FIND_IPROXY = "ps aux|grep -v grep|grep -i 'iproxy 8100'|awk '{print$2}'"
    KILL_IPROXY = "kill -9 `ps aux|grep -v grep|grep -i 'iproxy 8100'|awk '{print$2}'`"

class WindowsShellCMD:
    GET_WIFI_IP = "Get-NetIPAddress | where {($_.InterfaceAlias -eq '以太网') -and ($_.AddressFamily -eq 'IPv4')} | select -exp ipaddress"
    GET_ADB_PID = "Get-CimInstance Win32_Process | where {($_.Name -eq 'adb.exe') -and ($_.CommandLine -notlike '*5037*')} | select -exp ProcessId"
    GET_U2_PORT = "Get-NetTCPConnection | where {{($_.LocalPort -ne '5037') -and ($_.LocalAddress -eq '127.0.0.1') -and ($_.State -eq 'listen') -and ($_.OwningProcess -eq '{pid}')}} | select -exp LocalPort"
    GET_FIDDLER_PID = "Get-Process | where {$_.name -eq 'fiddler'} | select -exp id"
    FIND_FIDDLER = "Get-NetTCPConnection | where {{($_.OwningProcess -eq '{pid}') -and ($_.State -eq 'listen')}} | select -exp LocalPort"
    FIND_LOGCAT = "Get-CimInstance Win32_Process | where {($_.Name -eq 'adb.exe') -and ($_.CommandLine -like '*logcat*')} | select -exp ProcessId"
    KILL_LOGCAT = "Get-Process -id '{logcatPid}' | kill"
    FIND_CHROMEDRIVER = "Get-CimInstance Win32_Process | where {($_.Name -eq 'chromedriver.exe') -and ($_.CommandLine -like '*--adb-port=5037*')} | select -exp ProcessId"
    KILL_CHROMEDRIVER = "Get-Process -id '{chromedriverPid}' | kill"
    ADB_DEVICES = "adb devices | where {$_.split('\\n')} |where {$_ -notlike '*List*'} |  ForEach-Object{($_ -split '\\s+')[0]}"
    FIND_APPIUM = "Get-CimInstance Win32_Process | where {($_.Name -eq 'node.exe') -and ($_.CommandLine -like '*appium*')} | select -exp ProcessId"
    FIND_APPIUM_DESKTOP = "Get-CimInstance Win32_Process | where {($_.Name -eq 'Appium.exe')}"

class IME:
    APPIUM = 'io.appium.settings/.AppiumIME'



class ScrollDirection:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class Version:

    @staticmethod
    def to_int_list(ver):
        vs = list(map(int, ver.split(".")))
        if len(vs) < 3:
            [vs.append(0) for _ in range(3 - len(vs))]
        elif len(vs) > 3:
            raise ValueError("bad version format")
        return vs

    @staticmethod
    def _compare(a, b):
        for i in range(3):
            if a[i] > b[i]:
                return 1
            if a[i] < b[i]:
                return -1
        return 0

    def __init__(self, ver: str):
        self._version = self.to_int_list(ver)

    def __repr__(self):
        return "<version: {}>".format(self._version)

    def __str__(self):
        return ".".join(map(str, self._version))

    def compare(self, other: str):
        if isinstance(other, Version):
            return self._compare(self._version, other._version)
        else:
            other = self.to_int_list(other)
            return self._compare(self._version, other)

    def __eq__(self, other):
        if self.compare(other) == 0:
            return True
        return False

    def __ne__(self, other):
        if self.compare(other) == 0:
            return False
        return True

    def __gt__(self, other):
        if self.compare(other) == 1:
            return True
        return False

    def __ge__(self, other):
        if self.compare(other) in (0, 1):
            return True
        return False

    def __lt__(self, other):
        if self.compare(other) == -1:
            return True
        return False

    def __le__(self, other):
        if self.compare(other) in (-1, 0):
            return True
        return False


def version_compare(target_version, base_version):
    """版本号比对"""
    v1_list = target_version.split('.')
    v2_list = base_version.split('.')
    v = 0
    v1_len = len(v1_list)
    v2_len = len(v2_list)
    if v1_len > v2_len:
        for i in range(v1_len - v2_len):
            v2_list.append('0')
    elif v2_len > v1_len:
        for i in range(v2_len - v1_len):
            v1_list.append('0')
    else:
        ...
    for i, v in enumerate(v1_list):
        if int(v1_list[i]) > int(v2_list[i]):
            return True
        if int(v1_list[i]) < int(v2_list[i]):
            return False
    return True


def asyncio_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


def merge_multi_dicts(*dict_args):
    """
    合并多个dict
    :param dict_args: 字段
    :return:
    """
    result = {}
    for temp_dict in dict_args:
        result.update(temp_dict)
    return result


class ItemMap:
    """pytest 用例收集处理类"""

    listdict = {}

    def put(self, key, item):
        initversion = item.get_closest_marker("initversion").args[0]
        if key in self.listdict:
            listitem = self.listdict.get(key)
            listitem[initversion] = item
        else:
            listitem = {initversion: item}
            self.listdict[key] = listitem
            self.listdict.values()

    """过滤出符合当前app的用例
        数据结构
    [caseid:[initversion:item,initversion1:item1]]
    :param initversion
    :return [caseid:item]
    """
    def filter(self, initversion: str):
        resultdict = {}
        items = self.listdict.items()
        for caseid, value in items:
            itemlist = list(value.items())
            print(itemlist)
            if len(itemlist) > 1:
                for i in range(len(itemlist) - 1):
                    for j in range(len(itemlist) - i - 1):
                        ver1, tmp1 = itemlist[j]
                        ver2, tmp2 = itemlist[j + 1]
                        if version_compare(ver1, ver2):
                            itemlist[j], itemlist[j + 1] = itemlist[j + 1], itemlist[j]
                    version, item = itemlist[len(itemlist) - 1 - i]
                    if version_compare(initversion, version):
                        resultdict[caseid] = item
                        break
                    version, item = itemlist[len(itemlist) - 1 - i]
                    resultdict[caseid] = item
            else:
                version, item = list(itemlist)[-1]
                resultdict[caseid] = item
        return resultdict
