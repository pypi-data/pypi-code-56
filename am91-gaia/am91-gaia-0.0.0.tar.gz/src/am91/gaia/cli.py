import importlib
import logging
from argparse import ArgumentParser

from .manifest import BaseManifest
from .generator import Generator
from .defs import APP_NAME

def main():
    # Parse arguments
    args = parse_args()

    # Setup logger
    logging.basicConfig(level=getattr(logging, args.log_level))

    # Execute command
    args.func(args)

def parse_args():
    parser = ArgumentParser(prog=APP_NAME)
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
        default='WARNING', 
        help='logging level to show'
    )

    # Init parser
    subparsers = parser.add_subparsers()
    parser_init = subparsers.add_parser('init', help='initialize gaia project')
    parser_init.add_argument('type', help='project type (should be a valid project generator)')
    parser_init.add_argument('name', nargs='?', help='project name')
    parser_init.set_defaults(func=init)

    args = parser.parse_args()
    if 'func' not in vars(args):
        parser.print_help()
        exit()
    return args

def init(args):
    PREFIX = 'am91.gaia_template_'

    try:
        module_name = f'{PREFIX}{args.type}'
        module = importlib.import_module(module_name)
        manifest = module.Manifest()

        generator = Generator(manifest)
        generator.init(args.name)
        generator.generate(module_name)

    except ModuleNotFoundError:
        logging.error('Template not found')
