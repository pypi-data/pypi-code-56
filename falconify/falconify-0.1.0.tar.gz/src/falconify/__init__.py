#!/usr/bin/env python
import os
import sys
import json
import textwrap
import subprocess

try:
    import fcntl
    import termios
    import struct

    ioctl = fcntl.ioctl(0, termios.TIOCGWINSZ,
                        struct.pack('HHHH', 0, 0, 0, 0))
    _h, TERMWIDTH, _hp, _wp = struct.unpack('HHHH', ioctl)
    if TERMWIDTH <= 0:  # can occur if running in emacs pseudo-tty
        TERMWIDTH = None
except (ImportError, IOError):
    TERMWIDTH = None

# available
available_commands = ['bootstrap', 'create-module']

# adjust the path for root.
relative_path = os.getcwd() + '/'

# absolute script path
script_path = os.path.dirname(os.path.abspath(__file__)) + '/'

# template path
template_path = script_path + 'Templates/'

# set the path for the configuration
# mapper
config_path = script_path + 'config.json'

def main():
    # Command Configuration
    command = sys.argv[1]
    try:
        module_name = sys.argv[2]
    except:
        module_name = None

    # check if command is allowed
    if command not in available_commands:
        print('Command not supported!')
        exit()

    # check if the module name has been passed
    if command == 'create-module' and module_name is None:
        print('Please provide the module name')
        exit()

    CreateStruct().execute(command, module_name)


class CreateStruct:

    def __init__(self):
        pass

    @staticmethod
    def execute(command, module_name=None):
        if command == 'bootstrap':
            print("Installing Falconify")
            CreateStruct().git("init")
            CreateStruct().git("remote", "add", "source", "https://gitlab.com/raphacosta/falconify")
            CreateStruct().git("pull", "source", "master")
            print("Installed")
        if command == 'create-module':
            with open(config_path, 'r') as f:
                steps = json.load(f)
                for step in steps:
                    print(step['comments'])
                    module = module_name.capitalize()

                    # checking for _ words
                    if '_' in module:
                        module = module.split('_')
                        module = \
                            module[0].capitalize() + module[1].capitalize()

                    step_template = step['template'] + ".py.mako"
                    step_path = CreateStruct()\
                        ._resolve_path(module, step['path'])
                    step_filename = CreateStruct()\
                        ._resolve_name(
                        module, step['template'], step['filename'])
                    print("in..." + step_path)

                    if not os.path.exists(step_path):
                        os.makedirs(step_path, exist_ok=True)

                    fin = open(template_path + step_template, "rt")
                    fout = open(step_path + step_filename, "wt")

                    for line in fin:
                        fout.write(line.replace('${module}', module)
                                   .replace('${moduleRoute}', module.lower()))

                    fin.close()
                    fout.close()

                    print('Done with ' + step['template'])

    @staticmethod
    def status(_statmsg, fn, *arg, **kw):
        CreateStruct().msg(_statmsg + " ...", False)

        try:
            ret = fn(*arg, **kw)
            CreateStruct().write_outstream(sys.stdout, " done\n")
            return ret
        except IOError:
            CreateStruct().write_outstream(sys.stdout, " FAILED\n")
            raise

    @staticmethod
    def write_outstream(stream, *text):
        encoding = getattr(stream, 'encoding', 'ascii') or 'ascii'
        for t in text:
            if not isinstance(t, str):
                t = t.encode(encoding, 'replace')
            t = t.decode(encoding)
            try:
                stream.write(t)
            except IOError:
                # suppress "broken pipe" errors.
                # no known way to handle this on Python 3 however
                # as the exception is "ignored" (noisily) in TextIOWrapper.
                break

    @staticmethod
    def msg(msg, newline=True):
        if TERMWIDTH is None:
            CreateStruct().write_outstream(sys.stdout, msg)
            if newline:
                CreateStruct().write_outstream(sys.stdout, "\n")
        else:
            lines = textwrap.wrap(msg, TERMWIDTH)
            if len(lines) > 1:
                for line in lines[0:-1]:
                    CreateStruct().write_outstream(
                        sys.stdout, "  ", line, "\n")
            CreateStruct().write_outstream(
                sys.stdout, "  ", lines[-1], ("\n" if newline else ""))

    @staticmethod
    def _resolve_name(module, template, mapped_name):
        resolved = mapped_name.replace('${module}', module)
        resolved = resolved.replace('+', '')
        resolved = resolved.replace(' ', '')
        resolved = resolved.replace('template', template)
        return resolved + ".py"

    @staticmethod
    def _resolve_path(module, mapped_path):
        resolved = mapped_path.replace('${module}', module)
        resolved = resolved.replace('+', '')
        return relative_path + resolved

    @staticmethod
    def git(*args):
        return subprocess.check_call(['git'] + list(args))
