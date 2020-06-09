# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

from bottle import Bottle,run

app = Bottle()

class Router:

    def __init__(self):

        self.bottle = app

        self.run = run(app, host="localhost", port=8888)

    @app.route('/')
    def index(self):
        return 'Hello RoboMentor!'

    @app.route('/hello')
    def hello(self):
        return 'Hello RoboMentor!'