import os
from pathlib import Path
import unittest

from file_item import File

TEST_PATH = '/home/user/test.csv'
TEST_PATH2 = '/home/user/test2.csv'


class TestItem(unittest.TestCase):
    def setUp(self) -> None:
        self.file = File(TEST_PATH)
        self.file2 = File(TEST_PATH2)

    def test_basedir(self):
        basedir = File.basedir(__file__)
        self.assertEqual(basedir, Path(__file__).parent)

    def test_init_str(self):
        f = File(TEST_PATH)
        fp = Path(TEST_PATH)
        self.assertEqual(f.path, fp)

    def test_init_posix(self):
        p = Path(TEST_PATH)
        f = File(p)
        self.assertEqual(f.path, p)

    def test_init_wrong(self):
        with self.assertRaises(Exception) as ctx:
            File(2)
        self.assertTrue('The path variable should be str or PosixPath' in str(ctx.exception))

    def test_repr(self):
        self.assertEqual(repr(self.file), f'File(path="{TEST_PATH}")')

    def test_str(self):
        self.assertEqual(str(self.file), TEST_PATH)

    def test_eq_self(self):
        file2 = File(TEST_PATH)
        self.assertTrue(self.file == file2)

    def test_no_eq(self):
        self.assertFalse(self.file == self.file2)

    def test_eq_posix(self):
        p = Path(str(self.file.path))
        self.assertTrue(self.file == p)

    def test_eq_str(self):
        p = str(self.file.path)
        self.assertTrue(self.file == p)

    def test_name(self):
        self.assertEqual(self.file.name, 'test.csv')

    def test_create_folder(self):
        b_folder = File.basedir(__file__)
        folder = b_folder.joinpath('test_folder')
        path = folder.joinpath('test.csv')
        file_ = File(path)
        file_.create_folder()
        i = [i for i in os.listdir(str(b_folder))]
        self.assertIn('test_folder', i)
        os.rmdir(str(path))
        
    def test_from_strings(self):
        fp = '/home/user/'
        fn = 'test.csv'
        f = File.from_strings(fp, fn)
        self.assertTrue(f == self.file)

    def test_get_file_name_basic(self):
        self.assertEqual(File.get_file_name('test*.csv'), 'test-.csv')

    def test_get_file_name_replacer(self):
        self.assertEqual(File.get_file_name('test*.csv', replacer='_'), 'test_.csv')

    def test_get_file_name_ext(self):
        self.assertEqual(File.get_file_name('test*', ext='csv'), 'test-.csv')
        
    def test_get_file_name_wrong_replacer(self):
        with self.assertRaises(Exception) as ctx:
            File.get_file_name('test*.csv', replacer='>')
        self.assertTrue('replacer can\'t be in ' in str(ctx.exception))
