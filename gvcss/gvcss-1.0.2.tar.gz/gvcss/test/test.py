from ..pipeline import *

import unittest


class Test_checker(unittest.TestCase):
    def test_case1(self):
        r = check_single_fastq("gvcss/test/data/reads_case1.json")
        self.assertDictEqual(
            r, {
                "T": {
                    "R1": ["gvcss/test/data/R1.fastq"],
                    "R2": ["gvcss/test/data/R2.fastq"]
                }
            })

    def test_case2_pair(self):

        with self.assertRaises(SystemExit) as cm:
            check_single_fastq("gvcss/test/data/reads_case2.json")
        self.assertEqual(cm.exception.code, -1)

    def test_case3_pair(self):
        with self.assertRaises(SystemExit) as cm:
            check_single_fastq("gvcss/test/data/reads_case3.json")
        self.assertEqual(cm.exception.code, -2)

    def test_case4_pair(self):
        with self.assertRaises(SystemExit) as cm:
            check_single_fastq("gvcss/test/data/reads_case4.json")
        self.assertEqual(cm.exception.code, -3)

    def test_all_reads(self):
        d = get_tumor_all_reads({"T": {"R1": ["1", "2"], "R2": ["3"]}})
        self.assertListEqual(d, ["1", "2", "3"])


if __name__ == "__main__":
    unittest.main()