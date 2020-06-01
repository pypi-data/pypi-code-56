# -*- coding: utf-8 -*-
from .constant import *
import platform
from .powershell import *


def force_stop_app(udid, appPackage):
    """强制关闭App，只支持Android"""
    Logging.info('force_stop_app')
    return os.popen(AndroidShellCMD.FORCE_STOP_APP.format(udid=udid,
                                                          appPackage=appPackage)).read().strip()


def hide_floating_menu(udid):
    """隐藏Appetizer的浮窗，只支持Android"""
    Logging.info('hide_floating_menu')
    return os.popen(AndroidShellCMD.HIDE_FLOATING_MENU.format(udid=udid)).read().strip()


def upload_for_analysis(udid):
    """上传Appetizer的log，只支持Android"""
    Logging.info('upload_for_analysis')
    return os.popen(AndroidShellCMD.UPLOAD_FOR_ANALYSIS.format(udid=udid)).read().strip()


def get_surfaceflinger(udid, platformversion, appPackage):
    """获取surfaceflinger，只支持Android"""
    sysstr = platform.system()
    if (sysstr == "Windows"):
        with PowerShell('GBK') as ps:
            p, errs = ps.run(AndroidPowerShellCMD.SURFACEFLINGER_HUAWEI.format(udid=udid, appPackage=appPackage))
        return p.strip().split('\r\n')
    else:
        cmd = AndroidShellCMD.SURFACEFLINGER_Q
        # if version_compare(platformversion, '8.0'):
        #     cmd = AndroidShellCMD.SURFACEFLINGER_HUAWEI
        # else:
        #     cmd = AndroidShellCMD.SURFACEFLINGER
        return os.popen(cmd.format(udid=udid, appPackage=appPackage)).read().strip().split('\n')


def find_ime(udid):
    """判断是否安装了appium的ime，只支持Android"""
    sysstr = platform.system()
    if (sysstr == "Windows"):
        with PowerShell('GBK') as ps:
            p, errs = ps.run(AndroidPowerShellCMD.FIND_IME.format(udid=udid))
            p = p.strip()
    else:
        cmd = AndroidShellCMD.FIND_IME.format(udid=udid)
        p = os.popen(cmd).read().strip()
    if 'versionName' in p:
        return True
    return False


def proxy_on(udid):
    """使手机连接citm的代理，只支持Android"""
    host = get_wifi_ip()
    cmd = AndroidShellCMD.OPEN_PROXY.format(udid=udid, host=host)
    p = os.popen(cmd).read().strip()
    return p


def proxy_off(udid):
    """关闭手机连接citm的代理，只支持Android"""
    host = get_wifi_ip()
    cmd = AndroidShellCMD.CLOSE_PROXY.format(udid=udid, host=host)
    p = os.popen(cmd).read().strip()
    return p


def get_app_version(udid, appPackage, pt):
    """获取app的版本号"""

    def run_cmd(*args):
        for arg in args:
            if os.popen(arg).read():
                return os.popen(arg).read().strip()

    def run_powershellcmd(*args):
        for arg in args:
            with PowerShell('GBK') as ps:
                out, errs = ps.run(arg)
            if out:
                return out;

    if pt is Platform.ANDROID:
        sysstr = platform.system()
        if (sysstr == "Windows"):
            p = run_powershellcmd(AndroidPowerShellCMD.GET_APP_VERSION_3.format(udid=udid, appPackage=appPackage),
                                  AndroidPowerShellCMD.GET_APP_VERSION_2.format(udid=udid, appPackage=appPackage),
                                  AndroidPowerShellCMD.GET_APP_VERSION.format(udid=udid, appPackage=appPackage))
            print(p)
            p = p.strip()
        else:
            p = run_cmd(AndroidShellCMD.GET_APP_VERSION_3.format(udid=udid, appPackage=appPackage),
                        AndroidShellCMD.GET_APP_VERSION_2.format(udid=udid, appPackage=appPackage),
                        AndroidShellCMD.GET_APP_VERSION.format(udid=udid, appPackage=appPackage))
    else:
        cmd = IOSShellCMD.GET_APP_VERSION.format(udid=udid, appPackage=appPackage)
        p = os.popen(cmd).read().strip()
    return '.'.join(p.split('.')[:3])


def get_screen_reacts(udid, pt):
    """获取屏幕真实分辨率"""
    if pt is Platform.ANDROID:
        sysstr = platform.system()
        if (sysstr == "Windows"):
            with PowerShell('GBK') as ps:
                p, errs = ps.run(AndroidPowerShellCMD.GET_SCREEN_RESALUTION.format(udid=udid))
                p = p.strip()
        else:
            cmd = AndroidShellCMD.GET_SCREEN_RESALUTION.format(udid=udid)
            p = os.popen(cmd).read().strip()
    else:
        cmd = ""
        p = ""
    width = p.split('x')[0]
    height = p.split('x')[1]
    return {'width': int(width), 'height': int(height)}


def get_system_version(udid, pt):
    """获取系统的版本号"""
    if pt is Platform.ANDROID:
        cmd = AndroidShellCMD.GET_SYSTEM_VERSION.format(udid=udid)
    else:
        cmd = IOSShellCMD.GET_SYSTEM_VERSION.format(udid=udid)
    # sysstr = platform.system()
    # if(sysstr == "Windows"):
    #     with PowerShell('GBK') as ps:
    #         cmd = AndroidPowerShellCMD.GET_SYSTEM_VERSION.format(udid=udid)
    #         print(cmd)
    #         p = ps.run(cmd)
    # else:
    p = os.popen(cmd).read().strip().replace("\r\n", "")
    return p


def get_wifi_ip():
    """获取开启citm设备的无线ip地址，只支持Mac"""
    sysstr = platform.system()
    if (sysstr == "Windows"):
        with PowerShell('GBK') as ps:
            outs, errs = ps.run(WindowsShellCMD.GET_WIFI_IP)
        return outs.strip()
    else:
        return os.popen(MacShellCMD.GET_WIFI_IP).read().strip()


def get_u2_port():
    """获取uiautomator2的端口，只支持Mac"""
    sysstr = platform.system()
    if (sysstr == "Windows"):
        with PowerShell('GBK') as ps:
            pid, errs = ps.run(WindowsShellCMD.GET_ADB_PID)
        with PowerShell('GBK') as ps:
            port, errs = ps.run(WindowsShellCMD.GET_U2_PORT.format(pid=pid))
        return port.strip()
    else:
        return os.popen(MacShellCMD.GET_U2_PORT).read().strip()


def get_charles_port():
    """获取Charles的端口，只支持Mac"""
    sysstr = platform.system()
    if (sysstr == "Windows"):
        with PowerShell('GBK') as ps:
            pid, errs = ps.run(WindowsShellCMD.GET_FIDDLER_PID)
        with PowerShell('GBK') as ps:
            port, errs = ps.run(WindowsShellCMD.FIND_FIDDLER.format(pid=pid))
        return port
    else:
        return os.popen(MacShellCMD.FIND_CHARLES).read().strip()


def kill_logcat(logcat):
    """kill未关闭的logcat进程，只支持Mac"""
    sysstr = platform.system()
    if (sysstr == "Windows"):
        with PowerShell('GBK') as ps:
            pid, errs = ps.run(WindowsShellCMD.FIND_LOGCAT)
        with PowerShell('GBK') as ps:
            if pid:
                return ps.run(WindowsShellCMD.KILL_LOGCAT.format(logcatPid=pid))
    else:
        if os.popen(MacShellCMD.FIND_LOGCAT.format(logcat=logcat)).read().strip():
            return os.popen(MacShellCMD.KILL_LOGCAT.format(logcat=logcat)).read().strip()


def kill_chromedriver():
    """kill未关闭的chromedriver进程，只支持Mac"""
    sysstr = platform.system()
    if (sysstr == "Windows"):
        with PowerShell('GBK') as ps:
            pid, errs = ps.run(WindowsShellCMD.FIND_CHROMEDRIVER)
        with PowerShell('GBK') as ps:
            if pid:
                return ps.run(WindowsShellCMD.KILL_CHROMEDRIVER.format(chromedriverPid=pid))
    else:
        if os.popen(MacShellCMD.FIND_CHROMEDRIVER).read().strip():
            return os.popen(MacShellCMD.KILL_CHROMEDRIVER).read().strip()


def get_adb_devices():
    """获取Android设备，只支持Mac"""
    sysstr = platform.system()
    if (sysstr == "Windows"):
        with PowerShell('GBK') as ps:
            out, errs = ps.run(WindowsShellCMD.ADB_DEVICES)
            return list(
                filter(lambda x: len(x) != 0,
                       out.strip().split('\n')))
    else:
        return list(
            filter(lambda x: len(x) != 0,
                   os.popen(MacShellCMD.ADB_DEVICES).read().strip().split('\n')))


def get_ios_devices():
    """获取iOS设备，只支持Mac"""
    sysstr = platform.system()
    if (sysstr == "Darwin"):
        return list(set(
            filter(lambda x: len(x) != 0,
                   os.popen(MacShellCMD.IOS_DEVICES).read().strip().split('\n'))))
    else:
        return list()


def kill_iproxy():
    """kill未关闭的iproxy，只支持Mac"""
    if os.popen(MacShellCMD.FIND_IPROXY).read().strip():
        return os.popen(MacShellCMD.KILL_IPROXY).read().strip()


def urlscheme_jump(udid, pt, scheme):
    """urlscheme跳转指定页面"""
    sysstr = platform.system()
    cmd = AndroidShellCMD.URLSCHEME.format(udid=udid, appPackage=pt, urlscheme=scheme)
    Logging.info(cmd)
    if sysstr == "Windows":
        with PowerShell('GBK') as ps:
            p, errs = ps.run(cmd)
            p = p.strip()
    else:
        p = os.popen(cmd).read().strip()
    return p
