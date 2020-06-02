import collections
from typing import List, Mapping, Any, Optional, Iterable, Tuple

from git import Commit
from unidiff import PatchSet

from we_are_venom.common_types import ModuleAccumulation
from we_are_venom.utils.files import fetch_modules_total_lines_map, should_be_skipped

if False:  # TYPE_CHECKING
    from typing import DefaultDict


def _get_file_module(filename: str, modules: List[str]) -> Optional[str]:
    for module in modules:
        if filename.startswith(module):
            return module
    return None


def is_module_accumulated(
    touched_lines: Optional[int],
    total_lines: Optional[int],
    config: Mapping[str, Any],
) -> Optional[bool]:
    if not total_lines or total_lines < config['min_lines_in_module']:
        return None
    return bool(touched_lines and touched_lines >= config['min_touched_lines_for_accumulated_module'])


def get_touched_files_in_commit(
    commit: Commit,
    config: Mapping[str, Any],
) -> Iterable[Tuple[str, int]]:
    touched_lines_per_module: DefaultDict[str, int] = collections.defaultdict(int)
    raw_diff = commit.repo.git.diff(commit.tree, commit.parents[0] if commit.parents else None)
    for changed_file in PatchSet(raw_diff):
        filename = changed_file.path
        if should_be_skipped(filename, config['skip_dirs']):
            continue
        module = _get_file_module(filename, config['modules'])
        if not module:
            continue
        touched_lines_per_module[module] += changed_file.added + changed_file.removed
    return touched_lines_per_module.items()


def calclulate_module_accumulation_info(
    raw_git_history: List[Commit],
    email: str,
    config: Mapping[str, Any],
) -> List[ModuleAccumulation]:
    touched_lines_per_module: DefaultDict[str, int] = collections.defaultdict(int)
    for commit in raw_git_history:
        for module, new_touched_lines in get_touched_files_in_commit(commit, config):
            touched_lines_per_module[module] += new_touched_lines
    modules_total_lines_map = fetch_modules_total_lines_map(
        raw_git_history[0].repo.working_dir,
        config,
    )
    accumulated_modules_info = [
        ModuleAccumulation(
            module_name=m,
            touched_lines=l,
            total_lines=modules_total_lines_map.get(m),
            is_accumulated=is_module_accumulated(
                l,
                modules_total_lines_map.get(m),
                config,
            ),
        )
        for (m, l) in touched_lines_per_module.items()
    ]
    empty_modules_info = [
        ModuleAccumulation(
            module_name=m,
            touched_lines=0,
            total_lines=modules_total_lines_map.get(m),
            is_accumulated=is_module_accumulated(
                None,
                modules_total_lines_map.get(m),
                config,
            ),
        )
        for m in config['modules']
    ]
    return accumulated_modules_info + empty_modules_info


def calculate_total_accumulation_percent(module_accumulation_info: List[ModuleAccumulation]) -> int:
    accumulated_modules_number = len([m for m in module_accumulation_info if m.is_accumulated])
    scored_modules_number = len([m for m in module_accumulation_info if m.is_accumulated is not None])
    return int(accumulated_modules_number / scored_modules_number * 100)
