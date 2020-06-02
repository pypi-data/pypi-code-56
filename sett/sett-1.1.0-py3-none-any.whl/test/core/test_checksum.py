import unittest
import io

from sett.core import checksum, error


class TestChecksum(unittest.TestCase):
    def test_read_checksum_file(self):
        ref_checks = [
            ("a7186ae7ff993b379qcf3567775cfc71a212rf217e4dd", "testDir/file1.fastq"),
            ("a7186ae7ff993b379qcf3567775cfc71a212rf217e4dd",
             "testDir/file with spaces.fastq"),
            ("f8d2d394264823e711fgc34e4ac83f8cbc253c6we034f", "testDir/file2.fastq"),
            ("78f3b23fe49cf5f7f245ddf43v9788d9e62c0971fe5fb",
             "testDir/subdir2/file4.fastq")
        ]
        checksum_file_object = io.BytesIO(b"\n".join(
            sha.encode() + b' ' + name.encode() for sha, name in ref_checks))
        checks = list(checksum.read_checksum_file(checksum_file_object))
        self.assertEqual(checks, ref_checks)

        checksum_file_object = io.BytesIO(b".........")
        with self.assertRaises(error.UserError):
            checks = list(checksum.read_checksum_file(checksum_file_object))

    def test_compute_checksum_sha256(self):
        text = b'Mock an item where it is used, not where it came from.\n'\
               b'Mock an item where it is used, not where it came from.'
        expected_hash = '7ce0ad43befbf2b2e43fb108184ca6a4e3bd8ab8e05296d7890'\
                        'c523ad76d2bc7'
        hash1 = checksum.compute_checksum_sha256(file_object=io.BytesIO(text))
        hash2 = checksum.compute_checksum_sha256(file_object=io.BytesIO(text),
                                                 block_size=5)
        self.assertEqual(hash1, expected_hash,
                         f'global fraction should be {expected_hash}')
        self.assertEqual(hash2, expected_hash,
                         f'global fraction should be {expected_hash}')

    def test_write_checksums(self):

        class BytesIOWithName(io.BytesIO):
            def __init__(self, binary_content, file_name, *args, **kwargs):
                self.name = file_name
                io.BytesIO.__init__(self, binary_content, *args, **kwargs)

        files = ['/test/file1.txt', '/test/file2.txt']
        content = [b'Mock an item where it is used, not where it came from.\n'
                   b'Mock an item where it is used, not where it came from.',
                   b'This is the content of the second file.']
        fake_files = [BytesIOWithName(binary_content, file_name) for
                      binary_content, file_name in zip(content, files)]

        checksums = checksum.write_checksums(
            zip(('content/file1.txt', 'content/file2.txt'), fake_files))
        self.assertEqual(checksums,
                         b"7ce0ad43befbf2b2e43fb108184ca6a4e3bd8ab8e05296d789"
                         b"0c523ad76d2bc7 content/file1.txt\n"
                         b"860282aecc2a0b9efc6356aef13b56d46f26fad8824a3950df"
                         b"ea138ccf0e66c6 content/file2.txt\n")
