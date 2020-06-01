'''
Created on Apr 3, 2020

@author: Reynolds
'''
import unittest
from wrtdk.parser.em.em3d.conf.conf import confv5


class Test(unittest.TestCase):

    def setUp(self):
        self.msg = b'CONF\xa9\x05\x00\x00\x04\xea\x02\xfa\xe27\n\x05\x13\x88\x00\x1e\x11\x03 \x03\x06\x03\x10\x00\x05\x00\x10\x00!\x008\x00U\x00x\x00\xa1\x00\xd0\x01\x04\x01>\x01~\x01\xc4\x02\x10\x02b\x02\xba\x03 \n'

    def tearDown(self):
        pass

    def testParse(self):
        c = confv5()
        c.parse(self.msg)
        print(c.getData())
        self.assertFalse(c.hasErrored())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()