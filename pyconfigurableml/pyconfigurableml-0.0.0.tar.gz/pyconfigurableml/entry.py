'''
Utilities around programatic entry point.
'''


import argparse
import inspect
import logging
import os
from typing import Callable
from typeguard import typechecked
import yaml


@typechecked
def run(main: Callable[[object, logging.Logger], None]) -> None:
    '''
    Handle log levels and parsing a YAML configuration file.
    '''
    # Follow https://stackoverflow.com/a/37792573 to get the caller's file name.
    caller_file = inspect.stack()[1][1]
    caller_dir = os.path.dirname(os.path.abspath(caller_file))

    parser = argparse.ArgumentParser()

    parser.add_argument('--config', default=os.path.join(caller_dir, 'config.yml'))
    parser.add_argument('--level', default='INFO')
    args = parser.parse_args()

    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)

    logging.basicConfig(level=args.level)
    logger = logging.getLogger()

    main(config, logger)
