from datetime import datetime
from pathlib import Path

import PIL.ExifTags
from PIL import Image


class PhotoFile:
    number_to_month = {
        1: "01-janv",
        2: "02-fev",
        3: "03-mars",
        4: "04-avr",
        5: "05-mai",
        6: "06-juin",
        7: "07-juil",
        8: "08-aout",
        9: "09-sept.",
        10: "10-oct",
        11: "11-nov",
        12: "12-dec",

    }

    def __init__(self, filename, list_path, root_dest):
        self.filename = filename
        self.list_path = self.sort_path(list_path)
        self.root_dest = root_dest

    def tidy(self, no_metadata_set=None):
        self.handle_first_path(no_metadata_set)
        self.handle_other_paths()
        return no_metadata_set

    def handle_first_path(self, no_metadata_set):
        path = self.list_path[0]
        date = self.get_date_creation_pil(path)
        if date:
            new_path = self.create_path_from_date(date)
            self.move_to_path(Path(path), new_path)
        else:
            if no_metadata_set is not None:
                no_metadata_set.add(path)
        return no_metadata_set

    def handle_other_paths(self):
        for path in self.list_path[1:]:
            new_path = Path(self.root_dest) / "doublons" / self.filename
            self.move_to_path(Path(path), new_path)

    def create_path_from_date(self, date):
        return (Path(self.root_dest) / str(date.year) /
                self.number_to_month[date.month] / self.filename)

    @staticmethod
    def get_date_creation_pil(path):
        img = Image.open(path)
        exif_raw = img._getexif()
        if not exif_raw:
            return None
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in exif_raw.items()
            if k in PIL.ExifTags.TAGS
        }
        date_str = exif.get("DateTimeOriginal")
        if not date_str:
            return None
        try:
            date = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
            return date
        except ValueError as v_e:
            print(v_e)
            return None

    @staticmethod
    def sort_path(list_paths):
        """Select a picture among duplicates, based on size of the file.

        Arguments:
            list_paths {list} -- list of paths.

        Returns:
            str -- path selected
        """
        if len(list_paths) == 1:
            return list_paths
        else:
            # 2 or more paths.
            info_list = [(path, Path(path).stat().st_size)
                         for path in list_paths]
            info_list.sort(key=lambda tup_info: tup_info[1], reverse=True)
            # return file from heaviest to lightest
            return [tup_path[0] for tup_path in info_list]

    @staticmethod
    def move_to_path(old_path, new_path):
        # print(old_path, new_path)
        new_path.parent.mkdir(parents=True, exist_ok=True)
        old_path.replace(new_path)
        pass
