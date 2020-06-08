import numpy as np


class SpreadingModel(object):
    def __init__(self, graph):
        self.graph = graph
        self.status = {}
        self.initial_status = {}
        self.check = 0
        self.ids = self.graph.get_ids(stable=True)
        self.times = []
        self.received = []
        self.messes = []

    def set_initial_status(self, configuration):
        self.initial_status = configuration
        self.check = np.unique([j for i in configuration.values() for j in i]).size

    def init(self):
        self.status = {
            k: self.initial_status[k].copy() for k in self.initial_status.keys()
        }
        self.times = np.zeros(self.ids.size)
        self.received = np.array([len(self.initial_status[node]) for node in self.ids])
        self.messes = self.received.copy()

    def iteration_bunch(self, num_iter):
        times = []

        mx = None
        for _ in np.arange(num_iter):
            n = 0
            print(_)
            self.init()

            while np.sum(self.received < self.check) > 0:
                self.times[self.messes < self.ids.size] += 1
                n += 1
                self.iteration()

                if mx is not None:
                    if n == mx:
                        break

            mx = np.max(self.times)
            times = np.append(times, self.times)
        return times.reshape((num_iter, self.graph.size()))

    def iteration_bunch_complex(self, nodes):
        self.init()
        n = 0
        k = 0
        checked = True

        while True:
            self.iteration()
            n += 1

            if nodes is not None:
                if self.finish(nodes) and checked:
                    k = n
                    checked = False
            if self.finish():
                break
        return k, n

    def iteration_bunch_speed(self, time=None):
        self.init()
        n = 0

        while np.sum(self.received < self.check) > 0:
            self.iteration()
            n += 1

            if time is not None:
                if n > time:
                    break
        return n

    def finish(self, nodes=None):
        if nodes is None:
            nodes = self.graph.get_ids()

        for node in nodes:
            if len(self.status[node]) < self.check:
                return False
        return True

    def iteration(self):
        return None, True
