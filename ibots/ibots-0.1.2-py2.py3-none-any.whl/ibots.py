import os
import time
import json
import logging
import requests
import argparse
import importlib

from flask import Flask, request
from threading import Thread, Lock, Event

logger = logging.getLogger('CONTROL')

DIR = os.path.dirname(os.path.realpath(__file__))


class Waiter:
    def __init__(self, endpoint, period=1):
        self._endpoint = endpoint
        self._period = period

    def poll(self):
        self._event = Event()
        latest = ''
        while True:
            response = requests.get('{}/ibis/wait'.format(self._endpoint))
            if response.text != latest:
                self._event.set()
                self._event = Event()
                latest = response.text
            time.sleep(self._period)

    def wait(self, event_last=None, timeout=None):
        event = event_last if event_last else self._event

        if event.wait(timeout):
            return True, event
        else:
            return False, event


def start(port, config, bots=[]):
    waiter = Waiter(config['global']['endpoint'])

    # how to spin this off as a daemon?
    assert all(x in config['bots'] for x in bots)
    if not bots:
        bot_names = set(x for x in config['bots'])

    assert all(
        y in config['resources'] for x in bots for y in config[x]['resources'])
    resource_names = set(y for x in bots for y in config[x]['resources'])

    # instantiate resources
    resources = {
        x: importlib.__import__(x['class'])(
            Lock(),
            **config['resources'][x]['args'],
        )
        for x in resource_names
    }

    # instantiate bots
    bots = {
        getattr(
            __import__(
                config['bots'][x]['module'],
                fromlist=config['bots'][x]['class']),
            config['bots'][x]['class'])(
                config['global']['endpoint'],
                x,
                config['global'][x]['password'],
                {y: resources[y]
                 for y in config['bots'][x]['resources']},
                waiter,
            )
        for x in bot_names
    }

    # start bots
    for x in bots:
        x.start(**config[x]['args'])

    # run api polling
    poll_thread = Thread(target=waiter.poll, daemon=True)
    poll_thread.start()

    # run bots
    threads = {x: Thread(target=x.run, daemon=True) for x in bots}
    for x in threads:
        threads[x].start()

    # start server
    app = Flask(__name__)

    @app.route('/pause', methods=['POST'])
    def pause():
        print(dict(request.form))

    @app.route('/resource', methods=['POST'])
    def resource():
        for x in request.form.targets:
            resources[x].execute(request.form.instruction)

    @app.route('/bot', methods=['POST'])
    def bot():
        for x in request.form.targets:
            bots[x].execute(request.form.instruction)

    @app.route('/interact', methods=['POST'])
    def interact():
        interact_thread = Thread(bots[x].interact)
        interact_thread.start()

    app.run(port=port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config',
        help='Configuration file',
    )
    parser.add_argument(
        '-p',
        '--port',
        help='Port number',
        default=8000,
    )
    parser.add_argument(
        '-b',
        '--bots',
        nargs='+',
        default=[],
        help='List of bots',
    )
    parser.add_argument(
        '-d',
        '--directory',
        help='Working directory',
        default=os.path.join(DIR, '..', 'output'),
    )

    args = parser.parse_args()

    with open(args.config) as fd:
        config = json.load(fd)

    start(args.port, config, args.bots)
