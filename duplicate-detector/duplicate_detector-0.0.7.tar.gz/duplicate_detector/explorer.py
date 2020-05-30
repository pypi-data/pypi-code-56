#! /usr/bin/python3.8
import time
import os
from pathlib import Path
from tqdm import tqdm


def get_path_all_files(dir_to_scan):
    file_paths = {}

    for path, _, file_list in tqdm(os.walk(dir_to_scan)):
        for filename in file_list:
            if filename.startswith('.'):
                continue
            # equivalent to os.path.join(path, filename)
            full_path = str(Path(path) / filename)

            if filename not in file_paths.keys():
                file_paths[filename] = [full_path]
            else:
                file_paths[filename].append(full_path)

    print(f"Scanning of {dir_to_scan} is done, "
          f"{len(file_paths)} unique files found")
    return file_paths


if __name__ == "__main__":
    start = time.time()
    get_path_all_files("/media/nathan/MAXTOR/photos/photos_non_triees/")
    print(f"Took {time.time() - start}s")
    # ftp_get_duplicates(SERVER_HOST, SERVER_USER, SERVER_PASSWORD, DIR)
