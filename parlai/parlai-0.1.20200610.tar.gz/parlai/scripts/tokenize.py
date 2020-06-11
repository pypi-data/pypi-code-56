#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import numpy as np
from parlai.scripts.script import ParlaiScript
from parlai.core.agents import create_agent
from parlai.core.torch_agent import TorchAgent
from parlai.core.worlds import create_task
from parlai.core.params import ParlaiParser


class Tokenize(ParlaiScript):
    @classmethod
    def setup_args(cls):
        pp = ParlaiParser(True, True)
        pp.set_defaults(no_cuda=True)
        return pp

    def run(self):
        self.opt['no_cuda'] = True
        agent = create_agent(self.opt, True)
        assert self.opt['batchsize'] == 1
        assert isinstance(agent, TorchAgent)
        world = create_task(self.opt, agent)
        teacher = world.get_task_agent()

        lengths = []

        while not teacher.epoch_done():
            act = teacher.act()
            processed = agent.observe(act)
            text_vec = processed['text_vec']
            if text_vec is not None and act.get('episode_done'):
                if False:
                    text = agent.dict.vec2txt(text_vec).replace("\n", "\\n")
                    print(" ".join(agent.dict[t.item()] for t in text_vec))
                lengths.append(len(text_vec))
            agent.self_observe({})

        print("Min:", np.min(lengths))
        print("Max:", np.max(lengths))
        print("Mean: {:.1f}".format(np.median(lengths)))
        print("p05: {:.1f}".format(np.quantile(lengths, 0.05)))
        print("p10: {:.1f}".format(np.quantile(lengths, 0.10)))
        print("p25: {:.1f}".format(np.quantile(lengths, 0.25)))
        print("p50: {:.1f}".format(np.quantile(lengths, 0.50)))
        print("p75: {:.1f}".format(np.quantile(lengths, 0.75)))
        print("p90: {:.1f}".format(np.quantile(lengths, 0.90)))
        print("p95: {:.1f}".format(np.quantile(lengths, 0.95)))


if __name__ == '__main__':
    Tokenize.main()
