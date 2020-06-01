'''
Created on Nov 20, 2019

@author: reynolds
'''
import unittest
from wrtdk.parser.em.em3d.em.em import emv1


class test_emv1(unittest.TestCase):


    def setUp(self):
        self.msg = b't\xd5L\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n'
        
    def tearDown(self):
        pass

    def test_parse(self):
        em = emv1()
        em.parse(self.msg)
        self.assertTrue(em.hasErrored())
        
        em.set_bins(16)
        
        em.parse(self.msg)
        
        self.assertFalse(em.hasErrored())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()