from typing import Union, List, Tuple, Generator
from pathlib import Path
from struct import unpack, pack
from lxml import etree
from io import BytesIO
from ..ciphers.ripemd128 import Ripemd128
import zlib


class IOWrapper:
    def __init__(self, file_path: Union[str, Path] = None, binary_data: bytes = None, io_buffer=None,
                 mode: str = 'rb', offset: int = None, whence: int = 0):
        if file_path is not None:
            file = open(file_path, mode)
            self.__buffer__ = file
        elif binary_data is not None:
            self.__buffer__ = BytesIO(binary_data)
        elif io_buffer is not None:
            self.__buffer__ = io_buffer
        else:
            self.__buffer__ = BytesIO()
        if offset is not None:
            self.__buffer__.seek(offset, whence)

    @property
    def io(self):
        return self.__buffer__


class MdictHeaderBlock:
    @classmethod
    def read(cls, buffer: IOWrapper):
        buffer = buffer.io
        header_block_size = unpack('>I', buffer.read(4))[0]
        header_binary = buffer.read(header_block_size)
        adler32_checksum = unpack('<I', buffer.read(4))[0]
        assert adler32_checksum == zlib.adler32(header_binary) & 0xffffffff
        header_text = header_binary[:-2].decode('utf-16').strip()
        header_root = etree.fromstring(header_text)
        headers = {key: value for key, value in header_root.items()}
        return headers

    @classmethod
    def build(cls, headers: dict, buffer: IOWrapper = None):
        header_root = etree.Element('Dictionary', attrib=headers)
        header_binary = etree.tostring(header_root).decode('utf-8').encode('utf-16') + b'\x00\x00'
        adler32_checksum = zlib.adler32(header_binary) & 0xffffffff
        binary_data = pack('>I', len(header_binary)) + header_binary + pack('<I', adler32_checksum)
        if buffer is not None:
            buffer.io.write(binary_data)
        return binary_data


class MdictKeyMetaBlock:
    @classmethod
    def read(cls, headers: dict, buffer: IOWrapper, block_offset: int, whence: int = 0):
        buffer = buffer.io
        buffer.seek(block_offset, whence)
        version = float(headers['GeneratedByEngineVersion'])
        meta_width = 4 if version < 2.0 else 8
        meta_format = '>I' if version < 2.0 else '>Q'
        meta_block_binary = buffer.read(4 * 4 if version < 2.0 else 8 * 5)
        meta_block_io = BytesIO(meta_block_binary)
        key_blocks_count = unpack(meta_format, meta_block_io.read(meta_width))[0]
        entries_count = unpack(meta_format, meta_block_io.read(meta_width))[0]
        if version >= 2.0:
            key_info_block_decompressed_size = unpack(meta_format, meta_block_io.read(meta_width))[0]
        else:
            key_info_block_decompressed_size = None
        key_info_block_size = unpack(meta_format, meta_block_io.read(meta_width))[0]
        key_block_size = unpack(meta_format, meta_block_io.read(meta_width))[0]
        if version >= 2.0:
            adler32_checksum = unpack('>I', buffer.read(4))[0]
            assert adler32_checksum == zlib.adler32(meta_block_binary) & 0xffffffff
        return {
            'key_blocks_count': key_blocks_count,
            'entries_count': entries_count,
            'key_info_block_size': key_info_block_size,
            'key_block_size': key_block_size,
            'key_info_block_decompressed_size': key_info_block_decompressed_size
        }

    @classmethod
    def build(cls, meta: dict, buffer: IOWrapper = None, block_offset: int = None, whence: int = 0):
        meta_format = '>Q'
        meta_block_binary = \
            pack(meta_format, meta['key_blocks_count']) + \
            pack(meta_format, meta['entries_count']) + \
            pack(meta_format, meta['key_info_block_decompressed_size']) + \
            pack(meta_format, meta['key_info_block_size']) + \
            pack(meta_format, meta['key_block_size'])
        binary_data = \
            meta_block_binary + \
            pack('>I', zlib.adler32(meta_block_binary) & 0xffffffff)
        if buffer is not None:
            if block_offset is not None:
                buffer.io.seek(block_offset, whence)
            buffer.io.write(binary_data)
        return binary_data


class MDictKeyInfoBlock:
    @classmethod
    def read(cls, headers: dict, buffer: IOWrapper, block_offset: int, block_size: int, whence: int = 0):
        version = float(headers['GeneratedByEngineVersion'])
        encoding = headers['Encoding'].lower() or 'utf-16'
        meta_width = 4 if version < 2.0 else 8
        meta_format = '>I' if version < 2.0 else '>Q'
        byte_format = '>B' if version < 2 else '>H'
        byte_width = 1 if version < 2 else 2
        text_terminal = 0 if version < 2 else 1
        buffer = buffer.io
        buffer.seek(block_offset, whence)
        key_info_block_binary = buffer.read(block_size)
        key_info_io = BytesIO(key_info_block_binary)
        if version >= 2:
            assert key_info_io.read(4) == b'\x02\x00\x00\x00'
            key = key_info_io.read(4)
            adler32_checksum = unpack('>I', key)[0]
            compressed = key_info_io.read()
            if int(headers['Encrypted']) & 0x02:
                key = bytearray(Ripemd128.hash(key + pack(b'<L', 0x3695)))
                data = bytearray(compressed)
                previous = 0x36
                for i in range(len(data)):
                    t = (data[i] >> 4 | data[i] << 4) & 0xff
                    t = t ^ previous ^ (i & 0xff) ^ key[i % len(key)]
                    previous = data[i]
                    data[i] = t
                compressed = bytes(data)
            decompressed = zlib.decompress(compressed)
            assert adler32_checksum == zlib.adler32(decompressed) & 0xffffffff
            max_size = len(decompressed)
            key_info_io = BytesIO(decompressed)
        else:
            max_size = len(key_info_block_binary)
        key_block_info = []
        offset = 0
        while key_info_io.tell() < max_size:
            entry_count = unpack(meta_format, key_info_io.read(meta_width))[0]
            first_headword_size = unpack(byte_format, key_info_io.read(byte_width))[0] + text_terminal
            if encoding == 'utf-16':
                first_headword_size *= 2
            first_headword = key_info_io.read(first_headword_size).strip(b'\x00')
            last_headword_size = unpack(byte_format, key_info_io.read(byte_width))[0] + text_terminal
            if encoding == 'utf-16':
                last_headword_size *= 2
            last_headword = key_info_io.read(last_headword_size).strip(b'\x00')
            compressed_size = unpack(meta_format, key_info_io.read(meta_width))[0]
            decompressed_size = unpack(meta_format, key_info_io.read(meta_width))[0]
            key_block_info.append({
                'offset': block_offset + block_size + offset,
                'entry_count': entry_count,
                'first_headword': first_headword,
                'last_headword': last_headword,
                'compressed_size': compressed_size,
                'decompressed_size': decompressed_size
            })
            offset += compressed_size
        return key_block_info

    @classmethod
    def build(cls):
        pass


class MDictKeyBlock:
    @classmethod
    def read(cls, headers: dict, block_info: dict, buffer: IOWrapper):
        block_size = block_info['compressed_size']
        version = float(headers['GeneratedByEngineVersion'])
        encoding = headers['Encoding'].lower() or 'utf-16'
        meta_width = 4 if version < 2.0 else 8
        meta_format = '>I' if version < 2.0 else '>Q'
        delimiter = b'\x00\x00' if encoding == 'utf-16' else b'\x00'
        width = 2 if encoding == 'utf-16' else 1
        buffer = buffer.io
        buffer.seek(block_info['offset'], 0)
        key_block_binary = buffer.read(block_size)
        key_block_io = BytesIO(key_block_binary)
        key_block_type = key_block_io.read(4)
        adler32_checksum = unpack('>I', key_block_io.read(4))[0]
        if key_block_type == b'\x00\x00\x00\x00':  # No compression
            key_block = key_block_io.read()
        elif key_block_type == b'\x01\x00\x00\x00':  # lzo
            import lzo
            header = b'\xf0' + pack('>I', block_info['decompressed_size'])
            key_block = lzo.decompress(header + key_block_io.read())
        elif key_block_type == b'\x02\x00\x00\x00':  # zlib
            key_block = zlib.decompress(key_block_io.read())
        else:
            raise AttributeError('Unknown compression type')
        assert adler32_checksum == zlib.adler32(key_block) & 0xffffffff
        key_io = BytesIO(key_block)
        max_size = len(key_block)
        key_list = []
        while key_io.tell() < max_size:
            record_start = unpack(meta_format, key_io.read(meta_width))[0]
            end_offset = start_offset = key_io.tell()
            while key_io.tell() < max_size:
                if key_io.read(width) == delimiter:
                    end_offset = key_io.tell()
                    break
            key_size = end_offset - start_offset - width
            key_io.seek(start_offset)
            key_text = key_io.read(key_size).decode(encoding, errors='ignore').encode('utf-8').strip()
            key_io.seek(width, 1)
            key_list.append((record_start, key_text))
        return key_list

    @classmethod
    def build(cls):
        pass


class MDictRecordInfoBlock:
    @classmethod
    def read(cls, headers: dict, buffer: IOWrapper, block_offset: int, whence: int = 0):
        buffer = buffer.io
        buffer.seek(block_offset, whence)
        version = float(headers['GeneratedByEngineVersion'])
        meta_width = 4 if version < 2.0 else 8
        meta_format = '>I' if version < 2.0 else '>Q'
        record_block_count = unpack(meta_format, buffer.read(meta_width))[0]
        buffer.seek(meta_width, 1)
        record_info_block_size = unpack(meta_format, buffer.read(meta_width))[0]
        buffer.seek(meta_width, 1)
        assert 2 * meta_width * record_block_count == record_info_block_size
        record_block_info = []
        offset = 0
        record_offset = 0
        for i in range(record_block_count):
            compressed_size = unpack(meta_format, buffer.read(meta_width))[0]
            decompressed_size = unpack(meta_format, buffer.read(meta_width))[0]
            record_block_info.append({
                'offset': block_offset + 4 * meta_width + record_info_block_size + offset,
                'record_offset': record_offset,
                'compressed_size': compressed_size,
                'decompressed_size': decompressed_size
            })
            offset += compressed_size
            record_offset += decompressed_size
        return record_block_info

    @classmethod
    def build(cls):
        pass


class MDictRecordBlock:
    @classmethod
    def read(cls, headers: dict, info: dict, key_list: List[Tuple[int, bytes]], buffer: IOWrapper,
             file_type: str = 'mdx', block_id: int = 0):
        encoding = headers['Encoding'].lower() or 'utf-16'
        buffer = buffer.io
        buffer.seek(info['offset'], 0)
        record_block_compressed = buffer.read(info['compressed_size'])
        record_block_io = BytesIO(record_block_compressed)
        record_block_type = record_block_io.read(4)
        adler32_checksum = unpack('>I', record_block_io.read(4))[0]
        if record_block_type == b'\x00\x00\x00\x00':  # No compression
            record_block = record_block_io.read()
        elif record_block_type == b'\x01\x00\x00\x00':  # lzo
            import lzo
            header = b'\xf0' + pack('>I', info['decompressed_size'])
            record_block = lzo.decompress(header + record_block_io.read())
        elif record_block_type == b'\x02\x00\x00\x00':  # zlib
            record_block = zlib.decompress(record_block_io.read())
        else:
            raise AttributeError('Unknown compression type')
        assert adler32_checksum == zlib.adler32(record_block) & 0xffffffff
        assert len(record_block) == info['decompressed_size']
        record_io = BytesIO(record_block)
        record_count = len(key_list)
        for i in range(record_count):
            record_start, key_text = key_list[i]
            record_end = key_list[i + 1][0] if i + 1 < record_count else key_list[0][0] + info['decompressed_size']
            record_size = record_end - record_start
            assert record_size > 0
            relative_start = record_io.tell()
            record = record_io.read(record_size)
            relative_end = record_io.tell()
            if file_type == 'mdx':
                record = record.decode(encoding, errors='ignore').strip(u'\x00').encode('utf-8')
            yield key_text, record_start, record_end, relative_start, relative_end, record_size, block_id, record

    @classmethod
    def build(cls):
        pass


class MDictReader:
    def __init__(self, file_path: Union[str, Path] = None):
        self.__file_path__ = file_path if isinstance(file_path, Path) else Path(file_path)
        self.__buffer__ = IOWrapper(file_path=self.__file_path__)
        self.__headers__ = None
        self.__offsets__ = None
        self.__meta__ = None
        self.__key_info__ = None
        self.__key_list__ = None
        self.__record_info__ = None
        self.__key_lists__ = None

    @property
    def file_type(self) -> str:
        return self.__file_path__.suffix.replace('.', '').lower()

    @property
    def path(self) -> Path:
        return self.__file_path__

    @property
    def filename(self) -> str:
        return self.__file_path__.name

    def exists(self) -> bool:
        return self.__file_path__.exists()

    @property
    def headers(self) -> dict:
        if self.__headers__ is None:
            self.__headers__ = MdictHeaderBlock.read(self.__buffer__)
        return self.__headers__

    @property
    def version(self) -> str:
        return self.headers['GeneratedByEngineVersion']

    def is_old_version(self) -> bool:
        return float(self.version) < 2.0

    @property
    def __meta_width__(self) -> int:
        return 4 if self.is_old_version() else 8

    @property
    def __meta_format__(self) -> str:
        return '>I' if self.is_old_version() else '>Q'

    def __get_offsets__(self):
        with open(self.__file_path__, mode='rb') as file:
            header_block_length = unpack('>I', file.read(4))[0] + 4
            file.seek(header_block_length, 1)
            meta_block_offset = file.tell()
            file.seek(self.__meta_width__ * 2 if self.is_old_version() else self.__meta_width__ * 3, 1)
            key_info_block_size = unpack(self.__meta_format__, file.read(self.__meta_width__))[0]
            key_block_size = unpack(self.__meta_format__, file.read(self.__meta_width__))[0]
            if not self.is_old_version():
                file.seek(4, 1)
            key_info_block_offset = file.tell()
            key_blocks_offset = key_info_block_offset + key_info_block_size
            record_info_offset = key_blocks_offset + key_block_size
            file.seek(record_info_offset + 2 * self.__meta_width__)
            record_info_block_size = unpack(self.__meta_format__, file.read(self.__meta_width__))[0]
            record_blocks_offset = record_info_offset + 4 * self.__meta_width__ + record_info_block_size
            offsets = {
                'header': 0,
                'meta': meta_block_offset,
                'key_info': key_info_block_offset,
                'key_blocks':  key_blocks_offset,
                'record_info': record_info_offset,
                'record_blocks': record_blocks_offset
            }
            self.__offsets__ = offsets

    @property
    def offsets(self) -> dict:
        if self.__offsets__ is None:
            self.__get_offsets__()
        return self.__offsets__

    @property
    def meta(self) -> dict:
        if self.__meta__ is None:
            self.__meta__ = MdictKeyMetaBlock.read(
                headers=self.headers,
                buffer=self.__buffer__,
                block_offset=self.offsets['meta']
            )
        return self.__meta__

    @property
    def key_info(self) -> List[dict]:
        if self.__key_info__ is None:
            self.__key_info__ = MDictKeyInfoBlock.read(
                headers=self.headers,
                buffer=self.__buffer__,
                block_offset=self.offsets['key_info'],
                block_size=self.meta['key_info_block_size']
            )
        return self.__key_info__

    @property
    def key_list(self) -> List[Tuple[int, bytes]]:
        if self.__key_list__ is None:
            self.__key_list__ = []
            for info in self.key_info:
                self.__key_list__.extend(
                    MDictKeyBlock.read(
                        headers=self.headers,
                        block_info=info,
                        buffer=self.__buffer__
                    )
                )
        return self.__key_list__

    @property
    def keys(self) -> Generator[bytes, None, None]:
        for _, key_text in self.key_list:
            yield key_text

    @property
    def record_info(self) -> List[dict]:
        if self.__record_info__ is None:
            self.__record_info__ = MDictRecordInfoBlock.read(
                headers=self.headers,
                buffer=self.__buffer__,
                block_offset=self.offsets['record_info']
            )
        return self.__record_info__

    @property
    def key_lists(self) -> List[List[Tuple[int, bytes]]]:
        if self.__key_lists__ is None:
            self.__key_lists__ = []
            for block_id, info in enumerate(self.record_info):
                start = info['record_offset']
                end = info['record_offset'] + info['decompressed_size']
                self.__key_lists__.append(list(filter(lambda item: start <= item[0] < end, self.key_list)))
        return self.__key_lists__

    @property
    def records(self) -> Generator[Tuple[bytes, int, int, int, bytes], None, None]:
        for block_id, info in enumerate(self.record_info):
            yield from MDictRecordBlock.read(
                headers=self.headers,
                info=info,
                key_list=self.key_lists[block_id],
                buffer=self.__buffer__,
                block_id=block_id,
                file_type=self.file_type
            )


class MDictWriter:
    pass
