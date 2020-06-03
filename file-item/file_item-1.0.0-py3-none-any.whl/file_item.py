from typing import Optional, Union
from pathlib import Path, PosixPath
import os


class File:
    """
    File object
    """

    def __init__(self, path: Union[str, PosixPath]) -> None:
        """
        :param str path: file's absolute path
        """
        if isinstance(path, str):
            self.path = Path(path)
        elif isinstance(path, PosixPath):
            self.path = path
        else:
            raise ValueError(f'The path variable should be str or PosixPath, not {type(path)}')

    @property
    def name(self) -> str:
        """File name"""
        return Path(self.path).name

    def __repr__(self):
        return f'File(path="{self.path}")'

    def __str__(self):
        return str(self.path)

    def __eq__(self, other: Union['File', PosixPath, str]):
        if isinstance(other, self.__class__):
            return self.path == other.path
        elif isinstance(other, PosixPath):
            return self.path == other
        elif isinstance(other, str):
            return str(self) == other
        return False

    def create_folder(self) -> None:
        """
        Create folder by file path if not exist

        :return None:

        Example:
            >>> f = File('/home/user/test.csv')
            >>> f.create_folder()
        """
        if not os.path.exists(str(self)):
            os.makedirs(str(self))

    @staticmethod
    def basedir(file_: str) -> PosixPath:
        """
        Return file's basedir

        :param str file_: path to a file
        :return PosixPath: path to the file's folder

        Example:
            >>> from file_item import File
            >>> basedir = File.basedir(__file__)
        """
        return Path(file_).parent

    @staticmethod
    def get_file_name(name: str, ext: Optional[str] = None, replacer: str = '-') -> str:
        """
        Will replace forbidden characters from the string

        Forbidden symbols: 
        
            - < (less than)
            - > (greater than)
            - : (colon)
            - " (double quote)
            - / (forward slash)
            - \ (backslash)
            - | (vertical bar or pipe)
            - ? (question mark)
            - * (asterisk)

        Examples:
            >>> File.get_file_name('test*.csv')
            ... 'test-.csv'
            >>> File.get_file_name('test*', ext='csv')
            ... 'test-.csv'
            >>> File.get_file_name('test*.csv', replacer='_')
            ... 'test_.csv'

        :param str name: file's name
        :param str ext: file's extension, default None
        :param str replacer: replacer for forbidden characters, default: -
        :return str: file name
        """
        forbidden = ('<', '>', ':', '"', '/', '\\', '|', '?', '*')
        if replacer in forbidden:
            raise ValueError(f'replacer can\'t be in {forbidden}')
        translator = {k: replacer for k in forbidden}
        file_name = name.translate(str.maketrans(translator))
        if ext is not None:
            file_name = f'{file_name}.{ext}'
        return file_name

    @classmethod
    def from_strings(cls, folder_path: str, file_name: str) -> 'File':
        """
        Create a File object from strings

        :param str folder_path: path to a folder
        :param str file_name: file name
        :return File:

        Example:
            >>> file_ = File.from_strings('/home/user/folder', 'test.csv')
        """
        return cls(os.path.join(folder_path, file_name))
