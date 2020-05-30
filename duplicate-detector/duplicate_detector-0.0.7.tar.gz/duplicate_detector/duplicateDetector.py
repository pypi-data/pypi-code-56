from tqdm import tqdm
from pathlib import Path


class DuplicateDetector:
    def __init__(self, files_src, files_target, dest):
        self.src = files_src
        self.target = files_target
        self.path_duplicates = Path(dest) / "DUPLICATES"
        self.path_duplicates.mkdir(exist_ok=True)

    def compare(self):
        for filename in tqdm(self.src):
            if filename in self.target:
                self.handle_duplicate(self.src[filename])

    def handle_duplicate(self, paths):
        """Moves a list of file in the DUPLICATE folder

        Arguments:
            paths {list of str} -- [list of paths]
        """
        for p in paths:
            old = Path(p)
            filename = old.name
            old.replace(self.path_duplicates / filename)
        # [Path(p).replace(target=self.path_duplicates) for p in paths]
