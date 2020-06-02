#!/usr/bin/env python
#
# This file is part of Zepl Broker: https://gitlab.com/zepl1/zepl-broker
# (C)2020 Leonard Pollak <leonardp@tr-host.de>
#
# SPDX-License-Identifier:    AGPL-3

import sys, os, hashlib, binascii
import datetime as dt
import json

import asyncio
import zmq.asyncio

from pprint import pprint

from zepl_broker import ZeplBroker

def main():
    print(f'-- Starting Zepl Broker --')

    lc = ZeplBroker()
    try:
        loop = asyncio.get_event_loop()
        lc.start()
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        lc.stop() # how to clean shutdown?????
        print(f'-- Zepl Broker Terminated --')

if __name__ == '__main__':
    main()
