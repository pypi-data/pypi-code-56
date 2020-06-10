from ..driver import GenericFileDriver
from ..handler_enums import FILE_HANDLER_TYPE


class NullFileDriver(GenericFileDriver):

    def get_type(self):
        return FILE_HANDLER_TYPE.NULL

    def get_files(self, folder_name, extension):
        return ['NullFileDriver']

    def get_physical_file(self, file_name):
        return {
            'NullFileDriver': NullFileDriver
        }

    def store_files(self, folder_name, files, overwrite=False):
        pass

    def store_file(self, folder_name, file, overwrite=False):
        pass
