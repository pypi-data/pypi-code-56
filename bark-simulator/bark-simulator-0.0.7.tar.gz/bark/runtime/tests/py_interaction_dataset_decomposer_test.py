# Copyright (c) 2020 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
from bark.runtime.commons.parameters import ParameterServer
from bark.runtime.scenario.interaction_dataset_processing.dataset_decomposer import DatasetDecomposer
import os

class DatasetDecomposerTest(unittest.TestCase):
    def test_decompose_dataset(self):

        map_filename = os.path.join(os.path.dirname(__file__),"data/DR_DEU_Merging_MT_v01_shifted.xodr")
        track_filename = os.path.join(os.path.dirname(__file__),"data/interaction_dataset_dummy_track.csv")

        dataset_decomposer = DatasetDecomposer(
            map_filename=map_filename, track_filename=track_filename)

        dataset_decomposer.decompose()



if __name__ == '__main__':
    unittest.main()

