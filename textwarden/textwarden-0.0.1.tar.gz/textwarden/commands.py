"""
Commands.
"""

from textwarden import config
from textwarden import database as db
from textwarden import tools
from textwarden import users
import textwrap
import time

class command(object):
    def __init__(self, f):
        self.f = f
    def __call__(self, msg):
        user = users.User(msg.author.id)
        if not user.load():
            user.save()
        user.access()
        return self.f(msg)

class dev_command(object):
    def __init__(self, f):
        self.f = f
    def __call__(self, msg):
        if str(msg.author.id) not in config.devs:
            return("🚫 Only devs can use this command!")
        return self.f(msg)

@command
def echo(msg):
    _, argstring = tools.cmd_arg_split(msg)
    return argstring if argstring else "<empty>"

@command
@dev_command
def dumps(msg):
    _, argstring = tools.cmd_arg_split(msg)
    user = users.User(tools.id_from_mention(argstring.strip()))
    return str(user)

