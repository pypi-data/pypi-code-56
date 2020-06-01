import sys
import os
import datetime
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

from Common.Config import cfg as config
from Admin.Core import core

import logging
logger = logging.getLogger(__name__)

app = Flask(__name__, root_path=os.path.abspath('Admin'))
CORS(app)

app.secret_key = 'qwzvzxcvklj;k1237098jxcvpoidufsdf4+_)*&^5654zx[ipo345898vbjdf9'
app.permanent_session_lifetime = datetime.timedelta(days=365)

_view_tests = False
_use_cdn = False
_use_min_js = True


def init(version=None):
    func_name = f'{sys._getframe().f_code.co_name}()'
    try:
        flask_cfg = config.cfg.get('flask')
        if not isinstance(flask_cfg, dict):
            logger.error(f"Error in {func_name}: not isinstance(config.cfg.get('flask'), dict)...")
            return False
        global _view_tests, _use_cdn, _use_min_js
        _view_tests = flask_cfg.get('view_tests', False)
        _use_cdn = flask_cfg.get('use_cdn', False)
        _use_min_js = flask_cfg.get('use_min_js', True)

        if not core.init(version):
            logger.error(f"Error in {func_name}: not core.init()...")
            return False

        return True
    except Exception as e:
        print(f'Error in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.print_exc()}')
        return False


def print_request(func_name='', via_print=False):
    _print = print if via_print else logger.info
    _print(f'{func_name}; type(request): {type(request)}')
    _print(f'{func_name}; request.url: {request.url}')
    _print(f'{func_name}; request.endpoint: {request.endpoint}')
    _print(f'{func_name}; request.path: {request.path}')
    _print(f'{func_name}; request.form: {dict(request.form)}')
    _print(f'{func_name}; request.method: {request.method}')
    _print(f'{func_name}; request.args: {request.args.to_dict()}')
    _print(f'{func_name}; request.get_data(): {request.get_data()}')


@app.before_request
def before_request():
    if core.init_error is not None:
        return get_error_response(core.init_error)


@app.after_request
def after_request(response):
    return response


@app.context_processor
def utility_processor():

    def view_tests():
        return _view_tests

    def footer():
        return core.get_footer()

    def use_cdn():
        return _use_cdn

    def use_min_js():
        return _use_min_js

    return dict(footer=footer, view_tests=view_tests, use_cdn=use_cdn, use_min_js=use_min_js)


def json_response(data=None, error=None, status=200):
    if isinstance(data, list):
        result = []
    else:
        result = {}
    if data:
        result = data
    elif error:
        result['error'] = error
    resp = jsonify(result)
    resp.status_code = status
    return resp


def get_error_response(error, status=400):
    logger.debug(error)
    return json_response(error=error, status=status)


def get_list_response(func_name, result):
    if isinstance(result, str):
        return get_error_response(result)
    elif not isinstance(result, list):
        return get_error_response(f'Error in {func_name}: not isinstance(result, list)...')
    return jsonify(result)


import Admin.Routes
