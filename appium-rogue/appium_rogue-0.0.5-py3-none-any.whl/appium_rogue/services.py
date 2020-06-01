# -*- coding: utf-8 -*-
from .environment import *


class _AppiumServer:

    def __init__(self, host=Appium.HOST, port=Appium.PORT):
        self.appium_log_size = 0
        self.host = host
        self.port = port
        self.__running = threading.Event()
        self.__running.set()
        self.appium_process = None
        self.start = False
        self.quit = False
        with open('appium.log', 'w', encoding='utf8') as f:
            ...

    def run(self):
        if self.check_started():
            os.popen(
                "kill -9 `ps aux|grep -v grep|grep /usr/local/bin/appium|awk '{print $2}'`").read()
        cmd = "appium --session-override -a %s -p %s --chromedriver-executable  /usr/bin/chromedriver" % (
            self.host, self.port)
        self.appium_process = Popen(
            cmd, shell=True, stdout=PIPE, stderr=PIPE, bufsize=1, close_fds=True)
        self.start = False
        Logging.info("start appium")
        while self.appium_process.poll() is None and self.__running.isSet():
            try:
                line = self.appium_process.stdout.readline().decode('utf-8', 'replace')
            except KeyboardInterrupt:
                break
            if not self.start and self.check_started():
                self.start = True
                Logging.info("start appium success")
            with open('appium.log', 'a+', encoding='utf8') as f:
                f.write(Logging.get_now_time() + ' ' + line)

    def check_started(self):
        sysstr = platform.system()
        if(sysstr == "Windows"):
            with PowerShell('GBK') as ps:
                pid_appium = ps.run(WindowsShellCMD.FIND_APPIUM)
            with PowerShell('GBK') as ps:
                pid_appium_desktop = ps.run(WindowsShellCMD.FIND_APPIUM_DESKTOP)
        else:
            cmd = "ps aux|grep -v grep|grep /usr/local/bin/appium"
            cmd_desktop = "ps aux|grep -v grep|grep Appium"
            pid_appium = os.popen(cmd).read().strip()
            pid_appium_desktop = os.popen(cmd_desktop).read().strip()
        if pid_appium or pid_appium_desktop:
            return True

    def stop(self):
        self.__running.clear()
        time.sleep(1)
        self.appium_process.terminate()

    def reset(self):
        self.__running.set()
        self.start = False

    def is_start(self):
        return self.start

    def start_appium(self):
        threading.Thread(target=self.run, name='appiumThread').start()
        while not self.is_start():
            Logging.info('wait for appium start')
            time.sleep(1)


# class _CITMClient(CITMClient):

#     def __init__(self, http_proxy=None, https_proxy=None):
#         if http_proxy is None:
#             http_proxy = env.citm_service
#         super().__init__(http_proxy, https_proxy)

#     def enable_cheater(self, alias, namespace=env.app_env):
#         super().enable_cheater(alias, namespace)

#     def disable_cheater(self, alias, namespace=env.app_env):
#         super().disable_cheater(alias, namespace)

#     def create_cheater(self,
#                        netloc,
#                        path,
#                        method,
#                        rules,
#                        alias,
#                        namespace=env.app_env,
#                        scheme=None,
#                        mode="fixed",
#                        scope="request",
#                        enabled=True):
#         super().create_cheater(netloc, path, method, rules, namespace, alias, scheme, mode, scope,
#                                enabled)

#     def remove_cheater(self, alias, namespace=env.app_env):
#         super().remove_cheater(alias, namespace)

#     def list_cheater(self):
#         super().list_cheater()

#     def activate_rule(self, alias, rule_id, namespace=env.app_env):
#         super().activate_rule(alias, rule_id, namespace)

#     def add_rule(self, alias, body, namespace=env.app_env):
#         super().add_rule(alias, namespace, body)

#     def del_rule(self, alias, rule_id, namespace=env.app_env):
#         super().del_rule(alias, rule_id, namespace)

#     def enable_cheater_rule(self, alias, rule_id, namespace=env.app_env):
#         self.enable_cheater(alias, namespace)
#         self.activate_rule(alias, rule_id, namespace)

#     def disable_cheater_rule(self, alias, namespace=env.app_env):
#         self.disable_cheater(alias, namespace)

#     @asyncio_run
#     async def import_from_json(self):
#         async with aiohttp.ClientSession() as session:
#             async with session.get(env.etcdtool + '/citm') as resp:
#                 res = await resp.read()
#                 async with session.post(
#                         self.base_url + '/import',
#                         headers={'Content-Type': 'application/json'},
#                         proxy=self.req_kwargs['proxies']['http'],
#                         data=res) as resp:
#                     await resp.read()


def enabled_cheater(cheater_id: list, recover=True):
    """装饰器：启动cheater"""

    def wrapper(func):

        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            if recover:
                for temp_id in cheater_id:
                    self.addCleanup(citm_client.disable_cheater, temp_id['alias'])
            for temp_id in cheater_id:
                citm_client.enable_cheater(temp_id['alias'])
            f = func(self, *args, **kwargs)
            return f

        return _wrapper

    return wrapper


def disabled_cheater(cheater_id: list):
    """装饰器：关闭cheater"""

    def wrapper(func):

        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            for temp_id in cheater_id:
                citm_client.disable_cheater(temp_id['alias'])
            f = func(self, *args, **kwargs)
            return f

        return _wrapper

    return wrapper


def activate_cheater_rule(alias, rule_id):
    """装饰器：激活某一个cheater下的rule"""

    def wrapper(func):

        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            # 场景恢复
            self.addCleanup(citm_client.disable_cheater, alias)
            # enable cheater
            citm_client.enable_cheater(alias)
            # activate specified rule
            citm_client.activate_rule(alias, rule_id)
            f = func(self, *args, **kwargs)
            return f

        return _wrapper

    return wrapper


def enabled_cheater_rules(cheater_rules: list, recover=True):
    """装饰器：激活cheater rules"""

    def wrapper(func):

        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            if recover:
                for cheater_rule in cheater_rules:
                    if isinstance(cheater_rule, dict):
                        self.addCleanup(citm_client.disable_cheater_rule, cheater_rule['alias'])
                        Logging.info("restore(disable) cheater rule:" + cheater_rule)
                    else:
                        raise TypeError("Error type of cheater_rules")
            for cheater_rule in cheater_rules:
                Logging.info("enable cheater rule:" + cheater_rule)
                citm_client.enable_cheater_rule(cheater_rule['alias'], cheater_rule['rule_id'])
            f = func(self, *args, **kwargs)
            return f

        return _wrapper

    return wrapper


def disabled_cheater_rules(cheater_rules: list):
    """装饰器：关闭cheater rules"""

    def wrapper(func):

        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            for cheater_rule in cheater_rules:
                if isinstance(cheater_rule, dict):
                    citm_client.disable_cheater_rule(cheater_rule['alias'])
                else:
                    raise TypeError("Error type of cheater_rules")
            f = func(self, *args, **kwargs)
            return f

        return _wrapper

    return wrapper


appiumServer = _AppiumServer()
# citm_client = _CITMClient()
