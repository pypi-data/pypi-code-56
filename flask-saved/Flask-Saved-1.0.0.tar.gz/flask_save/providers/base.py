from .._compat import urljoin
from ..exception import UploadFileExists
from .._utils import get_file_extension
from werkzeug.datastructures import FileStorage
from flask import current_app
import os


class BaseStorage:
    def __init__(self, *args, **kwargs):
        self.extensions = current_app.config.get('STORAGE_COMMON_EXTENSIONS')
        self.file_max = current_app.config.get('STORAGE_COMMON_FILE_MAX')
        
    def generate_url(self, filename):
        raise NotImplementedError

    def read(self, filename):
        raise NotImplementedError

    def save(self, f, filename):
        raise NotImplementedError

    def delete(self, filename):
        raise NotImplementedError
        
    def check(self, f):
        ### 验证文件格式          
        extension = get_file_extension(f.filename )
        if extension not in self.extensions:
            raise UploadFileExists('File Extension Not Allow')

        ### 验证文件大小
        file_size = len(f.read())
        # f.read() 后文件指针在最后 会导致 f.save()保存文件为空字节，所以需要f.seek(0) 指针回到文件头
        f.seek(0)
        if file_size > self.file_max:
            raise UploadFileExists('File Size Not Allow')
        
        