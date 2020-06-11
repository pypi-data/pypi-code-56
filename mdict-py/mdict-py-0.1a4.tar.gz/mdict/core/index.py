from pathlib import Path
from typing import Union, List
from .mdict import MDictReader
from struct import unpack, pack
from io import BytesIO
import zlib
import dataset
import re


class MDictIndex:
    def __init__(self, mdx: Union[Path, str], db_path: Union[str, Path] = None, rebuild: bool = True):
        self.__mdx_file__ = mdx if isinstance(mdx, Path) else Path(mdx)
        self.__dict_name__ = self.__mdx_file__.name.replace('.mdx', '')
        self.__root__ = self.__mdx_file__.parent
        mdd_pattern = f"{self.__mdx_file__.name.replace('.mdx', '')}*.mdd"
        self.__mdd_files__ = list(mdd for mdd in self.__root__.glob(mdd_pattern))
        self.__others__ = list(file for file in self.__root__.glob('**/*.*[!mdd][!mdx]'))
        if db_path is None:
            self.__db_path__ = self.__root__ / f'{self.__dict_name__}.db'
        else:
            self.__db_path__ = db_path if isinstance(db_path, Path) else Path(db_path)
        if rebuild and self.__db_path__.exists():
            self.__db_path__.unlink()
        self.__db__ = dataset.connect(f'sqlite:///{self.__db_path__}')
        self.__mdx__ = MDictReader(file_path=self.__mdx_file__)
        self.__mdds__ = list(MDictReader(file_path=mdd) for mdd in self.__mdd_files__)

    @property
    def root(self) -> Path:
        return self.__root__

    @property
    def name(self) -> str:
        return self.__dict_name__

    @property
    def mdx_file(self) -> Path:
        return self.__mdx_file__

    @property
    def mdd_files(self) -> List[Path]:
        return self.__mdd_files__

    @property
    def other_files(self) -> List[Path]:
        return self.__others__

    @property
    def db(self) -> dataset.Database:
        return self.__db__

    @property
    def mdx(self) -> MDictReader:
        return self.__mdx__

    @property
    def mdds(self) -> List[MDictReader]:
        return self.__mdds__

    def __build_index_of_file__(self, file: MDictReader, case_sensitive: bool = False):
        headers = self.__db__['headers']
        headers.insert_many(
            list(
                {
                    'key': key,
                    'value': value,
                    'file_type': file.file_type,
                    'file_name': file.filename
                }
                for key, value in file.headers.items()
            )
        )
        record_blocks = self.__db__['record_blocks']
        record_blocks.insert_many(
            list(
                {
                    **info,
                    'block_id': i,
                    'file_type': file.file_type,
                    'file_name': file.filename
                }
                for i, info in enumerate(file.record_info)
            )
        )
        block_id = 0
        count = len(file.key_list)
        items = []
        record_end = file.record_info[block_id]['record_offset'] + file.record_info[block_id]['decompressed_size']
        for record_id, (record_offset, key) in enumerate(file.key_list):
            if record_offset >= record_end:
                block_id += 1
                record_end = \
                    file.record_info[block_id]['record_offset'] + \
                    file.record_info[block_id]['decompressed_size']
            relative_offset = record_offset - file.record_info[block_id]['record_offset']
            record_size = \
                file.key_list[record_id + 1][0] - record_offset \
                if record_id + 1 < count else \
                file.record_info[block_id]['decompressed_size'] - relative_offset
            items.append({
                'key': key.decode('utf-8') if case_sensitive else key.decode('utf-8').lower(),
                'record_offset': record_offset,
                'relative_offset': relative_offset,
                'record_size': record_size,
                'block_id': block_id,
                'record_id': record_id,
                'file_type': file.file_type,
                'file_name': file.filename
            })
        keys = self.__db__['keys']
        keys.insert_many(items)

    def build_index(self, case_sensitive: bool = False, verbose: bool = True):
        if verbose:
            print(f'Building index of {self.__mdx__.path}')
        self.__build_index_of_file__(self.__mdx__, case_sensitive)
        for mdd in self.__mdds__:
            if verbose:
                print(f'Building index of {mdd.path}')
            self.__build_index_of_file__(mdd, case_sensitive)


class MDictServer:
    def __init__(self, mdx: Union[Path, str], db_path: Union[str, Path] = None, base_url='/'):
        self.base_url = base_url
        self.__mdx_file__ = mdx if isinstance(mdx, Path) else Path(mdx)
        self.__dict_name__ = self.__mdx_file__.name.replace('.mdx', '')
        self.__root__ = self.__mdx_file__.parent
        mdd_pattern = f"{self.__mdx_file__.name.replace('.mdx', '')}*.mdd"
        self.__mdd_files__ = list(mdd for mdd in self.__root__.glob(mdd_pattern))
        self.__others__ = list(file for file in self.__root__.glob('**/*.*[!mdd][!mdx]'))
        if db_path is None:
            self.__db_path__ = self.__root__ / f'{self.__dict_name__}.db'
        else:
            self.__db_path__ = db_path if isinstance(db_path, Path) else Path(db_path)
        self.__db__ = dataset.connect(f'sqlite:///{self.__db_path__}')
        self.__mdx__ = MDictReader(file_path=self.__mdx_file__)
        self.__mdds__ = {
            mdd.name: MDictReader(file_path=mdd)
            for mdd in self.__mdd_files__
        }
        self.__hrefs__ = re.compile(r'href="(.+?)"')
        self.__sounds__ = re.compile(r'href="sound://(.+?)"')
        self.__entries__ = re.compile(r'href="entry://(.+?)"')

    @property
    def root(self) -> Path:
        return self.__root__

    @property
    def name(self) -> str:
        return self.__dict_name__

    @property
    def mdx_file(self) -> Path:
        return self.__mdx_file__

    @property
    def mdd_files(self) -> List[Path]:
        return self.__mdd_files__

    @property
    def other_files(self) -> List[Path]:
        return self.__others__

    @property
    def db(self) -> dataset.Database:
        return self.__db__

    @property
    def mdx(self) -> MDictReader:
        return self.__mdx__

    @property
    def mdds(self) -> dict:
        return self.__mdds__

    def link_record(self, record):
        results = []
        if '@@@LINK=' in record:
            word = record.replace('@@@LINK=', '').strip()
            records = self.fetch_contents(word)
            for record in records:
                results.extend(self.link_record(record))
        else:
            results.append(record)
        return results

    def query(self, word: str, case_sensitive: bool = False):
        if not case_sensitive:
            word = word.lower()
        records = self.fetch_contents(word)
        entries = []
        for record in records:
            entries.extend(self.link_record(record))
        html = ''.join([
            f"""<div class="mdx-entry">{
                entry
                    .replace('entry://', 'entry/')
                    .replace('sound://', '')
                    .replace('href="', f'href="{self.base_url}')
                    .replace('src="', f'src="{self.base_url}')
                    .strip()
            }</div>"""
            for entry in entries
        ])
        return html

    def fetch_file(self, path: str, case_sensitive: bool = False):
        for file in self.__others__:
            if Path(path).name in str(file) or file.name in path:
                with open(str(file), mode='rb') as reader:
                    return reader.read()
        path = path.replace('/', '\\').replace(self.base_url, '\\')
        if not path.startswith('\\'):
            path = '\\' + path
        if not case_sensitive:
            path = path.lower()
        results = []
        results.extend(self.fetch_contents(path, 'mdd'))
        if len(results) != 0:
            return results[0]

    def fetch_contents(self, key: str, file_type: str = 'mdx'):
        if file_type == 'mdx':
            encoding = self.__mdx__.headers['Encoding'].lower()
        else:
            encoding = 'utf-16'
        records = []
        for result in self.__db__['keys'].find(key=key, file_type=file_type):
            file_name = result['file_name']
            block_id = result['block_id']
            relative_offset = result['relative_offset']
            record_size = result['record_size']
            block = self.__db__['record_blocks'].find_one(block_id=block_id, file_type=file_type, file_name=file_name)
            offset = block['offset']
            compressed_size = block['compressed_size']
            decompressed_size = block['decompressed_size']
            with open(self.__root__ / file_name, mode='rb') as mdx:
                mdx.seek(offset)
                record_block_compressed = mdx.read(compressed_size)
                record_block_io = BytesIO(record_block_compressed)
                record_block_type = record_block_io.read(4)
                adler32_checksum = unpack('>I', record_block_io.read(4))[0]
                if record_block_type == b'\x00\x00\x00\x00':  # No compression
                    record_block = record_block_io.read()
                elif record_block_type == b'\x01\x00\x00\x00':  # lzo
                    import lzo
                    header = b'\xf0' + pack('>I', decompressed_size)
                    record_block = lzo.decompress(header + record_block_io.read())
                elif record_block_type == b'\x02\x00\x00\x00':  # zlib
                    record_block = zlib.decompress(record_block_io.read())
                else:
                    raise AttributeError('Unknown compression type')
                assert adler32_checksum == zlib.adler32(record_block) & 0xffffffff
                assert len(record_block) == decompressed_size
                record_io = BytesIO(record_block)
                record_io.seek(relative_offset)
                record = record_io.read(record_size)
                if file_type == 'mdx':
                    record = record.decode(encoding, errors='ignore').strip(u'\x00')
                records.append(record)
        return records
