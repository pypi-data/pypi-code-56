# -*- coding: utf-8 -*-
from hulk.utils.xml2list import ManifestXmlHandler
from .exceptions import *
from .shell import *


class _Env:
    _env = ENV.ENV_TEST
    _platform = Platform.ANDROID
    _citm_service = CITMProxy.DEFAULT
    _device = None
    _sqb_package = None
    _appActivity = None
    _sms_code = None
    _api_domain = None
    _mysql = None
    _redis = None
    _etcdtool = None
    _xcodeOrgId = None
    _xcodeSigningId = None
    app_ver = None
    module_router = None
    page_router = None
    Activities = None
    UDID = None
    popWindow = None
    _jenkins_buildid = None
    _activity_list = None

    @property
    def capabilities(self):
        config = {'udid': self.udid}
        config['deviceName'] = self.device
        config['platformName'] = self.platform
        config['platformVersion'] = get_system_version(self.udid, self.platform)
        if self.platform is Platform.ANDROID:
            config.update(self.sqb_package)
            config.update(self.appActivity)
            if version_compare(config['platformVersion'], '4.4'):
                config['automationName'] = AutomationName.UI_AUTOMATOR2
            else:
                config['automationName'] = AutomationName.APPIUM
            if not find_ime(self.udid):
                config['unicodeKeyboard'] = True
                config['resetKeyboard'] = True
            config['recreateChromeDriverSessions'] = True
            config['noSign'] = True
            config['showChromedriverLog'] = True
            config['disableWindowAnimation'] = True
            # config['settings[ignoreUnimportantViews]'] = True
            config['settings[waitForIdleTimeout]'] = 5000
            # config['noReset'] = True
            # config['dontStopAppOnReset'] = True
            # config['autoLaunch'] = False
            # config['chromeOptions'] = {'androidProcess': 'com.wosai.cashbar.beta2'}
            # config['newCommandTimeout'] = 9999
            # config['autoWebview'] = True
        else:
            config["automationName"] = AutomationName.XCUITEST
            config["bundleId"] = self.appPackage
            config["xcodeOrgId"] = self.xcodeOrgId
            config["xcodeSigningId"] = self.xcodeSigningId
        return config

    @property
    def app_version(self):
        return get_app_version(self.udid, self.appPackage, self.platform)

    @property
    def activity_list(self):
        return self._activity_list

    @property
    def appPackage(self):
        return self.sqb_package['appPackage']

    @property
    def udid(self):
        return self.UDID[self.device]

    @property
    def redis(self):
        return self._redis[self.app_env]

    @redis.setter
    def redis(self, value):
        self._redis = value

    @property
    def etcdtool(self):
        return self._etcdtool

    @etcdtool.setter
    def etcdtool(self, value):
        self._etcdtool = value

    @property
    def sqb_package(self):
        return self._sqb_package[self.app_env][self.platform]

    @sqb_package.setter
    def sqb_package(self, value):
        self._sqb_package = value

    @property
    def appActivity(self):
        return self._appActivity

    @appActivity.setter
    def appActivity(self, value):
        self._appActivity = value

    @property
    def app_env(self):
        return self._env

    @app_env.setter
    def app_env(self, value):
        self._env = value

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, value):
        self._platform = value

    @property
    def citm_service(self):
        return self._citm_service

    @citm_service.setter
    def citm_service(self, value):
        self._citm_service = value

    @property
    def sms_code(self):
        return self._sms_code[self.app_env]

    @sms_code.setter
    def sms_code(self, value):
        self._sms_code = value

    @property
    def api_domain(self):
        return self._api_domain[self.app_env]

    @api_domain.setter
    def api_domain(self, value):
        self._api_domain = value

    @property
    def mysql(self):
        return self._mysql[self.app_env]

    @mysql.setter
    def mysql(self, value):
        self._mysql = value

    @property
    def i(self):
        return self.platform is Platform.IOS

    @property
    def a(self):
        return self.platform is Platform.ANDROID

    @property
    def xcodeOrgId(self):
        return self._xcodeOrgId

    @xcodeOrgId.setter
    def xcodeOrgId(self, value):
        self._xcodeOrgId = value

    @property
    def xcodeSigningId(self):
        return self._xcodeSigningId

    @xcodeSigningId.setter
    def xcodeSigningId(self, value):
        self._xcodeSigningId = value


def clean():
    # 判断os是否有fwalk属性
    if hasattr(os, 'fwalk'):
        d_tree_generator = os.fwalk()

    else:
        d_tree_generator = os.walk('.')

    for x in d_tree_generator:
        for y in x[1]:
            if '__pycache__' in y:
                shutil.rmtree(x[0] + '/' + y)
        for y in x[2]:
            if 'hulk.log' in y:
                os.remove(x[0] + '/' + y)
                continue
            if y.endswith('.pyc') or y.endswith('.png'):
                if 'allure' in y:
                    continue
                os.remove(x[0] + '/' + y)


def list_dirs(path):
    """列出path目录下的文件夹"""
    ret = []
    for ele in os.listdir(path):
        p = ele if path == "." else join(path, ele)
        if isdir(p) and not ele.startswith(".") and not ele.startswith("_"):
            ret.append(p)
    return ret


def ignores(parent, *sub):
    """生成需要忽略的目录"""
    len_max = max([len(su) for su in sub])  # 路径深度
    for i in range(len_max):
        dirs_v2 = set()  # 当前层级下的路径集合
        remove_list = set()  # 需要移出的路径
        for su in sub:
            if i + 1 <= len(su):
                dirs_v2 = dirs_v2 | set(list_dirs(join(parent, *su[:i])))
                remove_list.add(join(parent, *su[:i + 1]))
        for remove_path in remove_list:
            try:
                dirs_v2.remove(remove_path)
            except KeyError as e:
                raise KeyError("check your path: %s" % e)
        yield dirs_v2


def dpath_to_lists(dpath):
    """将目录字符串转换成list对象"""
    return list(map(lambda s: s.strip().strip("/").split("/"), dpath.split(",")))


def caseid_factory(case):
    s = case.split("::")
    output = os.popen('find ' + Framework.CASE_DIR + ' -name *.py | xargs grep ' + s[-1])
    output = output.read().split(":")[0]
    caseid = output + '::' + case
    print(caseid)
    return caseid


def handle_args(args, other_args):
    if args.log:
        Colour.flag = True
    if args.dev_name:
        env.platform = Platform.IOS if args.dev_name.startswith('iphone') else Platform.ANDROID
        env.device = args.dev_name
    else:
        if len(get_adb_devices()) == 1:
            for x, y in env.UDID.items():
                if y == get_adb_devices()[0]:
                    Logging.info('auto choose device:' + x, True)
                    env.device = x
                    env.platform = Platform.ANDROID
                    env.app_ver = Version(env.app_version)
        elif len(get_ios_devices()) == 1:
            for x, y in env.UDID.items():
                if y == get_ios_devices()[0]:
                    Logging.info('auto choose device:' + x, True)
                    env.device = x
                    env.platform = Platform.IOS
                    env.app_ver = Version(env.app_version)
                    kill_iproxy()
        else:
            Logging.info('not specify device', True)
    env.app_env = args.env
    env.citm_service = args.citm
    sys.argv = [sys.argv[0]]
    sys.argv.extend(other_args)
    if args.suites:
        data = dpath_to_lists(args.suites)
        for ds in ignores(Framework.CASE_DIR, *dpath_to_lists(args.suites)):
            for d in ds:
                opt = "--ignore={}".format(d)
                sys.argv.append(opt)
    if args.tag:
        sys.argv.append('-m ' + (' and ' + env.platform + ' or ').join(args.tag.split(' or ')) +
                        ' and ' + env.platform)
    else:
        sys.argv.append('-m ' + env.platform)
    if args.case:
        case = caseid_factory(args.case)
        sys.argv.append(case)
    print(sys.argv)
    clean()
    handler = ManifestXmlHandler(env.appPackage, env.capabilities['platformVersion'])
    env._activity_list = handler.parse("AndroidManifest.xml", "activity")


env = _Env()
