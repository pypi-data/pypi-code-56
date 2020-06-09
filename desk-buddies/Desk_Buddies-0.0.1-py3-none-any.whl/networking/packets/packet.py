
# Packet structure:
# the first 4 bytes will be the length of the packet
# the next byte will be the packet identifier
# the remaining bytes will be json string representing a dictionary of values
import json
import struct

from cmnSys.action import Action


class Packet:
    # required fields for each action
    REQS = {Action.QUERY: ['uid', 'date'],
            Action.GET: ['date', 'week'],
            Action.REMOVE: ['uid', 'date']}

    def __init__(self, action: Action, data: dict):
        self.action = action
        self.data = data

    def encode(self):
        # the packet id header
        data = str(int(self.action)).encode('utf-8')
        data += json.dumps(self.data).encode('utf-8')
        # prepend the length to the front of the message
        msg = struct.pack('>I', len(data)) + data
        return msg


# removes the first 5 bytes because we don't need to except long messages on the server side
def from_server_str(stream: str) -> Packet:
    stream = stream[4:len(stream)]
    return from_str(stream)


def from_str(stream: str) -> Packet:
    action = Action(int(stream[0]))
    data = json.loads(stream[1:len(stream)])
    return Packet(action, data)


def from_args(args) -> Packet:
    data = {}
    for key in Packet.REQS[args['action']]:
        if key in args:
            data[key] = args[key]
    return Packet(args['action'], data)


