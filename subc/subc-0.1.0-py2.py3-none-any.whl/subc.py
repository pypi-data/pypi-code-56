#!/usr/bin/env python3
"""
A simple sub-command library for writing rich CLIs
"""
import argparse
from abc import ABC
from abc import abstractproperty
from abc import abstractmethod


class Command(ABC):
    """
    A simple class for implementing sub-commands in your command line
    application. Create a subclass for your app as follows:

        class MyCmd(subc.Command):
            pass

    Then, each command in your app can subclass this, implementing the three
    required fields:

        class HelloWorld(MyCmd):
            name = 'hello-world'
            description = 'say hello'
            def run(self):
                print('hello world')

    Finally, use your app-level subclass for creating an argument parser:

        def main():
            parser = argparse.ArgumentParser(description='a cool tool')
            MyCmd.add_commands(parser)
            args = parser.parse_args()
            args.func(args)
    """

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def description(self):
        pass

    def add_args(self, parser):
        pass  # default is no arguments

    @abstractmethod
    def run(self):
        pass

    def base_run(self, args):
        self.args = args
        return self.run()

    @classmethod
    def add_commands(cls, parser):
        subparsers = parser.add_subparsers(title='sub-command')
        for subcls in cls.__subclasses__():
            cmd = subcls()
            cmd_parser = subparsers.add_parser(cmd.name, description=cmd.description)
            cmd.add_args(cmd_parser)
            cmd_parser.set_defaults(func=cmd.base_run)
        def default(*args, **kwargs):
            raise Exception('you must select a sub-command')
        parser.set_defaults(func=default)
        return parser
