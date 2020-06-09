# -*- coding: utf-8 -*-
"""
RoboMentor_Client: Python library and framework for RoboMentor_Client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by RoboMentor.
:license: MIT, see LICENSE for more details.
"""

from bottle import Bottle, template

app = Bottle()

@app.route('/')
def index():
    return 'Hello RoboMentor!'

@app.route('/hello')
def hello():
    return 'Hello RoboMentor!'

if __name__ == '__main__':
    app.run(host="localhost", port=8888)