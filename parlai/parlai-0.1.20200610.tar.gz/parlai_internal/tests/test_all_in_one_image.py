#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import unittest
import parlai.utils.testing as testing_utils

"""
Integration tests for the All In One Image project

See parlai_internal/agents/comment_battle_all_in_one/comment_battle_all_in_one.py
"""


FAST_MODE = True
NUM_EXAMPLES = 512 if FAST_MODE else -1
MODEL_PATH = '/checkpoint/parlai/zoo/all_in_one_image/uru_only_model/model'


@testing_utils.skipUnlessGPU
class TestAllInOneImageModel(unittest.TestCase):
    def test_model(self):
        """
        Check the all-in-one image model.
        """
        valid, _ = testing_utils.eval_model(
            {
                'model_file': MODEL_PATH,
                'task': 'internal:comment_battle:imageDialog',
                'batchsize': 32,
                'image_mode_internal': 'uru',
                'fp16': True,
                'encode_detectron': False,
                'num_cands': '100',
                'num_examples': NUM_EXAMPLES,
            },
            skip_test=True,
        )

        if FAST_MODE:
            self.assertAlmostEqual(valid['accuracy'], 0.5549, delta=0.01)
        else:
            self.assertAlmostEqual(valid['accuracy'], 0.5742, delta=0.01)


if __name__ == '__main__':
    unittest.main()
