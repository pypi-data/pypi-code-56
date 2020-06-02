import glob
import os
import collections
from typing import Mapping, Any, List

from we_are_venom.utils.lists import flat

if False:  # TYPE_CHECKING
    from typing import DefaultDict


def should_be_skipped(filepath: str, skip_dirs: List[str]) -> bool:
    for dir_to_skip in skip_dirs:
        if dir_to_skip in filepath:
            return True
    return False


def fetch_modules_total_lines_map(path: str, config: Mapping[str, Any]) -> Mapping[str, int]:
    module_total_lines: DefaultDict[str, int] = collections.defaultdict(int)
    for module in config['modules']:
        wildcards = [
            os.path.join(path, module, '**', f'*.{e}')
            for e in config['extensions_to_check']
        ]
        filepathes = flat(glob.glob(w, recursive=True) for w in wildcards)
        for filepath in filepathes:
            if should_be_skipped(filepath, config['skip_dirs']):
                continue
            with open(filepath) as file_handler:
                num_lines = sum(1 for _ in file_handler)
            module_total_lines[module] += num_lines
    return module_total_lines
