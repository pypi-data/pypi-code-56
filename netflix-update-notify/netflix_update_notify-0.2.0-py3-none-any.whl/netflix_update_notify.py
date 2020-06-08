import atexit
import logging
import re
from threading import Thread

import requests
import semver

# Implementation libs
from pkg_info import get_pkg_info


try:
    from importlib import metadata
    from importlib import PackageNotFoundError
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata
    from importlib_metadata import PackageNotFoundError

__version__ = "0.2.0"


class UpdateNotifier(object):
    """Loosely based on update-notipy public module"""

    pattern = r"\d+\.\d+\.\d+"

    def __init__(self, name: str):
        """Set the package and SemVer string for what to check."""
        self.name: str = name
        try:
            self.version: str = metadata.version(name)
        except PackageNotFoundError:
            pass

    def notify(self) -> None:
        """Set up a notification for the user on process exit if updates exist."""
        logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)
        pkg = get_pkg_info(self.name)
        latest = pkg.version
        found_parts = re.findall(UpdateNotifier.pattern, latest)
        if len(found_parts) > 0:
            latest = found_parts[0]
        if semver.VersionInfo.parse(self.version).compare(latest) >= 0:
            return
        else:
            action, arg = (
                print,
                f"{self.name} update available {self.version} → {latest}. Run\npip install -U {self.name}",
            )
        atexit.register(action, arg) if arg else atexit.register(action)

    @staticmethod
    def _notify_version_thread(package: str):
        try:
            if package is None or package == "":
                return
            UpdateNotifier(package).notify()
        except (requests.exceptions.HTTPError, ValueError) as ee:
            # early prereleases do this due to SemVer version number requirements
            logging.debug(
                f"Checking for updates for {package} failed, but this is not fatal\n{ee}"
            )

    @staticmethod
    def notify_of_updates(package: str):
        update_checker = Thread(
            target=UpdateNotifier._notify_version_thread, kwargs={"package": package},
        )
        update_checker.start()
        atexit.register(update_checker.join)
