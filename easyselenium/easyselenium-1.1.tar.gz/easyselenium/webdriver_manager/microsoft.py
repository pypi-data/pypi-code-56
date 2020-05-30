import logging

from easyselenium.webdriver_manager import utils
from easyselenium.webdriver_manager.driver import IEDriver
from easyselenium.webdriver_manager.manager import DriverManager
from easyselenium.webdriver_manager.driver import EdgeChromiumDriver


class IEDriverManager(DriverManager):
    def __init__(self, version="latest",
                 os_type=utils.os_type(),
                 path=None,
                 name="IEDriverServer",
                 url="http://selenium-release.storage.googleapis.com",
                 latest_release_url=None,
                 log_level=None):
        super().__init__(path, log_level)
        self.driver = IEDriver(version=version,
                               os_type=os_type,
                               name=name,
                               url=url,
                               latest_release_url=latest_release_url)

    def install(self):
        return self.download_driver(self.driver)


class EdgeChromiumDriverManager(DriverManager):
    def __init__(self, version="latest",
                 os_type=utils.os_type(),
                 path=None,
                 name="edgedriver",
                 url="https://msedgedriver.azureedge.net",
                 latest_release_url="https://msedgedriver.azureedge.net/"
                                    "LATEST_STABLE",
                 log_level=None):
        super().__init__(path, log_level)
        self.driver = EdgeChromiumDriver(version=version,
                                         os_type=os_type,
                                         name=name,
                                         url=url,
                                         latest_release_url=latest_release_url)

    def install(self):
        return self.download_driver(self.driver)
