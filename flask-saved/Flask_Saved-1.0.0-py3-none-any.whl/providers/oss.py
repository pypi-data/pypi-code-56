from .base import BaseStorage
from .._compat import urljoin
from .._utils import get_file_extension
from itertools import islice
from math import ceil
from flask import current_app
from werkzeug.utils import cached_property
import oss2
import os
  

class OssStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._access_key = current_app.config.get('STORAGE_OSS_ACCESS_KEY')
        self._secret_key = current_app.config.get('STORAGE_OSS_SECRET_KEY')
        self._endpoint = current_app.config.get('STORAGE_OSS_ENDPOINT')
        self._bucket = current_app.config.get('STORAGE_OSS_BUCKET')
        self._cname = current_app.config.get('STORAGE_OSS_CNAME')
        self._domain = current_app.config.get('STORAGE_OSS_DOMIAN')
        self.base_path = current_app.config.get('STORAGE_OSS_BASE_PATH')
 
    @cached_property
    def auth(self):
        return oss2.Auth(self._access_key, self._secret_key)

    @cached_property
    def bucket(self):
        return oss2.Bucket(self.auth, self._endpoint, self._bucket)
    
    def _generate_full_filename(self, storage, filename=None):
        filename = filename + '.' + get_file_extension(storage.filename) if filename else storage.filename
        return os.path.join(self.base_path, filename).replace('\\','/')
    
    def save(self, storage, filename=None):
        self.check(storage)
        dest = self._generate_full_filename(storage , filename)
        result = self.bucket.put_object(dest, storage)
        if result.status == 200:
            return dest
        else:
            abort(500)
            
    def read(self, filename):
        pass
    
    def delete(self, filename):
        info = self.bucket.delete_object(filename)
        if info.status == 204:
            return True
        else:
            abort(500)
    
    def generate_url(self, filename):
        if self._domain:
            return urljoin(self._domain, filename)
        else:
            return urljoin(self.host, filename)
    
    @cached_property
    def host(self):
        return '{schema}://{bucket}.{endpoint}'.format(
            schema='https', 
            bucket=self._bucket,
            endpoint=self._endpoint
        )