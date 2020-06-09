# These are all of the methods callable by the client, that interact with the server
from cmnSys.action import Action
from cmnSys import directoryFinder
from cmnUtils.dateUtils import string_to_datetime
from networking.packets.packet import Packet
from server.adjacencyMatrix import AdjacencyMatrix
from server.schedule import Schedule


class ServerQueryManager:

    def __init__(self):
        self.funcs = {Action.GET: self.get,
                      Action.REMOVE: self.remove,
                      Action.QUERY: self.add}

        self.schedule = Schedule(directoryFinder.server_schedule_dir())
        self.adjmat = AdjacencyMatrix(directoryFinder.server_adjacency_file(), True)

    def add(self, args: dict) -> dict:
        datetime_obj = string_to_datetime(args['date'])
        results = []
        uids_on_day = self.schedule.get(datetime_obj)
        response_code = 3

        for uid in uids_on_day:
            if self.adjmat.is_adjacent(args['uid'], uid) == True:
                results.append(uid)


        if len(results) > 0:
            # uid can't work on the same day as someone already working on that day
            response_code = 409
        else:
            added = self.schedule.add(args['uid'], datetime_obj)
            if not added:
                # uid not added successfully
                response_code = 417
            else:
                # uid added to day successfully
                response_code = 200

        response = {'responseCode': response_code, 'results': results}
        return response

    def remove(self, args: dict) -> dict:
        datetime_obj = string_to_datetime(args['date'])
        results = []
        uids_on_day = self.schedule.get(datetime_obj)

        count = uids_on_day.count(args['uid'])
        if count == 0:
            # uid not found on day
            response_code = 404
        else:
            self.schedule.remove(args['uid'], datetime_obj)
            # uid removed from day successfully
            response_code = 200

            check = self.schedule.get(datetime_obj)
            count = check.count(args['uid'])

        if count != 0:
            # uid was not removed correctly, expectation failed
            response_code = 417

        response = {'responseCode': response_code, 'results': results}

        return response

    def get(self, args: dict) -> dict:
        datetime_obj = string_to_datetime(args['date'])
        response_code = 3
        results = {}
        if not args['week']:
            results[args['date']] = self.schedule.get(datetime_obj)
            # uids on date gotten successfully
            response_code = 200
        else:
            response_code = 417

        response = {'responseCode': response_code, 'results': results}

        return response

    def respond(self, packet: Packet) -> Packet:
        args = packet.data
        return Packet(packet.action, self.funcs[packet.action](args))
