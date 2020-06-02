import unittest
from unittest import mock

import io

from sett.protocols import liquid_files


class _TestLiquidFilesBase:
    data = b".....:::::"
    upload_attachment_args = {}
    expected_post_calls = []

    @classmethod
    def test_upload_attachment(cls):
        mock_post = mock.Mock(return_value=b"3")

        def mock_multipart_encode(*args, **kwargs):
            return ("mock_content_type", {"args": args, "kwargs": kwargs})
        with mock.patch('builtins.open', lambda *args, **kwargs: io.BytesIO(cls.data)), \
                mock.patch('sett.protocols.liquid_files.post', mock_post), \
                mock.patch('sett.protocols.liquid_files.multipart_encode',
                           mock_multipart_encode):
            liquid_files.upload_attachment(**cls.upload_attachment_args)
        mock_post.assert_has_calls(cls.expected_post_calls)


class TestLiquidFilesSingle(unittest.TestCase, _TestLiquidFilesBase):
    upload_attachment_args = dict(
        host="host/", api_key="api_key", file_path="data.tar", chunk_size=1024)
    expected_post_calls = [
        mock.call(
            "host/attachments", {
                "args": ("Filedata", "data.tar", _TestLiquidFilesBase.data),
                "kwargs": {}},
            "api_key", "mock_content_type")
    ]


class TestLiquidFilesChunks(unittest.TestCase, _TestLiquidFilesBase):
    upload_attachment_args = dict(
        host="host/", api_key="api_key", file_path="data.tar", chunk_size=5)
    expected_post_calls = [
        mock.call(
            "host/attachments", {
                "args": ("Filedata", "data.tar", b"....."),
                "kwargs": {"extra_data": (("name", "data.tar"), ("chunk", 0), ("chunks", 2))}},
            "api_key", "mock_content_type"),
        mock.call(
            "host/attachments", {
                "args": ("Filedata", "data.tar", b":::::"),
                "kwargs": {"extra_data": (("name", "data.tar"), ("chunk", 1), ("chunks", 2))}},
            "api_key", "mock_content_type")
    ]
