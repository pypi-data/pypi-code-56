#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from parlai.agents.transformer.transformer import (
    TransformerClassifierAgent,
    TransformerGeneratorAgent,
)
from parlai.core.agents import create_agent, create_agent_from_shared
from parlai.core.metrics import AverageMetric
from parlai.utils.safety import OffensiveLanguageClassifier
from parlai.utils.typing import TShared

from parlai_internal.tasks.reddit_topics.constants import CLASS_LST, NONE, POLITICS, RELIGION, MEDICAL, NSFW, DRUGS

import os
import random


CANNED_RESPONSE = (
    "I'm sorry, I'm not sure what to say. Do you want to talk about something else?"
)
NONSEQ_PATH = "/checkpoint/parlai/projects/safeways/data/nonseqs.txt"

TOPICS_THRESHOLDS = {
    POLITICS: 0.5,
    RELIGION: 0.75,
    MEDICAL: 0.5,
    NSFW: 0.8,
    DRUGS: 0.5,
}


class TopicsClassifier:
    """
    Load model to detect sensitve topics
    """

    def __init__(self, shared: TShared = None):
        if not shared:
            self.model = self._create_topics_model()
        else:
            self.model = create_agent_from_shared(shared['model'])
        self.classes = CLASS_LST
        self.thresholds = TOPICS_THRESHOLDS

    def share(self):
        shared = {'model': self.model.share()}
        return shared

    def _create_topics_model(self):
        from parlai.core.params import ParlaiParser

        parser = ParlaiParser(False, False)
        TransformerClassifierAgent.add_cmdline_args(parser)
        parser.set_params(
            model='transformer/classifier',
            model_file='/checkpoint/edinan/20200520/safety_dance2/638/model',
            interactive_mode=True,
            print_scores=True,
        )
        safety_opt = parser.parse_args([], print_args=False)
        return create_agent(safety_opt)

    def about_sensitive_topic(self, text):
        """
        Returns the probability that a message is safe according to the classifier.
        """
        act = {'text': text, 'episode_done': True}
        self.model.observe(act)
        response = self.model.act()['text']
        pred_class, prob = [x.split(': ')[-1] for x in response.split('\n')]
        prob = float(prob)  # cast string to float
        if pred_class != NONE and prob < self.thresholds[pred_class]:
            pred_class = NONE

        return pred_class != NONE, prob


class SafetyMixin(object):
    """
    Abstract mixin for wrapping an agent's responses for safety.
    """

    @classmethod
    def add_cmdline_args(cls, argparser):
        grp = super(SafetyMixin, cls).add_cmdline_args(argparser)
        grp.add_argument(
            '--response',
            default='nonseqs',
            type=str,
            choices={'canned', 'nonseqs'},
            help='Which kind of response to use when unsafe content is detected',
        )
        grp.add_argument(
            '--classifiers',
            default='all',
            type=str,
            choices={'all', 'safety', 'topics'},
            help='Which classifiers to use',
        )
        grp.add_argument(
            '--replace',
            default='reply',
            type=str,
            choices={'all', 'input', 'reply'},
            help='When to replace unsafe response: on model reply, on model input, or both',
        )

    def __init__(self, opt, shared=None):
        super().__init__(opt, shared)
        if shared is not None:
            self.classifiers = shared['classifiers']
            self.nonseqs = shared['nonseqs']
        else:
            self.classifiers = [None, None]
            if opt['classifiers'] == 'all' or opt['classifiers'] == 'safety':
                self.classifiers[0] = OffensiveLanguageClassifier()
            if opt['classifiers'] == 'all' or opt['classifiers'] == 'topics':
                self.classifiers[1] = TopicsClassifier()
            self.nonseqs = self._load_nonseqs()

    def _load_nonseqs(self):
        with open(NONSEQ_PATH, 'r') as f:
            lines = f.read().splitlines()
        return lines

    def share(self):
        shared = super().share()
        shared['classifiers'] = self.classifiers
        shared['nonseqs'] = self.nonseqs
        return shared

    def check_ok(self, text):
        if self.classifiers[0] is not None:
            pred, _ = self.classifiers[0].contains_offensive_language(text)
            if pred:
                return False
        if self.classifiers[1] is not None:
            pred, _ = self.classifiers[1].about_sensitive_topic(text)
            if pred:
                return False

        return True

    def get_safe_response(self):
        resp = self.opt['response']
        if resp == 'canned':
            return CANNED_RESPONSE
        if resp == 'nonseqs':
            return random.choice(self.nonseqs)

        raise RuntimeError(f'{resp} not yet supported')

    def eval_step(self, batch):
        inpt = [obs.get('text') for obs in batch.observations]
        outpt = super().eval_step(batch)
        safe_output = outpt.text
        flags = []
        for i, text in enumerate(outpt.text):
            ok = True
            if self.opt['replace'] == 'all' or self.opt['replace'] == 'input':
                if inpt[i]:
                    ok = self.check_ok(inpt[i])
                if not ok:
                    safe_output[i] = self.get_safe_response()
            if ok and (self.opt['replace'] == 'all' or self.opt['replace'] == 'reply'):
                if text:
                    ok = self.check_ok(text)
                if not ok:
                    safe_output[i] = self.get_safe_response()
            flags.append(int(not ok))

        self.record_local_metric('safety_flags', AverageMetric.many(flags))

        outpt['text'] = safe_output
        return outpt


class TransformerGeneratorSafeAgent(SafetyMixin, TransformerGeneratorAgent):
    """
    Wrapping transformer generator into a safe agent.

    Ex:
    ```
    python examples/interactive.py -m parlai_internal.agents.safety_wrapper.safety_wrapper:TransformerGeneratorSafeAgent -mf zoo:blender/blender_90M/model
    ```
    """

    pass
