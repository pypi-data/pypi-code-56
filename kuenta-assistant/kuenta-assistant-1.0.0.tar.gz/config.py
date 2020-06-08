import configparser
import os
import click


envs = {
    "test": "https://test-api.kuenta.co"
}

class Config:
    def __init__(self, env: str, file = None):
        self.file = file or os.path.join(os.getenv("HOME"), ".kuenta.ini")
        self.env = env
        self.parser = configparser.ConfigParser()
        self.parser.read(self.file)
        self.base_url = envs[env]
        

    @property
    def section(self):
        if not self.parser.has_section(self.base_url):
            self.parser[self.base_url] = {}
        return self.parser[self.base_url]
    
    def get(self, option: str):
        return self.section.get(option)
    
    def set(self, option: str, value: str):
        self.section[option] = value

    def save(self):
        with open(self.file, "w") as file:
            self.parser.write(file)
    