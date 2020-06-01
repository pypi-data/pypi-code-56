# -*- coding: utf-8 -*-
import argparse
import asyncio
import inspect
import json
import os
import random
import re
import shutil
import string
import sys
import threading
import time
import traceback
from functools import *
from os.path import *
from subprocess import *
from unittest.case import TestCase

import aiohttp
import allure
import pymysql
import pytest
import requests
from _pytest.fixtures import FixtureRequest
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from attr import *
# from citm.client import *
from hulk.conn import *
from hulk.utils.util import *
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as ec
from termcolor import colored, cprint
from urllib3.exceptions import *
from selenium.webdriver.common.by import By


class Colour:
    flag = False
    truncate = False

    @staticmethod
    def c(msg, print_to_console, colour, attrs=None):
        if not Colour.truncate:
            with open('log.log', 'w', encoding='utf8') as f:
                Colour.truncate = True

        def p(x):
            with open('log.log', 'a+', encoding='utf8') as f:
                f.write(colored(x + '\n', '%s' % colour, attrs=attrs))
            if print_to_console:
                return cprint(x, '%s' % colour, attrs=attrs)

        return p(msg)

    @staticmethod
    def show_verbose(msg, print_to_console):
        Colour.c(msg, print_to_console, 'green')

    @staticmethod
    def show_debug(msg, print_to_console):
        Colour.c(msg, print_to_console, 'white', ['dark'])

    @staticmethod
    def show_info(msg, print_to_console):
        Colour.c(msg, print_to_console, 'cyan')

    @staticmethod
    def show_warn(msg, print_to_console):
        Colour.c(msg, print_to_console, 'blue')

    @staticmethod
    def show_error(msg, print_to_console):
        Colour.c(msg, print_to_console, 'magenta')


class Logging:

    @staticmethod
    def error(msg, print_to_console=False):
        Colour.show_error(Logging.get_now_time() + " [Error]:" + "".join(str(msg)), Colour.flag or
                          print_to_console)

    @staticmethod
    def warn(msg, print_to_console=False):
        Colour.show_warn(Logging.get_now_time() + " [Warn]:" + "".join(str(msg)), Colour.flag or
                         print_to_console)

    @staticmethod
    def info(msg, print_to_console=False):
        Colour.show_info(Logging.get_now_time() + " [Info]:" + "".join(str(msg)), Colour.flag or
                         print_to_console)

    @staticmethod
    def debug(msg, print_to_console=False):
        Colour.show_debug(Logging.get_now_time() + " [Debug]:" + "".join(str(msg)), Colour.flag or
                          print_to_console)

    @staticmethod
    def verbose(msg, print_to_console=False):
        Colour.show_verbose(Logging.get_now_time() + " [verbose]:" + "".join(str(msg)),
                            Colour.flag or print_to_console)

    @staticmethod
    def get_now_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
