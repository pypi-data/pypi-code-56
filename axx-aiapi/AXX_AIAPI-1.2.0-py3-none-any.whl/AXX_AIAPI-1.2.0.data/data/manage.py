import os
import logging
import sys
from flask import Flask
from controller import init_blue_print
from config import config, G
from config.log_config import config_log
from utils import parse_args
import flask_cors


def create_app(env):
    logger = None
    app = Flask(__name__)
    flask_cors.CORS(app)
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object(config.get(env))
    init_blue_print(app)
    config_log()
    if env == 'prd':
        logger = logging.getLogger('gunicorn')
    else:
        logger = logging.getLogger('console')
    G.logger = logger
    app.logger = logger
    return app


def init_python_path(_file_):
    package_dir = os.path.join(os.path.dirname(_file_), '../')
    abs_path = os.path.abspath(package_dir)
    if abs_path not in sys.path:
        sys.path.insert(0, abs_path)


init_python_path(__file__)

__all__ = ['main']


def main():
    args = parse_args()

    if args.env:
        app = create_app(args.env)
    else:
        app = create_app("default")

    port = args.port if args.port else 8080
    app.run('0.0.0.0', port)
    app.logger.info(f'run server at port {port}')


if __name__ == '__main__':
    main()
