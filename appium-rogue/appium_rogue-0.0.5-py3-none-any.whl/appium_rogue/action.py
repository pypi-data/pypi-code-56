# -*- coding: utf-8 -*-
from .locator import *
from .util import *

from selenium.webdriver.support.ui import WebDriverWait


class _Action:

    def __init__(self, driver: WebDriver = None):
        self.driver = driver
        self.is_android = True if env.platform is Platform.ANDROID else False
        self.id = None
        self.cursor = None
        self.dirty = False
        self.handling_pop_window = False
        self.tv_guide_button = False
        self.width = None
        self.height = None
        self.touch_action = None
        self.end = False
        self.pytest_keyboard_interrupt = False
        self.restart_flag = False
        self.current_account = None
        self.current_keryboard = None

    def init(self):
        # init_mysql_connection(self)
        # citm_client.import_from_json()
        proxy.close_proxy()
        stop_u2()
        threading.Thread(target=self.check_appium_active, name='checkAppiumActiveThread').start()
        appiumServer.start_appium()
        if env.platform is Platform.ANDROID:
            threading.Thread(target=logcat.run, name='logcatThread').start()
        Logging.info('server init finished')
        self.init_driver()

    @rerun
    def check_appium_active(self):
        count = 0
        while not appiumServer.quit and count < WAIT_TIME:
            time.sleep(1)
            count += 1
            Logging.debug('[appium log size]:' + str(os.path.getsize("appium.log")))
            if count == WAIT_TIME:
                if appiumServer.appium_log_size == os.path.getsize("appium.log"):
                    raise_error(WaitTimeTooLongError,
                                "appium without action more than {}s".format(WAIT_TIME))
                    self.init()
                else:
                    count = 0
                    appiumServer.appium_log_size = os.path.getsize("appium.log")

    def init_driver(self):
        self.reset(connect_appium())
        env.a and self.driver.activate_ime_engine(IME.APPIUM)
        Logging.info('driver init finished')

    def reset(self, driver):
        """单例模式,所以当driver变动的时候,需要重置一下driver"""
        self.driver = driver
        self.set_implicitly_wait()
        self.width = driver.get_window_size()['width']
        self.height = driver.get_window_size()['height']
        self.touch_action = TouchAction(driver)

    def set_end(self):
        self.end = True

    def quit_test(self):
        if self.cursor:
            self.cursor.close()
        if self.driver:
            try:
                env.a and self.driver.deactivate_ime_engine()
                self.driver.quit()
            except HTTPError as e:
                ...
        if appiumServer.is_start():
            appiumServer.stop()
        appiumServer.quit = True
        if logcat.adb:
            logcat.stop()
        Logging.info('test finished')

    @rerun
    @show_action
    def accept_alert(self):
        if env.i:
            Logging.info('start accept alert')
            self.driver.switch_to.alert.accept()
            Logging.info('end accept alert')

    @show_action
    @screen_shoot
    def find_element(self, locator):
        """查找元素，如果有多个只返回第一个"""
        Logging.debug('[Finding]:' + str(locator))
        self.handle_all_pop_window()
        r = act.find_element(self.driver, locator)
        if r is STALE:
            Logging.info(STALE)
            self.handle_all_pop_window()
            return act.find_element(self.driver, locator)
        return r

    @show_action
    def find_elements(self, locator):
        """查找多个元素"""
        Logging.debug('[Finding]:' + str(locator))
        self.handle_all_pop_window()
        return act.find_element(self.driver, locator, False)

    def handle_all_pop_window(self):
        """处理弹窗，只支持安卓"""
        if env.platform is Platform.ANDROID:
            wait_loading()
            if not self.handling_pop_window and len(
                    window()) > 1 and window[-1] not in env.popWindow.exclude_windows:
                self.handling_pop_window = True
                Logging.info('start handle pop window:' + str(window))
                if env.platform is Platform.IOS:
                    return
                i = 0
                while i < 4 and len(window) > 1:
                    windows = env.popWindow.windows_dict.get(window[-1], None)
                    if not windows:
                        Logging.info(str(window[-1]) + ' not in locator list')
                        window()
                    else:
                        self.handle_all_pop_window_()
                    i = i + 1
                self.handling_pop_window = False
                Logging.info('end handle pop window')
            else:
                Logging.info('not find pop window')
            if not self.handling_pop_window:
                self.handle_guide_button()

    def handle_all_pop_window_(self):
        for x in env.popWindow.windows_dict[window()[-1]]:
            Logging.debug('[handle window]:' + str(x))
            try:
                if x in env.popWindow.text_list:
                    y = env.popWindow.text_dialog_dict.get(x.text, None)
                    if y:
                        y.click
                else:
                    x.click
            except Exception:
                Logging.info('[handle window]:not find window element ')
            if len(window()) == 1:
                break
        else:
            if len(window) == len(window()) and window.windows == window():
                self.handling_pop_window = False
                raise_error(
                    RuntimeError,
                    "failed to handle pop window, CurrentActivity：{}, SurfaceFlinger：{}".format(
                        window()[-1], window))

    def handle_guide_button(self):
        if env.app_ver < '4.2.8':
            if not self.tv_guide_button and window(
            )[-1] == env.Activities.COM_WOSAI_CASHBAR_CORE_MAIN_MAINACTIVITY:
                Logging.info('start handle guide button')
                self.tv_guide_button = True
                if env.popWindow.tv_guide_button.displayed:
                    Logging.info('found guide button')
                    if not env.popWindow.tv_guide_button.click:
                        self.tv_guide_button = False
                        Logging.info('fail to handle guide button')
                        return
                else:
                    self.tv_guide_button = False
                    Logging.info('not found guide button')
                Logging.info('end handle guide button')

    def find_with_raise(self, locator):
        ele = self.find_element(locator)
        if ele is None:
            raise_error(
                NotFoundElementError, "未能找到元素：{}，当前surfaceFlinger：{}".format(
                    locator,
                    window() if env.platform is Platform.ANDROID else ''))
        return ele

    def soft_click(self, locator):
        """点击元素(若该元素不存在，则不点击)"""
        ele = self.find_element(locator)
        if ele is not None:
            return act.click(ele)

    @rerun
    def click(self, locator):
        """点击元素(若该元素不存在，则上抛异常)"""
        if locator.name == 'btn_virtual_back':
            if window()[-1] == window()[0]:
                return self.send_key_event('KEYCODE_BACK')
        else:
            return act.click(self.find_with_raise(locator))


    @rerun
    def clear(self, locator):
        """清空文本内容"""
        act.clear(self.find_with_raise(locator))

    @rerun
    def input(self, locator, value, clear=False):
        """输入文本内容"""
        if locator.name == 'username' or locator.name == 'password':
            self.dirty = True
        ele = self.find_with_raise(locator)
        if clear:
            act.clear(ele)
        act.input(ele, str(value))

    @rerun
    def is_element_displayed(self, locator):
        """判断元素是否可见/存在"""
        ele = self.find_element(locator)
        if not ele:
            return False
        return act.is_element_displayed(ele)

    @rerun
    def is_element_selected(self, locator):
        """判断元素是否选中，比如选中tab栏位被选中"""
        return act.is_element_selected(self.find_with_raise(locator))

    @rerun
    def is_element_enabled(self, locator):
        """判断元素是否可用"""
        return act.is_element_enabled(self.find_with_raise(locator))

    @rerun
    def is_element_checked(self, locator):
        """判断元素是否勾选，比如checkbox"""
        return act.is_element_checked(self.find_with_raise(locator))

    @rerun
    def get_element_attribute(self, locator, attribute_name=None):
        """获取元素属性值"""
        if not attribute_name:
            attribute_name = ElementAttribute.TEXT if env.a else ElementAttribute.NAME
        r = self.find_with_raise(locator).get_attribute(attribute_name)
        Logging.info('[' + attribute_name + ']:' + str(r))
        return r

    @rerun
    def switch_to_context(self, index=0, retry=1):
        """切换到指定index的context"""
        current_context = self.driver.current_context
        contexts = self.driver.contexts
        if current_context == contexts[index]:
            return True
        while retry > 0:
            Logging.info('start switch to context:' + str(contexts[index]))
            self.driver.switch_to.context(contexts[index])
            current_context = self.driver.current_context
            retry -= 1
            if current_context == contexts[index]:
                Logging.info('end switch to context:' + str(contexts[index]))
                return True
        return False

    @show_action
    @rerun
    def find_toast_util_timeout(self, toast_msg, timeout=5, poll=0.05):
        """是否弹出指定内容的toast(仅对安卓且版本号大于>5.0以及automator2有效)"""
        if self.is_android and version_compare(env.capabilities['platformVersion'],
                                               '5.0') and env.capabilities['automationName'].lower(
        ) == AutomationName.UI_AUTOMATOR2:
            try:
                message = '//*[@text=\'{}\']'.format(toast_msg)
                WebDriverWait(self.driver, timeout, poll).until(
                    ec.presence_of_element_located((By.XPATH, message)))
                Logging.info("[found toast]:" + toast_msg)
                return True
            except Exception as e:
                Logging.error("在{}秒内未能找到指定内容的toast:{}".format(timeout, toast_msg))
                return False
        else:
            return True

    @rerun
    def scroll_to_find_element(self, locator, times=3, swipe_range="normal"):
        """通过滚动找到元素"""
        direct = locator.direction.lower()
        if direct not in get_direction_list():
            times = 0
        while times >= 0:
            ele = self.find_element(locator)
            if ele is not None:
                return ele
            if direct == ScrollDirection.UP:
                self.swipe_down_to_up(1, swipe_range)
            elif direct == ScrollDirection.DOWN:
                self.swipe_up_to_down()
            elif direct == ScrollDirection.LEFT:
                self.swipe_right_to_left()
            elif direct == ScrollDirection.RIGHT:
                self.swipe_left_to_right()
            times -= 1
        raise_error(
            NotFoundElementError, "未能找到元素：{}，当前surfaceFlinger：{}".format(
                locator,
                window() if env.platform is Platform.ANDROID else ''))

    @rerun
    def take_screenshot_on_error(self, method_name, save_to=None):
        """截图"""
        env.a and Logging.info('[windows]:' + str(window))
        if len(window()) >= 1:
            fp = method_name + '-' + window[
                -1] + '.png' if env.platform is Platform.ANDROID else method_name + '.png'
        else:
            fp = method_name + '.png' if env.platform is Platform.ANDROID else method_name + '.png'
        if save_to is not None and os.path.isdir(save_to):
            fp = os.path.join(save_to, fp)
        Logging.verbose('[save screenshot]:' + fp)
        try:
            self.driver.save_screenshot(fp)
        except Exception:
            Logging.warn('failed to save screenshot')

    @rerun
    def tap(self, x, y, duration=None):
        """点击指定坐标"""
        Logging.info('[tap]:' + str(x) + ' ' + str(y))
        self.driver.tap([(x, y)], duration)

    @rerun
    def tap_percentPos(self, x, y, duration=None):
        """点击指定百分比坐标"""
        Logging.info('[tap_per]:' + str(x) + ' ' + str(y))
        origin_h = get_screen_reacts(env.udid, Platform.ANDROID)['height']
        origin_w = get_screen_reacts(env.udid, Platform.ANDROID)['width']
        real_x = origin_w * x
        real_y = origin_h * y
        self.driver.tap([(real_x, real_y)], duration)

    @rerun
    def set_implicitly_wait(self, implicitly_wait=Appium.IMPLICITLY_WAIT):
        """设置隐式等待时间（隐式等待和显示等待都存在时，超时时间取二者中较大的）"""
        self.driver.implicitly_wait(implicitly_wait)

    @rerun
    def send_key_event(self, arg, num=0):
        """模拟实体按键 https://developer.android.com/reference/android/view/KeyEvent.html"""
        event_list = {'KEYCODE_HOME': 3, 'KEYCODE_BACK': 4, 'KEYCODE_MEN': 82, 'KEYCODE_NUM': 7, "KEYCODE_ENTER": 66}
        if arg == 'KEYCODE_NUM':
            self.driver.press_keycode(int(event_list[arg]) + int(num))
        elif arg in event_list:
            self.driver.press_keycode(int(event_list[arg]))

    @rerun
    def swipe_left_to_right(self, count=1):
        """从左往右边滑动"""
        for x in range(count):
            time.sleep(1)
            self.driver.swipe(self.width * 1 / 10, self.height / 2, self.width * 9 / 10,
                              self.height / 2, 1000)

    @rerun
    def swipe_right_to_left(self, count=1):
        """从右往左边滑动"""
        for x in range(count):
            time.sleep(1)
            self.driver.swipe(self.width * 9 / 10, self.height / 2, self.width / 10,
                              self.height / 2, 1000)

    @rerun
    def swipe_up_to_down(self, count=1):
        """从上向下滑动"""
        for x in range(count):
            time.sleep(1)
            self.driver.swipe(self.width / 2, self.height * 0.2, self.width / 2, self.height - 1,
                              1000)

    @rerun
    def swipe_down_to_up(self, count=1, swipe_range="normal"):
        """从下向上滑动"""
        for x in range(count):
            time.sleep(1)
            if swipe_range == "tiny":
                self.driver.swipe(self.width / 2, self.height * 0.5, self.width / 2, 1, 1000)
            else:
                self.driver.swipe(self.width / 2, self.height * 0.8, self.width / 2, 1, 1000)

    @rerun
    def swipe_down_to_up_distance(self, h_distance=1, count=1):
        """从下向上滑动到指定的距离"""
        for x in range(count):
            time.sleep(1)
            self.driver.swipe(self.width / 2, self.height * 0.8, self.width / 2, h_distance, 1000)

    @rerun
    def swipe_by_coordinate(self, start_x, start_y, end_x, end_y, duration=1500):
        """按指定方向滑动"""
        self.touch_action.press(start_x, start_y).wait(duration).move_to(end_x,
                                                                         end_y).release().perform()

    @rerun
    def long_press(self, locator, duration):
        """长按元素"""
        ele = self.find_element(locator)
        self.touch_action.long_press(ele, duration * 1000).perform()

    @rerun
    def _find_text_in_page(self, key_word):
        """检查页面是否存在指定的关键字"""
        return key_word in self.driver.page_source

    def get_text(self, locator):
        """获取元素text值"""
        return self.get_element_attribute(locator)

    def back_press(self):
        """模拟物理返回键"""
        self.send_key_event('KEYCODE_BACK')

    def press(self, action=''):
        if action == 'back':
            self.send_key_event('KEYCODE_BACK')
        elif action == 'home':
            self.send_key_event('KEYCODE_HOME')
        elif action == "enter":
            self.send_key_event('KEYCODE_ENTER')

    def set_number_by_soft_keyboard(self, nums):
        """模仿键盘输入数字,nums支持list"""
        list_nums = list(nums)
        for num in list_nums:
            self.send_key_event('KEYCODE_NUM', num)

    def is_text_present(self, text, is_retry=True, retry_time=5):
        """检查页面是否存在指定的text"""
        try:
            if is_retry:
                return WebDriverWait(self.driver,
                                     retry_time).until(lambda driver: self._find_text_in_page(text))
            return self._find_text_in_page(text)
        except Exception:
            Logging.error("在当前页面中未发现指定关键字：{}".format(text))
            return False

    def check_element(self, locator):
        """勾选元素-已经做判断"""
        if not locator.checked:
            locator.click

    def uncheck_element(self, locator):
        """反勾选元素-已经做判读"""
        if locator.checked:
            locator.click

    def select_element(self, locator):
        """选中元素-已经做判断"""
        if not locator.selected:
            locator.click

    def unselect_element(self, locator):
        """反选中元素-已经做判读"""
        if locator.selected:
            locator.click

    @rerun
    def record(self, result):
        # if not get_adb_devices():
        #     sys.exit()
        if result.failed:
            Logging.error(' '.join([result.when, result.nodeid, result.outcome]))
            Logging.error(result.longreprtext)
            self.take_screenshot_on_error(result.nodeid[result.nodeid.rfind('/') + 1:])
            allure.attach(action.driver.get_screenshot_as_png(), result.nodeid,
                          allure.attachment_type.PNG)
        else:
            Logging.verbose(' '.join([result.when, result.nodeid, result.outcome]))


class Click:

    def __get__(self, instance, Type):
        return action.click(instance)


class Clear:

    def __get__(self, instance, Type):
        return action.clear(instance)


class Input:

    def __get__(self, instance, Type):
        return partial(action.input, instance)


class Displayed:

    def __get__(self, instance, Type):
        return action.is_element_displayed(instance)


class Selected:

    def __get__(self, instance, Type):
        return action.is_element_selected(instance)


class Enabled:

    def __get__(self, instance, Type):
        return action.is_element_enabled(instance)


class Checked:

    def __get__(self, instance, Type):
        return action.is_element_checked(instance)


class Text:

    def __get__(self, instance, Type):
        return action.get_text(instance)


action = _Action()
Locator.click = Click()
Locator.clear = Clear()
Locator.input = Input()
Locator.displayed = Displayed()
Locator.selected = Selected()
Locator.enabled = Enabled()
Locator.checked = Checked()
Locator.text = Text()
