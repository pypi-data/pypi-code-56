from .base import BaseStorage, UploadFileExists
import os
from .._utils import get_file_extension
from .._compat import urljoin
from flask import current_app, send_from_directory


class LocalStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = current_app.config.get('STORAGE_LOCAL_BASE_URL')
        self.base_path = current_app.config.get('STORAGE_LOCAL_BASE_PATH')
        
    def generate_url(self, filename):
        full_path = os.path.join(self.base_path, filename).replace('\\','/')
        return urljoin(self.base_url or 'http', full_path)


    def save(self, storage, filename=None):
        self.check(storage)
        filename = filename + '.' + get_file_extension(storage.filename) if filename else storage.filename
        ### 获取保存的目标地址        
        dest = os.path.join(self.base_path, filename)
        # 如果保存的目标路径已经存在则返回异常
        if os.path.exists(dest):
            raise UploadFileExists('File Already Exists')
        # 获取目标地址的路径
        folder = os.path.dirname(dest)
        if not os.path.exists(folder):
            # 路径不存在的时候新建路径
            os.makedirs(folder)
        storage.save(dest)
        return filename

    def read(self, filename, path=None):
        _path = path or self.base_path
        if not os.path.exists(_path):
            raise FileExistsError('Not Find %s' %dest)
        return send_from_directory(_path, filename)

    def delete(self, filename, path=None):
        dest = os.path.join(path or self.base_path, filename)
        if os.path.exists(dest):
           os.remove(dest)
        # raise FileExistsError('Not Find %s' %dest)