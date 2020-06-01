'''
Created on Apr 3, 2020

@author: Reynolds
'''
import unittest
from wrtdk.parser.em.em3d.em.em import emv2


class Test(unittest.TestCase):


    def setUp(self):
        self.msg = b't\xd3V|\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n'


    def tearDown(self):
        pass


    def testParse(self):
        em = emv2()
        em.set_bins(16)
        
        em.parse(self.msg)
        self.assertFalse(em.hasErrored())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()