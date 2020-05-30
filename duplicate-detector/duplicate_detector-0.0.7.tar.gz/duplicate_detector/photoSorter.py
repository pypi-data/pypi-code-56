import json
from pathlib import Path
from tqdm import tqdm
from .photofile import PhotoFile

# TODO : Class, make prettier or things work


class PhotoSorter:
    extensions_allowed = ['JPG', 'JPEG', 'PNG', 'MP4', 'MOV']

    def __init__(self, dir_content, dest):
        self.content = dir_content
        self.dest = dest
        self.no_metadata = set()

    def tidy(self):
        for filename in tqdm(self.content):
            extension = self.get_extension(filename)
            if extension in self.extensions_allowed:
                file = PhotoFile(filename, self.content[filename], self.dest)
                self.no_metadata = file.tidy(no_metadata_set=self.no_metadata)

        with open(Path(self.dest) / "a_trier.json", "w+") as f:
            json.dump(list(self.no_metadata), f, indent=2)

        print(f"{len(self.no_metadata)} files to sort by hand are in a file, "
              f"'a_trier.json' in {self.dest}")

    @staticmethod
    def get_extension(file: str):
        if file.startswith('.'):
            return ''
        else:
            return file.split('.')[-1].upper()
