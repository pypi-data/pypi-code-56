
import unittest
from bnbxrate.bnb import BNB


class TestMethods(unittest.TestCase):
    def testrun_bnb(self):
        """BNB get USD/BGN rate for date 01.01.2020."""
        self.assertEqual(BNB().get_rate('01.01.2020'),
                         {'31.12.2019': '1.74099'})
