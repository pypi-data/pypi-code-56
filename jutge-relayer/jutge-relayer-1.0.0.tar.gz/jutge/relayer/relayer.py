"""
Notifications relayer for Jutge.org
"""

import argparse
import asyncio
import json
import logging

import aioredis
import websockets as ws
from jutge import util

# use custom logging
util.init_logging()
logging.getLogger('').setLevel(logging.INFO)

# dict of users to list of ws
sockets = {}

# number of ws (just to improve speed)
number_of_websockets = 0

# number of processed subscriptions
number_of_subscriptions = 0

# number of sent notifications
number_of_notifications = 0

# args from arg parser
args: argparse.Namespace = None


async def handle_subscription(channel):
    """This coroutine is called each time a message is available on the redis channel"""
    global number_of_subscriptions, number_of_notifications

    while await channel.wait_message():
        number_of_subscriptions += 1
        message = await channel.get_json()
        try:
            user = message['user']
        except:
            return
        if user in sockets:
            data = json.dumps(message)
            for websocket in sockets[user]:
                number_of_notifications += 1
                await websocket.send(data)


async def handle_websocket(websocket, path):
    """This coroutine is called each time a client websocket connects"""
    global number_of_websockets

    # get user from the path
    user = path[1:]

    # get IP
    ip = websocket.remote_address[0]
    print(websocket.remote_address)

    # log connection
    logging.info(f'connected user={user} ip={ip}')

    # add websocket to the list of the user
    if user in sockets:
        if len(sockets[user]) > args.max_sockets:
            # too many websockets for an individual user. sucker!
            logging.info(f'sucker user={user}')
            return
        sockets[user].append(websocket)
    else:
        sockets[user] = [websocket]

    # update counter
    number_of_websockets += 1

    # discard incoming messages
    async for message in websocket:
        pass

    # websocket closes
    logging.info(f'disconnected user={user}')
    number_of_websockets -= 1
    sockets[user].remove(websocket)
    if not sockets[user]:
        del (sockets[user])


async def init_subscriptions():
    # connect to redis database
    redis = await aioredis.create_redis(args.redis_url)
    # subscribe to channel
    subscription = await redis.subscribe(args.channel)
    channel = subscription[0]
    # handle incoming messages in the channel
    await asyncio.ensure_future(handle_subscription(channel))


async def init_websockets():
    await ws.serve(handle_websocket, args.host, args.port)


async def init_timer():
    last_log = ''
    while True:
        log = f'statistics websockets={number_of_websockets} users={len(sockets)} notifications={number_of_notifications}'
        if log != last_log:
            logging.info(log)
            last_log = log
        await asyncio.sleep(args.period)


async def amain():
    global args

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Notification relayer for Jutge.org')
    parser.add_argument(
        '--hostname',
        type=str,
        help='host for the server',
        default='localhost')
    parser.add_argument(
        '--port',
        type=int,
        help='port for the server',
        default=9999)
    parser.add_argument(
        '--channel',
        type=str,
        help='name of the notifications channel',
        default='jutge.notifications')
    parser.add_argument(
        '--redis-url',
        type=str,
        help='URL for redis',
        default='redis://localhost')
    parser.add_argument(
        '--redis-password',
        type=str,
        help='auth password for redis',
        default='')
    parser.add_argument(
        '--period',
        type=int,
        help='how often to print statistics, in seconds',
        default=5)
    parser.add_argument(
        '--max-sockets',
        type=int,
        help='maximum number of connections per user before deeming it a sucker',
        default=20)
    args = parser.parse_args()

    logging.info(f'start')
    await asyncio.gather(
        init_subscriptions(),
        init_websockets(),
        init_timer(),
    )


def main():
    asyncio.run(amain())


if __name__ == '__main__':
    main()
