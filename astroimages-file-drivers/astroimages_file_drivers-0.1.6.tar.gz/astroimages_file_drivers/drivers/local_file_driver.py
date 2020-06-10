from ..driver import GenericFileDriver
from ..handler_enums import FILE_HANDLER_TYPE
from ..util.local_file_system import list_files_in_folder, read_full_file_in_bytes, store_file


class LocalFileDriver(GenericFileDriver):

    def get_type(self):
        return FILE_HANDLER_TYPE.LOCAL

    def get_files(self, folder_name, extension):
        return list_files_in_folder(folder_name, extension)

    def get_physical_file(self, file_name):
        return read_full_file_in_bytes(file_name)

    def store_files(self, folder_name, files, overwrite=False):
        for file in files:
            # print('FILE = %s' % '{}/{}'.format(folder_name, file['name']))
            self.store_file('{}/{}'.format(folder_name, file['name']), file['contents'], overwrite)

    def store_file(self, path, file, overwrite=False):
        return store_file(path, file, overwrite)
