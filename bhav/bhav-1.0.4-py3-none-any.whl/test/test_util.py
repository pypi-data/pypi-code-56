import unittest
from bhav.util import today, fetch, unzip, writeCSV, readCSV, dateList

class TestUtilMethods(unittest.TestCase):
    def test_dateList(self):
        self.assertEqual(dateList('20200520', '20200529'), list(['20200520', '20200521', '20200522', '20200523', '20200524', '20200525', '20200526', '20200527', '20200528', '20200529']))

if __name__ == '__main__':
    unittest.main()