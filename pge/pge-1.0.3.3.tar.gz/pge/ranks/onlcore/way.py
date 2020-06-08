import numpy as np

from dtg.stationary.dierckx import stat_exponential
from dtg.stationary.giratis import stat_plain
from pge.ranks.extrem_onl import NodeExInfo


class WayEx(NodeExInfo):
    @staticmethod
    def get_exes_comm(gr, nodes, params):
        res = []
        for params_ in params:
            cls = gr.get_attributes(params_[0], nodes)
            ex = 1
            u = np.max(cls)
            for u in np.unique(cls)[::-1]:
                ts = np.array(gr.get_all_short_pathes(nodes[cls > u])[1])
                if ts.size == 0:
                    continue

                if np.max(ts) > 2:
                    ex = min(
                        [
                            1,
                            2
                            * np.sum(ts - 1) ** 2
                            / (ts.size * np.sum(np.multiply(ts - 1, ts - 2))),
                        ]
                    )
                else:
                    ex = min([1, 2 * np.sum(ts) ** 2 / (ts.size * np.sum(ts ** 2))])
                if ex < 1:
                    break
            res.append((ex, u))
        return res

    @staticmethod
    def get_test_comm(gr, nodes, level, param):
        if nodes.size == 0:
            return (0, 0), (0, 0)

        cls = gr.get_attributes(param, nodes)
        ts = gr.get_all_short_pathes(nodes[cls > level], plain=True)[1]
        if ts.size == 0:
            return (0, 0), (stat_plain(cls), np.mean(cls))

        q = np.sum(gr.get_attributes(param) > level) / gr.size()
        return (
            (
                stat_exponential(ts, q),
                q
                * np.sum([np.sum(ti) for ti in ts])
                / np.sum([np.size(ti) for ti in ts]),
            ),
            (stat_plain(cls), np.mean(cls)),
        )
