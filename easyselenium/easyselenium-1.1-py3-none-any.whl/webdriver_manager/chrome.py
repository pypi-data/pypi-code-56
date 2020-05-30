import os

from easyselenium.webdriver_manager import utils
from easyselenium.webdriver_manager.driver import ChromeDriver
from easyselenium.webdriver_manager.manager import DriverManager
from easyselenium.webdriver_manager.utils import ChromeType


class ChromeDriverManager(DriverManager):
    def __init__(self, version="latest",
                 os_type=utils.os_type(),
                 path=None,
                 name="chromedriver",
                 url="http://chromedriver.storage.googleapis.com",
                 latest_release_url="http://chromedriver.storage.googleapis.com/LATEST_RELEASE",
                 chrome_type=ChromeType.GOOGLE,
                 log_level=None):
        super(ChromeDriverManager, self).__init__(path, log_level)

        self.driver = ChromeDriver(name=name,
                                   version=version,
                                   os_type=os_type,
                                   url=url,
                                   latest_release_url=latest_release_url,
                                   chrome_type=chrome_type)

    def install(self):
        driver_path = self.download_driver(self.driver)

        os.chmod(driver_path, 0o755)
        return driver_path
