import configparser
import os
import sys
import copy
import socket


class Config:

    def __init__(self):
        config = None
        conf_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'conf')
        conf_base_dir = os.path.join(conf_dir, 'base')
        for name in os.listdir(conf_base_dir):
            if name.startswith('.'):
                continue
            conf_file = os.path.join(conf_base_dir, name)
            config = self._update_config(config, self._read_config(conf_file))
        host_conf_file = os.path.join(os.path.join(conf_dir, 'host'), socket.gethostname() + '.cfg')
        if os.path.exists(host_conf_file) and os.path.isfile(host_conf_file):
            config = self._update_config(config, self._read_config(host_conf_file))
        self.cfg = config
        self.update_from_env()
        self.update_values()

    def __getitem__(self, item):
        return self.cfg.__getitem__(item)

    def print_confing(self, func_name=None):
        if func_name is None:
            func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        print(f'{func_name}: config: {self.cfg}')

    @staticmethod
    def _read_config(path):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(path)
        return {section: dict(config.items(section)) for section in config.sections()}

    @staticmethod
    def _update_config(config, ext_config):
        if config:
            for key in ext_config:
                if key in config:
                    config[key].update(ext_config[key])
                else:
                    config[key] = ext_config[key]
            return config
        else:
            return ext_config

    def update_from_env(self):
        new_cfg = copy.deepcopy(self.cfg)
        for section_name in self.cfg:
            for key in self.cfg[section_name]:
                env_key = f'{section_name.upper()}_{key.upper()}'
                if env_key in os.environ:
                    new_cfg[section_name][key] = os.environ[env_key]
        self.cfg = new_cfg

    def update_values(self):
        new_cfg = copy.deepcopy(self.cfg)
        for section_name in self.cfg:
            for k, v in self.cfg[section_name].items():
                if isinstance(v, str):
                    if v.strip() == '' or v.strip().lower() == 'none' or v.strip().lower() == '<none>':
                        new_cfg[section_name][k] = None
                    elif v.strip().lower() == 'true':
                        new_cfg[section_name][k] = True
                    elif v.strip().lower() == 'false':
                        new_cfg[section_name][k] = False
        self.cfg = new_cfg


cfg = Config()
