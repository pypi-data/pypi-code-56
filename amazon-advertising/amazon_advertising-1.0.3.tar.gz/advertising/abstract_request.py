from abc import ABCMeta, abstractmethod
import os
import requests
import shutil
import gzip
import io
import tempfile


class AbstractRequest(metaclass=ABCMeta):
    api = None
    method = None
    stream = False
    files = []

    @abstractmethod
    def build_args(self):
        return None


class NoArgsRequest(AbstractRequest):
    def build_args(self):
        return None


class DownloadRequest(AbstractRequest):

    dest_file = None
    unzip = False

    def download(self, resp: requests.Response):
        temp_file_name = self.dest_file
        if self.unzip == True:
            with tempfile.NamedTemporaryFile() as tmpfile:
                temp_file_name = tmpfile.name

        with open(temp_file_name, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        if self.unzip == True:
            with gzip.open(temp_file_name, 'rb') as f_in:
                with open(self.dest_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        return self.dest_file

    def build_response(self, resp: requests.Response):
        if resp.status_code == 200 and self.dest_file is not None:
            self.download(resp)
        return resp
