import os
from pathlib import Path

import fire
import toml
from termcolor import colored, cprint

from datactl.utils import now_str, require_dir, require_file, show_data

CONFIG_PATH = require_file(Path.home() / '.datactl' / 'config.toml')
config = toml.load(CONFIG_PATH)


class Config():

    def __init__(self, obj):
        self._obj = obj

    def backup(self, path=None):
        '''
        Backup the configuration file
        '''
        if path:
            require_dir(path)
            backup_path = path + \
                '{}_{}.toml'.format(CONFIG_PATH.name, now_str())
        else:
            backup_path = str(CONFIG_PATH) + '.{}.toml'.format(now_str())
        with open(backup_path, 'w+') as f:
            toml.dump(config, f)
        cprint(colored('backup done to %s' % backup_path, color='green'))

    def restore(self, path):
        '''
        Restore a configuration from file
        '''
        assert Path(path).is_file(), 'The file [%s] should exists' % path
        with open(path) as rf:
            with open(CONFIG_PATH, 'w+') as f:
                f.write(rf.read())
        cprint(colored('restore is done from %s to %s' %
                       (path, CONFIG_PATH), color='green'))

    def show(self, section=False):
        '''
        Show a configuration
        '''
        if section:
            show_data(config[section], self._obj)
        else:
            with open(CONFIG_PATH, 'r') as f:
                cprint(colored(f.read(), color='green'))

    def list(self, path=None):
        '''
        List files in the configuration directory
        '''
        path = Path(path) if path else Path(CONFIG_PATH).parent
        data = []
        for f in os.listdir(path):
            full_path = Path(path) / f
            ttype = 'file' if full_path.is_file() else 'directory'
            data.append(dict(type=ttype, path=full_path))
        show_data(data, self._obj)

    def reset(self):
        '''
        Reset the configuration file
        '''
        with open(CONFIG_PATH, 'w+') as f:
            f.write('')
        cprint(colored('the configuration file is empty', color='green'))

    def set(self, section, key, value):
        '''
        Set a key and value to the section
        '''
        config.setdefault(section, {})
        config[section].update({key: value})
        with open(CONFIG_PATH, 'w+') as f:
            toml.dump(config, f)
        cprint(colored('Done !', color='green'))

    def copy(self, section, new_section):
        '''
        Copy a section to another
        '''
        config[new_section] = config[section]
        with open(CONFIG_PATH, 'w+') as f:
            toml.dump(config, f)
        cprint(colored('Done !', color='green'))

    def unset(self, section, key):
        '''
        Remove a key from a section
        '''
        config[section].pop(key)
        with open(CONFIG_PATH, 'w+') as f:
            toml.dump(config, f)
        cprint(colored('Done !', color='green'))

    def get(self, section, key=None):
        '''
        get a value from a section
        '''
        try:
            if key:
                return config[section][key]
            return config[section]
        except:
            return None

    def delete(self, section):
        '''
        Delete a section
        '''
        config.pop(section)
        with open(CONFIG_PATH, 'w+') as f:
            toml.dump(config, f)
        cprint(colored('Done !', color='green'))


def main():
    fire.Fire(Config)
