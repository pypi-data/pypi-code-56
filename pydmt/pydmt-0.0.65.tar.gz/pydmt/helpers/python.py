from typing import Callable


def make_console_script(package_name: str, main: Callable):
    """
    return a string suitable to be used as the section 'console_scripts'
    of the 'entry_points' parameters of setup.py.
    
    example: 'pycmdtools=pycmdtools.endpoints.main:main'
    :param package_name:
    :param main:
    :return:
    """
    return "{}={}:{}".format(
        package_name,
        getattr(main, '__module__'),
        main.__name__,
    )
