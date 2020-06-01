''' Execute the acorn package as a module. ''' 
from .client import cli

import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    name = 'python -m acorn'
    sys.argv = ['-m', 'acorn'] + args
    cli.main(args=args, prog_name=name)