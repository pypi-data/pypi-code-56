# -*- coding: utf-8 -*-
from .environment import *


def check_version(down: str = '4.2.7', high: str = '5.0.0'):
    """检查app版本，如果不符合，则跳过"""

    def checker(obj):
        if env.app_ver:
            if down and env.app_ver < down:
                obj.__unittest_skip__ = True
                obj.__unittest_skip_why__ = "client version {} is under {}".format(
                    env.app_ver, down)
            if high and env.app_ver > high:
                obj.__unittest_skip__ = True
                obj.__unittest_skip_why__ = "client version {} is above {}".format(
                    env.app_ver, high)
        return obj

    return checker


def tag(*tags):
    """给类或方法添加多个标签"""

    def wrapper(obj):
        for tag in tags:
            if tag == CITM and not getattr(obj, '__unittest_skip__', False):
                pytest.mark.usefixtures('open_proxy')(obj)
            if tag == SMOKE and not getattr(obj, '__unittest_skip__', False):
                pytest.mark.usefixtures('close_proxy')(obj)
            pytest.mark.__getattr__(tag)(obj)
            """自动对用例添加分级标识标签"""
            if tag == CASELEVEL.P0:
                allure.severity(BLOCKER)(obj)
            elif tag == CASELEVEL.P1:
                allure.severity(CRITICAL)(obj)
            else:
                allure.severity(NORMAL)(obj)
        return obj

    return wrapper


def caseid(caseid):
    """给类或方法添加caseid"""

    def wrapper(obj):
        pytest.mark.caseid(caseid)(obj)
        allure.label("caseid", caseid)(obj)
        return obj

    return wrapper


def initversion(version):
    """给类或方法添加多个标签"""

    def wrapper(obj):
        pytest.mark.initversion(version)(obj)
        allure.label("initversion", version)(obj)
        return obj

    return wrapper


def unimplemented(info=None):
    """标识出未完整实现用例逻辑的方法"""

    def wrapper(obj):
        case = info or obj.__doc__ or obj.__name__
        obj.__unittest_skip__ = True
        obj.__unittest_skip_why__ = "unimplemented: {}".format(case)
        return obj

    return wrapper


def obsolete(obj):
    """标识已经废弃的接口，用例跳过执行"""
    obj.__unittest_skip__ = True
    obj.__unittest_skip_why__ = "obsolete"
    return obj


def phabricator_issue(issue_id: int):
    """标识phabricator上面的bug id，只需要传入数字部分"""

    def wrapper(obj):
        obj.__unittest_skip__ = True
        obj.__unittest_skip_why__ = "phabricator issue: http://phabricator.wosai-inc.com/T{}".format(
            issue_id)
        return obj

    return wrapper
