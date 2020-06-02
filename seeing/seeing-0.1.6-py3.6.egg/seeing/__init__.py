"""
monitor file modify then execute it.
support go, python, c++, c.
filename endswith .py .c .cpp .go
"""

__author__ = 'Mikele'
__version__ = '0.1.6'

import argparse
import os, time, logging, sys
from os.path import getmtime, join, isfile, splitext
from pprint import pprint
from subprocess import Popen


logging.basicConfig(level=logging.INFO)

help_text = 'monitor execute file every seconds.'

commands = ['go', 'python', 'py', 'py3', 'python3', 'g++', 'gcc']
tails = ['py', 'html', 'css', 'js']
watch_tails = set(['.'+ tail for tail in tails])
modify_files = {}
last_files = {}
ignore_dirnames = set(['.git', 'migrations', 'locale', '__pycache__'])
boot_time = time.time()

def watch_dev(root):
    '''
    :params root: dir root
    dev frontend and backend when use template etc. jinja2 django
    '''
    for name in os.listdir(root):
        new_name = join(root, name)
        _, tail = splitext(name)
        if isfile(new_name):
            if tail in watch_tails:
                modify_files[new_name] = getmtime(new_name)
                last_files[new_name] = getmtime(new_name)
        else:
            if name not in ignore_dirnames and not name.startswith('.'):
                watch_dev(new_name)


def run_command(filename):
    '''run switch file tail'''
    if filename.endswith('.cpp'):
        cmd = "g++ {} && ./a.out"
    elif filename.endswith('.c'):
        cmd = "gcc {} && ./a.out"
    elif filename.endswith('.py'):
        cmd = "python3 {}"
    elif filename.endswith('.go'):
        # os.environ.setdefault('GOPATH', os.getcwd())
        cmd = "go run {}"
    elif args.cmd:
        cmd = ' '.join(sys.argv[2:])
        print(sys.argv)
    if isfile(filename):
        logging.info(cmd.format(filename))
        os.system(cmd.format(filename))
    else:
        logging.info(cmd)
        os.system(cmd)


def reload(fork, command):
    '''
    when file remove or modify reload
    '''
    fork.terminate()
    fork.wait(10)
    fork = Popen(command)


def monitor_file_modify_every(seconds, filename, command, dirname):
    '''
    monitor file change
    '''
    fork = None
    if filename:
        st = os.stat(filename).st_mtime
        run_command(filename)
    while True:
        if filename:
            f = os.stat(filename)
            if st != f.st_mtime:
                st = f.st_mtime
                if filename:
                    run_command(filename)
        else:
            # if monitor dir
            global last_files
            global modify_files
            last_files = {}
            watch_dev(dirname)
            # 刚启动时目录下所有文件修改时间
            if boot_time > time.time() - 1:
                # boot 1 seconds ago
                new_modify_files = modify_files.copy()
                print(command)
                fork = Popen(command)
                # pprint(new_modify_files)
            else:
                # l_len, m_len = len(last_files.keys()), len(modify_files.keys())
                if modify_files != new_modify_files:
                    new_modify_files = modify_files.copy()
                    reload(fork, command)
                elif last_files != modify_files:
                    modify_files = last_files.copy()
                    reload(fork, command)
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            os._exit(0)

def main():
    parser = argparse.ArgumentParser(description=help_text + " support go cpp c py")
    parser.add_argument('-f', '--filename', required=False,
       help='if filename,watch file, else watch dir to dev web app')
    parser.add_argument(
        '-s', '--seconds', metavar='seconds', action='store',
        type=float, default=1.0, help=help_text)
    parser.add_argument('-d', '--dirname', default='.', help='watch dirname')
    parser.add_argument(
        '-c', '--cmd', metavar='cmd', action='store', nargs='*',
        help="command to execute script, eg: seeing -c bash hello.sh")
    args = parser.parse_args()
    print("Press Ctrl+c to exit")
    monitor_file_modify_every(args.seconds, args.filename, args.cmd,
            args.dirname)

if __name__ == '__main__':
    main()
