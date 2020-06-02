import unittest
from pathlib import Path
from unittest import mock

from sett.core import error
from sett.core.filesystem import search_files_recursively, delete_files, \
    form_output_tar_name


class TestFilesystem(unittest.TestCase):

    def test_search_files_recursively_with_non_existing_path(self):
        with self.assertRaises(error.UserError):
            list(search_files_recursively(list('does_not_exist')))

    def test_search_files_recursively(self):
        docs = Path(__file__).parent.parent.parent / 'docs'
        f = Path(__file__)
        self.assertTrue(docs.exists())
        found = list(search_files_recursively(list([docs, f])))
        self.assertEqual(len(found), len(list(docs.rglob("*"))))

    @staticmethod
    def test_delete_files_with_non_existing_paths():
        delete_files('does_not_exist_1', 'does_not_exist_2')

    @mock.patch('sett.core.filesystem.os')
    @mock.patch('sett.core.filesystem.os.path')
    def test_delete_files(self, mock_path, mock_os):
        f = ["1", "2"]
        mock_path.exists.return_value = True
        delete_files(*f)
        self.assertEqual(mock_os.unlink.call_count, 2)

    @mock.patch('sett.core.filesystem.os.path')
    def test_delete_files_failed(self, mock_path):
        mock_path.exists.return_value = True
        with self.assertRaises(error.UserError):
            # As '1' does NOT exist, 'unlink' will fail
            delete_files("1")

    def test_form_output_tar_name(self):
        tar_name = form_output_tar_name("1")
        self.assertIsInstance(tar_name, str)
        self.assertTrue(tar_name.endswith("1.tar"))
        tar_name = form_output_tar_name("1.tar")
        self.assertTrue(tar_name.endswith("1.tar"))

    def test_form_output_tar_name_failing(self):
        with self.assertRaises(error.UserError) as context:
            form_output_tar_name("d/1")
        self.assertEqual(str(context.exception),
                         'output directory does not exist: d')
