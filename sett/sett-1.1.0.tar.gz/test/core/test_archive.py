import unittest
from unittest.mock import patch
import tarfile
import io

from sett.core import archive
from sett.core.error import UserError


def prepare_archive(content):
    f_io = io.BytesIO()
    with tarfile.open(fileobj=f_io, mode='w') as tar:
        for f_name, f_content in content:
            f_io_content = io.BytesIO(f_content)
            t_info = tarfile.TarInfo(f_name)
            t_info.size = len(f_io_content.getvalue())
            tar.addfile(t_info, f_io_content)
    f_io.seek(0)
    return f_io


original_tar_open = tarfile.open


def mock_tar_open(f_io):
    def mock(*_, **__):
        return original_tar_open(fileobj=f_io)
    return mock


class TestArchive(unittest.TestCase):
    def test_check_tar(self):
        # Correct archive:
        f_io = prepare_archive((
            ("metadata.json", b'{"test": true}'),
            ("data.tar.gz.gpg", b"some initial binary data: \x00\x01")
        ))
        with patch('tarfile.open', mock_tar_open(f_io)):
            archive.check_tar("f.tar")

        # Wrong extension:
        with patch('tarfile.open', mock_tar_open(f_io)),\
                self.assertRaises(UserError):
            archive.check_tar("f")

        # Too many files in archive:
        f_io = prepare_archive((
            ("metadata.json", b'{"test": true}'),
            ("data.tar.gz.gpg", b"some initial binary data: \x00\x01"),
            ("bullshit.txt", b"....")
        ))
        with patch('tarfile.open', mock_tar_open(f_io)),\
                self.assertRaises(UserError):
            archive.check_tar("f.tar")

        # Relative path:
        f_io = prepare_archive((
            ("../metadata.json", b'{"test": true}'),
            ("data.tar.gz.gpg", b"some initial binary data: \x00\x01")
        ))
        with patch('tarfile.open', mock_tar_open(f_io)),\
                self.assertRaises(UserError):
            archive.check_tar("f.tar")
