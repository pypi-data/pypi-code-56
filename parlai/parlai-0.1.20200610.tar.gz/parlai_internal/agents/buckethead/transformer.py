#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Transformer Agents.
"""

from parlai.agents.transfomer.transformer import TransformerGeneratorModel
from parlai.agents.transfomer.modules import TransformerGeneratorModel

import torch

from .modules import BucketheadGeneratorModel


class BucketheadAgent(TransformerGeneratorAgent):
    @classmethod
    def add_cmdline_args(cls, argparser):
        """
        Add command-line arguments specifically for this agent.
        """
        agent = argparser.add_argument_group('Buckethead Arguments')
        agent.add_argument('--buckets', type=int, default=32)
        agents.add_argument('--max-position', type=int, default=128)
        super(BucketheadAgent, cls).add_cmdline_args(argparser)
        return agent

    def build_model(self, states=None):
        """
        Build and return model.
        """
        model = BucketheadModel(self.opt, self.dict)
        if self.opt['embedding_type'] != 'random':
            self._copy_embeddings(
                model.encoder.embeddings.weight, self.opt['embedding_type']
            )
        return model
