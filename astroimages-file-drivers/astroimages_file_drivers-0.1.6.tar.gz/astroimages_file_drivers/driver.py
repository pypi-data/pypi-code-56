from abc import ABC, abstractmethod


class GenericFileDriver(ABC):

    @abstractmethod
    def get_physical_file(self, file_name):
        pass

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def get_files(self, folder_name, extension):
        pass

    @abstractmethod
    def store_files(self, folder_name, files, overwrite=False):
        """ files must be a dictionary array with the following structure:

            array_files = [
                {'name': 'file1.txt', 'contents': 'CONTENTS FILE 1'},
                {'name': 'file2.txt', 'contents': 'CONTENTS FILE 2'},
            ]

        """
        pass

    @abstractmethod
    def store_file(self, folder_name, file, overwrite=False):
        pass

    def get_file(self, file_name):
        return self.get_physical_file(file_name)
