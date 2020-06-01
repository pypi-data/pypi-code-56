from .action import action
from .atxdriver import AtxDriver

class DriverAgent:
    @staticmethod
    def start_session():
        if isinstance(action.driver, WebDriver):
            action.driver.start_session(env.capabilities)
        if isinstance(action.driver, AtxDriver):
            AtxDriver.start_session(env.capabilities)

    @staticmethod
    def start():
        if isinstance(action.driver, WebDriver):
            appiumServer.start_appium()

    @staticmethod
    def isStart():
        if isinstance(action.driver, WebDriver):
            return appiumServer.is_start()

    @staticmethod
    def run():

    @staticmethod
    def check_started():

    @staticmethod
    def stop():

    @staticmethod
    def reset():

    @staticmethod
    def activate_ime_engine():
        if isinstance(action.driver, WebDriver):
            action.driver.activate_ime_engine(IME.APPIUM)

    @staticmethod
    def connect():
        if isinstance(action.driver, WebDriver):
            driver = connect_appium()
        else:
            driver = AtxDriver()
        return driver

    @staticmethod
    def implicitly_wait(implicitly_wait):
        if isinstance(action.driver, WebDriver):
            action.driver.implicitly_wait(implicitly_wait)

    @staticmethod
    def get_window_size():
        if isinstance(action.driver, WebDriver):
           return action.driver.get_window_size()
    @staticmethod
    def get_touchAction():
        if isinstance(action.driver, WebDriver):
            return TouchAction(action.driver)

    @staticmethod
    def quit():
        if isinstance(action.driver, WebDriver):
            action.driver.quit()

