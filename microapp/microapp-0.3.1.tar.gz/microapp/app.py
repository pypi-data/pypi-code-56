# -*- coding: utf-8 -*-
"""Microapp application module"""

from __future__ import print_function

import sys, abc

from microapp.base import MicroappObject, microapp_builtins
from microapp.error import TestError
from microapp.utils import appdict
from microapp.parse import (AppArgParser, DataRegistry, data_transfer,
                            mgrdata_transfer)
from microapp.manage import Manager


class App(MicroappObject, AppArgParser, DataRegistry):

    def __new__(cls, mgr, *vargs, **kwargs):

        pos = sys.argv[0].rfind("-")
        if pos>=0:
            sys.argv[0] = sys.argv[0][:pos]+"-"+cls._name_

        else:
            sys.argv[0] += "-"+cls._name_

        obj = super(App, cls).__new__(cls, *vargs, **kwargs)
        obj.manager = mgr

        obj.add_argument("--forward", metavar="expr", action="append",
                delay=True, help="forward variables to next app")

        obj.add_argument("--share", metavar="expr", action="append",
                delay=True, help="share variables between sibling apps")

        obj.add_argument("--downcast", metavar="expr", action="append",
                delay=True, help="downcast variables under this app")

        # syntax: --import 'a | a from b | a as b from c'
        # order: filepath -> loaded module
        obj.add_argument("--import", metavar="modname", action="append",
                type=str, help="import python object")

        obj.add_argument("--assert-in", metavar="expr", action="append",
                eval=True, type=bool, help="assertion test on input")

        obj.add_argument("--assert-out", metavar="expr", action="append",
                eval=True, type=bool, delay=True, help="assertion test on output")

        obj.add_argument("--assert-forward", metavar="expr", action="append",
                eval=True, type=bool, delay=True, help="assertion test on the forwarded")

        obj.add_argument("--assert-share", metavar="expr", action="append",
                eval=True, type=bool, delay=True, help="assertion test on the share")

        obj.add_argument("--assert-downcast", metavar="expr", action="append",
                eval=True, type=bool, delay=True, help="assertion test on the downcast")

        obj.add_argument('--version', action='version', version=(cls._name_
                + " " + cls._version_))

        import datetime
        obj.set_config("latest.when", str(datetime.datetime.now()),
                        createall=True)

        obj._dcasts.update(mgr.iter_downcast())
        
        return obj

    def _cfgkey(self, items):

        if not items:
            newkey = "app.%s" % self._name_

        elif items[0] in ("global",):
            newkey = ".".join(items)

        elif items[0] in ("project",):
            prjname = self._dcasts["_project_"]["name"]
            newkey = "project.%s.%s" % (prjname, ".".join(items[1:]))

        else:
            newkey = "app.%s.%s" % (self._name_, ".".join(items))

        return newkey

    def get_config(self, key=None):

        items = [] if key is None else key.split(".")
        newkey = self._cfgkey(items)

        return self.manager.get_config(newkey)

    def has_config(self, key):
        items = key.split(".")
        newkey = self._cfgkey(items)

        return self.manager.has_config(newkey)

    def set_config(self, key, value, createall=False):
        items = key.split(".")
        newkey = self._cfgkey(items)

        self.manager.set_config("app.%s.%s" % (self._name_, key), value,
                createall=createall)

    def pre_perform(self, args):
        pass

    @abc.abstractmethod
    def perform(self, args):
        pass

    def run(self, args, subargs, forward):
        """app run function"""

        # do not change the following order
        self._env.update(self.manager.iter_downcast())
        self._env.update(self.manager.iter_shared())
        self._env.update(forward)

        args = self.parse_args(args, self._env)

        if args.assert_in:
            for ain in args.assert_in:
                if not ain["_"]:
                    raise TestError("Assert-in test failed.")

        # prepeform
        self.pre_perform(args)

        if args.downcast:
            #data_transfer(args.downcast, self._env, self._dcasts)
            data_transfer(args.downcast, self._dcasts)

        # perform
        ret = self.perform(args)
        if ret is None:
            ret = 0

        # postperform
        self.post_perform(args)

        if args.forward:
            data_transfer(args.forward, self._fwds)

        if args.assert_forward:
            for afwd in args.assert_forward:
                afwd.env = appdict(self._env)
                afwd.env.update(self._fwds)
                afwdval = afwd(afwd.data)
                if not afwdval["_"]:
                    raise TestError("Assert-forward test failed.")

        if args.share:
            mgrdata_transfer(args.share, self.manager.set_shared)

        if args.assert_share:
            for ashrd in args.assert_share:
                ashrd.env = appdict(self._env)
                ashrd.env.update(self._shrds)
                ashrdval = ashrd(ashrd.data)
                if not afwdval["_"]:
                    raise TestError("Assert-share test failed.")

        if args.assert_out:
            for aout in args.assert_out:
                aout.env = appdict(self._env)
                aout.env.update(self._dcasts)
                aout.env.update(self._shrds)
                aout.env.update(self._fwds)
                aoutval = aout(aout.data)
                if not aoutval["_"]:
                    raise TestError("Assert-out test failed.")

        fwds = self._fwds
        self._fwds = appdict()

        return ret, fwds

    def post_perform(self, args):
        pass

    def get_manager(self, manager_class=None):

        if manager_class is None:
            manager_class = Manager

        mgr = manager_class(self)

        return mgr

