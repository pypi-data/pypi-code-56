"""

This Project is owned by RaidTheWeb

Even though IreTheKID's code is not in here.
He still helped <https://repl.it/@IreTheKID> check him out.
Thanks IreTheKID!! :)

DOCUMENTATION: 

Quick Docs: <https://repl.it/talk/link-here> !COMING SOON!

Full Docs: <https://cifproject.raidtheweb.repl.co/repltalk/docs>

NOTE: Just remembered I have to write documentation now :(


CIFReplTalk is Asyncio-Ready.

"""

################
# IMPORTS
################
import repltalk
import base64
import asyncio
import string
import random
import shelve
import os
import json


################
# KEEP ALIVE
################
from flask import Flask
from threading import Thread
app = Flask('')

@app.route('/')
def main():
    return "Status: Live"
def run():
    app.run(host="0.0.0.0", port=8080)
def keep_alive():
    server = Thread(target=run)
    server.start()



################
# SIGNER
################
class Signer():
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def sign(self, replusername):

        key = self.user + ':' + self.password + ':' + replusername

        token = base64.b64encode(key.encode())
        return token.decode()


################
# MAIN CLASS
################
class Bot():

    def __init__(self, prefix=None, handler=None, db_name='cifrepltalk.db'):
        if prefix == None:
            letters = string.ascii_lowercase

            prefix = ''.join(
                random.choice(letters) for i in range(4)
            )
            self.prefix = '$ [ {} ]'.format(prefix)
        else:
            self.prefix = prefix
        self.client = repltalk.Client()
        self.db_name = db_name
        if not handler:
            self.handler_class = Handler
        else:
            self.handler_class = handler

    def login(self, token):
        asyncio.run(
            self.login_internal(token)
        )

    async def login_internal(self, token):
        token = base64.b64decode(
            token.encode()
        ).decode()
        user, password, repluser = token.split(':')
        await self.client.login(user, password)
        self.handler = self.handler_class(
            self.prefix, self.db_name
        )
        
        
    def run(self, postid):
        asyncio.run(
            self.handler.run(self.client, postid)
        )
        return True


################
# DEFAULT HANDLER CLASS
################
class Handler():

    def __init__(self, prefix, fname):
        self.actions = {}
        self.prefix = prefix
        self.fname = fname

    async def on_message(self, message, ctx):
        if message.startswith(self.prefix):
            command = message[len(self.prefix) + 1:]
            args = command.split(' ')
            return await self.execute(
                ctx, args[0], *tuple(args[1:])
            )

    def assign(self, name, func):
        self.actions[name] = func

    def detach(self, name):
        del self.actions[name]

    async def execute(self, ctx, name, *args):
        func = self.actions[name]
        return await func(ctx, *args)

    async def nothing(self):
        pass

    async def db_write(self, data):
        d = json.loads(
            open(self.fname).read()
        )
        d += [data]
        with open(self.fname, 'w') as db_:
            db_.write(
                json.dumps(
                    d
                )
            )
            

    async def db_read(self):
        with open(self.fname) as db_:
            return json.loads(
                db_.read()
            )


    async def run(self, client, postid):
        if not os.path.exists(self.fname):
            with open(self.fname, 'w') as db_:
                db_.write(
                    json.dumps(
                        []
                    )
                )
        target = await client.get_post(postid)
        while True:
            for comment in await target.get_comments(order='new'):
                if not str(comment.id) in await self.db_read():
                    ctx = comment
                    run = await self.on_message(
                        comment.content, ctx
                    )
                    if run:
                        try:
                            await target.post_comment(run)
                        except KeyError:
                            await self.nothing()
                    await self.db_write(
                        str(comment.id)
                    )

            
