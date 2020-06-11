#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Test many variants of transformers.
"""

import unittest
import parlai.utils.testing as testing_utils
from parlai.core.opt import Opt


class TestClassifier(unittest.TestCase):
    """
    Test transformer/classifier.
    """

    @testing_utils.retry()
    def test_simple(self):
        valid, test = testing_utils.train_model(
            Opt(
                dict(
                    task='integration_tests:classifier',
                    model='parlai_internal.agents.retnref_style.retnref_style:ClassifierOnGeneratorAgent',
                    classes=['one', 'zero'],
                    optimizer='adamax',
                    truncate=8,
                    learningrate=7e-3,
                    batchsize=32,
                    num_epochs=5,
                    n_layers=1,
                    n_heads=1,
                    ffn_size=32,
                    embedding_size=32,
                )
            )
        )
        assert valid['accuracy'] > 0.97
        assert test['accuracy'] > 0.97


if __name__ == '__main__':
    unittest.main()
