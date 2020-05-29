# -*- coding: utf-8 -*-
"""Microapp project module"""

from __future__ import print_function

import sys, os, shlex, json, multiprocessing

from microapp.base import MicroappObject, microapp_builtins
from microapp.error import (UsageError, InternalError, TypeCheckError,
                            NormalExit, ConfigError)
from microapp.utils import tostr, tostr_iter, appdict
from microapp.parse import ProjectArgParser, DataRegistry, data_transfer
from microapp.app import App
from microapp.group import Group, GroupCmd
from microapp.manage import Manager
from microapp.framework import load_appclass


class Project(MicroappObject, ProjectArgParser, Manager, DataRegistry):
    """Microapp Project Base-class"""

    def __new__(cls, *vargs, **kwargs):

        prog = kwargs.pop("prog", cls._name_)
        desc = kwargs.pop("description", cls._description_)
        epilog = kwargs.pop("epilog", None)

        obj = super(Project, cls).__new__(cls, *vargs, prog=prog,
                description=desc, epilog=epilog, **kwargs)

        if sys.version_info < (3, 0):
            obj.add_argument("--multiproc-method",
                    help="multiprocessing spawning method")

        obj.add_argument("--forward", metavar="expr", action="append",
                delay=True, help="forward variables to next app")

        obj.add_argument("--share", metavar="expr", action="append",
                delay=True, help="share variables between sibling apps")

        obj.add_argument("--downcast", metavar="expr", action="append",
                delay=True, help="downcast variables under this app")

        obj.add_argument('--version', action='version', version=(prog + " "
                + cls._version_))

        obj._config = obj._load_config()
        obj.set_config("name", obj._name_, createall=True)
        obj.set_config("version", obj._version_)

        prjdcast = appdict({"name": obj._name_, "version": obj._version_})
        obj._dcasts["_project_"] = prjdcast

        return obj

    def _load_config(self):


        home = os.path.expanduser("~")
        cfgdir = os.path.join(home, ".microapp")
        self._cfgfile = os.path.join(cfgdir, "config")

        if not os.path.exists(cfgdir):
            os.makedirs(cfgdir)

        if os.path.isfile(self._cfgfile):
            with open(self._cfgfile) as f:
                config = json.load(f)

        else:
            import datetime
            now = datetime.datetime.now()

            created = appdict({"by": self._name_, "when": str(now)})
            config = appdict({"created" : created})

            with open(self._cfgfile, "w") as f:
                json.dump(config, f, sort_keys=True, indent=4)

        return config


    def set_config(self, keylist, value, createall=False, curcfg=None):

        if isinstance(keylist, str):
            keylist = keylist.split(".")

        key = keylist[0]

        if curcfg is None:
            curcfg = self._config

            if key not in ("app", "global", "project"):
                key = "project"
                keylist.insert(0, key)
                keylist.insert(1, self._name_)

        if len(keylist)==1:
            curcfg[key] = value

        elif key in curcfg:
            self.set_config(keylist[1:], value, curcfg=curcfg[key],
                    createall=createall)

        elif createall:
            newconfig = appdict()
            curcfg[key] = newconfig
            self.set_config(keylist[1:], value, curcfg=newconfig,
                    createall=createall)
        else:
            raise UsageError("Key '%s' does not exist." % key)

    def has_config(self, keylist, curcfg=None):

        if isinstance(keylist, str):
            keylist = keylist.split(".")

        key = keylist[0]

        if curcfg is None:
            curcfg = self._config

            if key not in ("app", "global", "project"):
                key = "project"
                keylist.insert(0, key)
                keylist.insert(1, self._name_)

        if key not in curcfg:
            return False

        elif len(keylist)==1:
            return True

        else:
            return self.get_config(keylist[1:], curcfg=curcfg[key])

    def get_config(self, keylist, curcfg=None):

        if isinstance(keylist, str):
            keylist = keylist.split(".")

        key = keylist[0]

        if curcfg is None:
            curcfg = self._config

            if key not in ("app", "global", "project"):
                key = "project"
                keylist.insert(0, key)
                keylist.insert(1, self._name_)

        if key not in curcfg:
            raise ConfigError("Key '%s' is not found." % key)

        elif len(keylist)==1:
            return curcfg[key]

        else:
            return self.get_config(keylist[1:], curcfg=curcfg[key])

    def perform(self, aargs):
        pass

    def run_command(self, args=None, cwd=None, project_args=[], group_args=[],
                app_args=[], forward=appdict(), shared=appdict(), downcast=appdict()):
        """MicroappProject command execution entry"""

        multiprocessing.freeze_support()

        try:

            if args is None:
                args = sys.argv[1:]

            elif isinstance(args, (str, bytes, bytearray)):
                if sys.platform == "win32":
                    args = shlex.split(tostr(args).replace("\\", "/"))
                else:
                    args = shlex.split(tostr(args))

            else:
                args = [a for a in tostr_iter(args)]

            project_args = [a for a in tostr_iter(project_args)]
            group_args = [a for a in tostr_iter(group_args)]
            app_args = [a for a in tostr_iter(app_args)]
            
        except Exception as err:
            print("ERROR: wrong argument syntax: '%s'\n" % str(args),
                    file=sys.stderr)
            sys.exit(1)

        try:
            ret = -1, None

            pwd = os.getcwd()
            if cwd and os.path.isdir(cwd):
                os.chdir(cwd)

            pargs, aargs = args, []

            for cidx, citem in enumerate(args):
                if citem == "--":
                    pargs, aargs = args[:cidx], args[cidx+1:]
                    break

            pargs += project_args

            pargs, rargs = self.parse_known_args(pargs, self._env)

            if sys.version_info < (3, 0) and hasattr(multiprocessing,
                    "set_start_method"):

                if pargs.multiproc_method:
                    multiprocessing.set_start_method(pargs.multiproc_method["_"])

                elif sys.platform == "darwin":
                    multiprocessing.set_start_method("spawn")

            self.perform(pargs)

            if pargs.forward:
                data_transfer(pargs.forward, self._fwds)
            self._fwds.update(forward)

            if pargs.share:
                data_transfer(pargs.share, self._shrds)
            self._shrds.update(shared)

            if pargs.downcast:
                data_transfer(pargs.downcast, self._dcasts)
            self._dcasts.update(downcast)

            if rargs or aargs:

                app = GroupCmd(self)

                sys.argv[0] = self._name_

                ret = app.run(rargs+group_args, aargs, self._fwds)

            else:
                print(self.format_help())

                ret = 0, None

        except UsageError as err:
            print("USAGE ERROR: " + str(err))

        except ConfigError as err:
            print("CONFIG ERROR: " + str(err))

        except InternalError as err:
            print("INTERNAL ERROR: " + str(err))

        except TypeCheckError as err:
            print("TYPE MISMATCH: " + str(err))

        except NormalExit:
            ret = 0

        except (KeyboardInterrupt, EOFError):
            print('[Interrupted.]')

        finally:
            os.chdir(pwd)

            with open(self._cfgfile, "w") as f:
                json.dump(self._config, f)

        return ret

    def run_class(self, cls, cwd=None, project_args=[], group_args=[],
                app_args=[], forward=appdict(), shared=appdict(), downcast=appdict()):
        """MicroappProject app execution entry"""

        multiprocessing.freeze_support()

        project_args = [a for a in tostr_iter(project_args)]
        group_args = [a for a in tostr_iter(group_args)]
        app_args = [a for a in tostr_iter(app_args)]

        try:
            ret = -1, None

            pwd = os.getcwd()
            if cwd and os.path.isdir(cwd):
                os.chdir(cwd)

            pargs, _ = self.parse_known_args(project_args, self._env)

            if sys.version_info < (3, 0) and hasattr(multiprocessing,
                    "set_start_method"):
                if pargs.multiproc_method:
                    multiprocessing.set_start_method(pargs.multiproc_method["_"])

                elif sys.platform == "darwin":
                    multiprocessing.set_start_method("spawn")

            self.perform(pargs)

            if pargs.forward:
                data_transfer(pargs.forward, self._fwds)
            self._fwds.update(forward)

            if pargs.share:
                data_transfer(pargs.share, self._shrds)
            self._shrds.update(shared)

            if pargs.downcast:
                data_transfer(pargs.downcast, self._dcasts)
            self._dcasts.update(downcast)

            if cls:
                if issubclass(cls, Group):
                    grp = cls(self)
                    sys.argv[0] = self._name_
                    ret = grp.run(group_args, app_args, self._fwds)

                elif issubclass(cls, App):
                    app = cls(self)
                    sys.argv[0] = self._name_
                    ret = app.run(app_args, [], self._fwds)
            else:
                print(self.format_help())

                ret = 0, None

        except UsageError as err:
            print("USAGE ERROR: " + str(err))

        except ConfigError as err:
            print("CONFIG ERROR: " + str(err))

        except InternalError as err:
            print("INTERNAL ERROR: " + str(err))

        except TypeCheckError as err:
            print("TYPE MISMATCH: " + str(err))

        except NormalExit:
            ret = 0

        except (KeyboardInterrupt, EOFError):
            print('[Interrupted.]')

        finally:
            os.chdir(pwd)

            with open(self._cfgfile, "w") as f:
                json.dump(self._config, f)

        return ret

    def get_builtin_apps(self):

        dapps = []

        for scls in self.__class__.mro():
            if hasattr(scls, "_builtin_apps_"):
                dapps.extend(getattr(scls, "_builtin_apps_"))

        return dapps


class MicroappProject(Project):
    """Microapp default project"""

    _name_ = "microapp"
    _version_ = "0.3.1"
    _description_ = "A command-line portal to Microapp apps."
    _long_description_ = "A command-line portal to Microapp apps."
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/microapp"

