# -*- coding: utf-8 -*-
from .logcat import logcat
from .services import *

from selenium.webdriver.support.ui import WebDriverWait


def auto_restart_app(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            Logging.warn('Catch ' + str(e) + ' in init app, restart app')
            Logging.warn(str(traceback.format_exc()))
            self.restart_app()
            return func(self, *args, **kwargs)

    return wrapper


def last_function_name(i=2):
    while sys._getframe(i).f_code.co_name in skippedFuncNameList:
        i += 1
    return sys._getframe(i).f_code.co_name


def show_action(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        Logging.info('[Action]:' + last_function_name())
        return func(*args, **kwargs)

    return wrap


def screen_shoot(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        '''测试步骤截图'''
        locator = args[1]

        ele = func(*args, **kwargs)
        if ele and not isinstance(ele, str):
            Logging.info('[element]:' + ele.get_attribute(ElementAttribute.TEXT))
            Logging.info('[location]:' + str(locator))
            location = ele.location_in_view
            x = location['x']
            y = location['y']
            # screen_shoot_find(args[0], ele.get_attribute(ElementAttribute.TEXT))
            Logging.info('[location]:' + str(x) + ":" + str(y))
            with allure.step(locator.location):
                current_window = window()
                no_screen_shoot = ['tv.danmaku.bili.ui.login.LoginActivity', 'tv.danmaku.bili.ui.login.LoginOriginalActivity']
                if len(window()) >= 1 and current_window[-1] not in no_screen_shoot:
                    allure.attach(args[0].driver.get_screenshot_as_png(), "img",
                                  allure.attachment_type.PNG)
                origin_h = args[0].driver.get_window_size()['height']
                origin_w = args[0].driver.get_window_size()['width']
                percent_h = y / origin_h
                percent_w = x / origin_w
                allure.attach("[" + str(percent_w) + "," + str(percent_h) + "]", 'elementLocation')
                """规避某些判定某些无归属页面的locator引发的属性异常问题"""
                cover_racts = locator.cover_racts
                allure.attach(str(cover_racts), 'coverRacts')
        return ele

    return wrapper


def handle_method_name(name):
    a = name.split('.')
    b = a[-1].split(' ')
    c = b[-1].split('=')
    return a[-2] + '.py::' + b[0] + '::' + c[-1][:-2]


def rerun(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (NotFoundElementError, StaleElementReferenceException,
                InvalidSelectorException) as e:
            Logging.warn('Catch ' + e.__class__.__name__ + ', retry once find:' + str(args[0]))
            time.sleep(2)
            self.take_screenshot_on_error(
                handle_method_name(self.id) + '[NotFoundElementError]:' + str(args[0].name))
            time.sleep(1)
            return func(self, *args, **kwargs)
        except (WebDriverException, WaitTimeTooLongError) as e:
            Logging.warn('Catch ' + e.__class__.__name__ + ', restart webdriver session')
            self.driver.start_session(env.capabilities)
            self.restart_flag = True
            """严重注意！！！！这个弹窗标志位容易出现问题"""
            self.handling_pop_window = False
            if func.__name__ is not 'record':
                pytest.fail(e.__class__.__name__)
        except Exception as e:
            Logging.warn('Catch ' + e.__class__.__name__)
            if func.__name__ is not 'record':
                pytest.fail(e.__class__.__name__)

    return wrapper


def connect_appium():
    req_url = "http://%s:%s/wd/hub" % (Appium.HOST, Appium.PORT)
    kill_chromedriver()
    Logging.info('connecting webdriver')
    driver = WebDriver(req_url, env.capabilities)
    Logging.info('webdriver connected')
    return driver


def init_mysql_connection(obj):
    """全局的mysql连接，用例层可以不使用MySQLConnectionMgr来进行连接"""
    Logging.info('start connect mysql')
    mgr = MySQLConnectionMgr(
        autocommit=True, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, **env.mysql)
    mgr.backend = mgr.BACKEND_PYMYSQL
    success = False
    while not success:
        try:
            obj.cursor = mgr.connection.cursor()
            success = True
            Logging.info('mysql connected')
        except pymysql.err.MySQLError as e:
            Logging.error(str(e))
            Logging.error(traceback.format_exc())
            Logging.warn('catch mysql connect error, retry connect')


def get_sqb_sms_code(cellphone):
    """获取短信验证码"""
    param = {"cellphone": cellphone}
    resp = requests.get(url=env.sms_code, params=param)
    return resp.content.decode("utf-8").strip()


def get_sms_code_from_redis(cellphone, db=1, **kwargs):
    """从redis中读取短信验证码"""
    if kwargs:
        env.redis.update(kwargs)
    else:
        kwargs = env.redis.copy()
    redis_conn = RedisConnectionMgr(**kwargs, db=db).client
    keys = redis_conn.keys("*" + cellphone + "*")
    if keys:
        key = keys[0]
        return redis_conn.get(key)
    return None


@asyncio_run
async def change_password(account, password):
    account = str(account)
    password = str(password)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    async with aiohttp.ClientSession() as session:
        async with session.post(
                env.api_domain + '/V2/Account/findPasswordAuthCode',
                data='cellphone=' + account + '&token=',
                headers=headers) as resp:
            data = json.loads((await resp.read()).decode().strip())['data']
        async with session.post(
                env.api_domain + '/V2/Account/findPassword',
                data='cellphone=' + account + '&authCode=' + data + '&newPassword=' + password +
                     '&token=',
                headers=headers) as resp:
            await resp.read()


def raise_error(error_type, msg):
    Logging.error(str(error_type))
    Logging.error(msg)
    if isinstance(error_type, (AssertionError, WebDriverException)):
        raise error_type
    raise error_type(msg)


@asyncio_run
async def stop_u2_req(port):
    url = 'http://127.0.0.1:'
    charles = get_charles_port()
    proxy = url + charles if charles else None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url + port + '/ping', proxy=proxy, timeout=1) as resp:
                res = (await resp.read()).decode().strip()
                if res == 'pong':
                    async with session.delete(url + port + '/uiautomator', proxy=proxy) as resp:
                        res = (await resp.read()).decode().strip()
                        # assert res in ['Success', 'already stopped']
    except asyncio.TimeoutError as e:
        ...
    except aiohttp.client_exceptions.ServerDisconnectedError as e:
        ...


def stop_u2():
    port = get_u2_port()
    if port:
        ports = port.split('\n')
        for port in ports:
            if port.startswith('82'):
                continue
            stop_u2_req(port)


def wait_loading():
    if env.a:
        loading_start_time = time.time()
        while logcat.isLoading() is True:
            Logging.info('Loading')
            time.sleep(1)
            if time.time() - loading_start_time > WAIT_TIME:
                raise_error(WaitTimeTooLongError, "wait loading more than {}s".format(WAIT_TIME))


def get_direction_list():
    """方向集合"""
    return [ScrollDirection.UP, ScrollDirection.DOWN, ScrollDirection.LEFT, ScrollDirection.RIGHT]


class _Window:

    def __init__(self, w=None):
        self._windows = w or []

    def __getitem__(self, n):
        if n == -1:
            Logging.debug('[current activity]:' + self._windows[n])
        else:
            Logging.debug('[window ' + str(n) + ']:' + self._windows[n])
        return self._windows[n]

    def __call__(self):
        wait_loading()
        return _Window(self.windows)

    def __len__(self):
        Logging.debug('[window len]:' + str(len(self._windows)))
        return len(self._windows)

    def __str__(self):
        return str(self._windows)

    @property
    def windows(self):
        """过滤非待测app的layer"""
        layer_windows = get_surfaceflinger(env.udid, env.capabilities['platformVersion'], env.appPackage)
        Logging.debug('[layer_windows]:' + str(layer_windows))
        self._windows = []
        for layer in layer_windows:
            if layer in env.activity_list:
                self._windows.append(layer)
        if "PopupWindow" in layer_windows[-1]:
            self._windows.append(layer_windows[-1])
        Logging.debug('[get windows]:' + str(self._windows))
        return self._windows


class _Proxy:

    def __init__(self):
        self.proxyOn = True

    def open_proxy(self):
        if env.platform is Platform.ANDROID and not self.proxyOn:
            Logging.info('proxy on')
            proxy_on(env.udid)
            self.proxyOn = True

    def close_proxy(self):
        if env.platform is Platform.ANDROID and self.proxyOn:
            Logging.info('proxy off')
            proxy_off(env.udid)
            self.proxyOn = False


def catch(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.__init__()
        try:
            func(self, *args, **kwargs)
            self.finished = True
        except Exception as e:
            self.err = e
            self.errInfo = traceback.format_exc()
            Logging.info('catch exception')

    return wrapper


class _Act:

    def __init__(self):
        self.finished = None
        self.result = None
        self.err = None
        self.errInfo = None

    @catch
    def ele_find(self, driver, locator, is_single):
        Logging.debug('find element by locator:' + str(locator))
        location = locator.location
        by_type = locator.by_type
        idx = locator.idx
        # source = driver.page_source
        # Logging.debug('page_source:' + str(source))
        if by_type in [ElementAttribute.TEXT, ElementAttribute.NAME]:
            if env.a:
                by_type = By.XPATH
                location = '//*[@text=\"%s\"]' % location
            if env.i:
                by_type = ElementAttribute.NAME
        if is_single:
            if idx == 0:
                # self.result = driver.find_element(by_type, location)
                self.result = WebDriverWait(driver, timeout=5, poll_frequency=0.5).until(lambda d: d.find_element(
                    by_type, location))
            else:
                # self.result = driver.find_elements(by_type, location)[idx]
                self.result = WebDriverWait(driver, timeout=5, poll_frequency=0.5).until(lambda d: d.find_elements(
                    by_type, location)[idx])
        else:
            self.result = driver.find_elements(by_type, location)

    @catch
    def ele_click(self, ele):
        ele.click()

    @catch
    def ele_input(self, ele, value):
        Logging.info('[input]:' + value)
        env.a and ele.send_keys(value)
        env.i and ele.set_value(value)

    @catch
    def ele_clear(self, ele):
        self.result = ele.clear()

    @catch
    def ele_is_displayed(self, ele):
        self.result = ele.is_displayed()

    @catch
    def ele_is_selected(self, ele):
        self.result = ele.is_selected()

    @catch
    def ele_is_enabled(self, ele):
        self.result = ele.is_enabled()

    @catch
    def ele_is_checked(self, ele):
        self.result = True if ele.get_attribute("checked").lower() == 'true' else False

    def raise_webdriver_exception(self):
        if self.err and isinstance(self.err, WebDriverException):
            raise_error(self.err, self.errInfo)

    def raise_wait_time_too_long_error(self):
        raise_error(WaitTimeTooLongError,
                    last_function_name() + " wait more than {}s without response".format(WAIT_TIME))

    def return_success(self):
        if self.finished:
            Logging.info(last_function_name() + ' success')
            return True

    def return_result(self, action, level=LogLevel.INFO):
        if self.finished:
            if level == LogLevel.INFO:
                Logging.info('[' + action + ']:' + str(self.result))
            if level == LogLevel.DEBUG:
                Logging.debug('[' + action + ']:' + str(self.result.get_attribute(ElementAttribute.TEXT)))
            return self.result
        else:
            Logging.debug('wait [' + action + '] finish')

    def check_finished(self, f, *arg):
        for x in range(WAIT_TIME):
            if env.platform is Platform.ANDROID:
                Logging.debug('determining stale')
                if len(window) < len(window()):
                    return STALE
            r = f(*arg) if arg else f()
            if self.finished:
                return r
            if self.err and isinstance(self.err, InvalidSelectorException):
                self.raise_webdriver_exception()
            if self.err and isinstance(self.err, (NoSuchElementException, TimeoutException)):
                Logging.debug('[catch]:' + str(self.err))
                return None
            self.raise_webdriver_exception()
            time.sleep(1)
        self.raise_wait_time_too_long_error()

    def find_element(self, driver, locator, is_single=True):
        threading.Thread(
            target=self.ele_find, name='findThread', args=(driver, locator, is_single)).start()
        return self.check_finished(self.return_result, 'find', LogLevel.DEBUG)

    def click(self, ele):
        threading.Thread(target=self.ele_click, name='clickThread', args=(ele,)).start()
        return self.check_finished(self.return_success)

    def clear(self, ele):
        threading.Thread(target=self.ele_clear, name='clearThread', args=(ele,)).start()
        return self.check_finished(self.return_success)

    def input(self, ele, value):
        threading.Thread(target=self.ele_input, name='inputThread', args=(ele, value)).start()
        return self.check_finished(self.return_success)

    def is_element_displayed(self, ele):
        threading.Thread(
            target=self.ele_is_displayed, name='isDisplayedThread', args=(ele,)).start()
        return self.check_finished(self.return_result, 'prensent')

    def is_element_selected(self, ele):
        threading.Thread(target=self.ele_is_selected, name='isSelectedThread', args=(ele,)).start()
        return self.check_finished(self.return_result, 'selected')

    def is_element_enabled(self, ele):
        threading.Thread(target=self.ele_is_enabled, name='isEnabledThread', args=(ele,)).start()
        return self.check_finished(self.return_result, 'enabled')

    def is_element_checked(self, ele):
        threading.Thread(target=self.ele_is_checked, name='isCheckedThread', args=(ele,)).start()
        return self.check_finished(self.return_result, 'checked')


def _adb_minicap():
    """
    capture screen with minicap
    https://github.com/openstf/minicap
    """

    screencap_adb = "adb shell \"LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1080x1920@1080x1920/0 -s > /sdcard/screencap/" + str(
        time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))) + ".jpg\""

    resp = os.popen(screencap_adb)


def pull_to_pc(dest_folder_path):
    pull_adb = "adb pull /sdcard/screencap/ " + str(dest_folder_path)
    resp = os.popen(pull_adb)
    time.sleep(7)  # 等待pull 完成
    print("adb pull resp: ", resp)


act = _Act()
proxy = _Proxy()
window = _Window()
