# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

from bottle import route,run

class Router:

    def __init__(self):
        print("0")
        self.run = run(host="localhost", port=8888)
        print(self.run)

    @route('/')
    def index(self):
        print("1")
        return 'Hello RoboMentor!'

    @route('/hello')
    def hello(self):
        print("2")
        return 'Hello RoboMentor!'