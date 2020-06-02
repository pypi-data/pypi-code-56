import configparser
import os
from typing import Any, Optional, Mapping


def load_config_from(config_path: str, config_section_name: str = 'venom') -> Optional[Mapping[str, Any]]:
    parser = configparser.ConfigParser()
    parser.read(config_path)
    user_config = dict(parser[config_section_name]) if parser.has_section(config_section_name) else {}
    if 'modules' not in user_config:
        return None
    modules = []
    for raw_module in user_config['modules'].split('\n'):
        module = raw_module.strip()
        if not module:
            continue
        if not module.endswith(os.sep):
            module = f'{module}{os.sep}'
        modules.append(module)

    config = {
        'history_depth_years': (
            int(user_config['history_depth_years'])
            if user_config.get('history_depth_years')
            else 1 / 12
        ),
        'min_lines_in_module': (
            int(user_config['min_lines_in_module'])
            if user_config.get('min_lines_in_module')
            else 20
        ),
        'skip_dirs': ['/migrations/'],
        'extensions_to_check': ['py', 'html', 'css', 'md', 'cfg', 'js', 'ts'],
        'min_touched_lines_for_accumulated_module': (
            int(user_config['min_touched_lines_for_accumulated_module'])
            if user_config.get('min_touched_lines_for_accumulated_module')
            else 50
        ),
    }
    config['modules'] = modules
    return config
