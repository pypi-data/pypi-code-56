import json
from colorama import init, Fore

init(autoreset=True)


class HPassCli:
    def __init__(self, primary, hello_password_data_dir):
        self.primary = primary
        self.hello_password_data_dir = hello_password_data_dir
        with open(hello_password_data_dir, 'r', encoding='utf-8') as f:
            password_data_json = json.load(f)
        self.password_data_json = password_data_json

    def get_password_list(self):
        return self.password_data_json


def cli_start(primary, hello_password_data_dir):
    h_pass_cli = HPassCli(primary=primary, hello_password_data_dir=hello_password_data_dir)
    while True:
        user_input = input('H-Pass> ')
        if user_input == 'exit' or user_input == 'quit':
            break
