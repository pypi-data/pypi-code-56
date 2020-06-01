from .device import *

from selenium.webdriver.common.by import By

class AtxDriver:

    def __init__(self):
        device_id = connect_device("android", None)
        self.device = get_device(device_id)

    def start_session(self, capabilities):
        """
            Returns:
                deviceId (string)
            """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException('Capabilities must be a dictionary')
        self.device.session(capabilities['appPackage'])

    def activate_ime_engine(self, engine):

    def implicitly_wait(self, time_to_wait):

    def find_element(self, by=By.ID, value=None):

        if by == By.ID:
            by = By.CSS_SELECTOR
            value = '[id="%s"]' % value
        elif by == By.TAG_NAME:
            by = By.CSS_SELECTOR
        elif by == By.CLASS_NAME:
            by = By.CSS_SELECTOR
            value = ".%s" % value
        elif by == By.NAME:
            by = By.CSS_SELECTOR
            value = '[name="%s"]' % value

    def find_elements(self):

    def page_source(self):

    def click(self):

    def get_screenshot_as_png(self):

    def get_window_size(self):

class AtxEle:


atxdriver = AtxDriver()