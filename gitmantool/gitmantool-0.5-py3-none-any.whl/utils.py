import yaml
import os
import sys

from colorama import Fore, Style


# ─── SETTINGS CLASS ─────────────────────────────────────────────────────────────

class SettingsFile:

    NAME = "settings.gm"

    def create(self):
        print("Settings file not exist, creating...")
        link = input("Input link of git server: ")
        with open(self.NAME, 'w') as f:
            yaml.dump({"link": link}, f, default_flow_style=False)

    @property
    def link(self):
        try:
            with open(self.NAME, "r") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(f"error: {e}")
            sys.exit()
        else:
            return data['link']

    @property
    def exist(self):
        return os.path.isfile(self.NAME)

    @property
    def server(self):
        return self.link.split("/")[2]

    @property
    def username(self):
        return self.link.split("/")[3]

    @property
    def repo(self):
        return self.link.split("/")[4]


# ────────────────────────────────────────────────────────────────────────────────


# ─── CREDENTIALS MANAGER ────────────────────────────────────────────────────────

# Clase encargada de gestionar el fichero de credenciales
class CredsManager:

    CREDS_FOLDER = os.environ["HOME"] + "/.gitmanager"
    CREDS_FILE = "creds.yaml"

    def __init__(self):
        self.CREDS_PATH = f"{self.CREDS_FOLDER}/{self.CREDS_FILE}"
        if not self.exist:
            self._generate_basic_file()

    def _generate_basic_file(self):
        try:
            print(" [i] Creating credentials file...")
            os.system(f"mkdir -p {self.CREDS_FOLDER}")
            os.system(f"touch {self.CREDS_PATH}")
        except Exception as e:
            print(e)
            sys.exit(" [!] Can't create the credentials file")
        else:
            print("\n [i] Adding servers...")
            tokens = {
                "github": self.input_token("github"),
                "gitlab": self.input_token("gitlab")
            }
            with open(self.CREDS_PATH, 'w') as f:
                yaml.dump(tokens, f, default_flow_style=False)

    @property
    def exist(self):
        return os.path.isfile(self.CREDS_PATH)

    def get_token(self, server):
        with open(self.CREDS_PATH, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if data[server] is None:
                print(" [!] Please add token on config file:")
                print(f"\t{self.CREDS_PATH}")
                sys.exit()
            return data[server]

    def input_token(self, server):
        token = input(f"   Input token for {server.title()}: ")
        if len(token) == 0:
            return None
        return token

# ────────────────────────────────────────────────────────────────────────────────


# return current version
def get_version():
    try:
        with open('gitmanager/version.yaml', "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        print(e)
    else:
        return data['version']


def print_header():
    print(f"{Fore.GREEN}{Style.DIM}# Git Manager Tool (v{get_version()})\n\n")


def salir(mensaje=None):
    if mensaje is not None:
        print(f"{Fore.RED}[X]{Fore.RESET} {mensaje}\n")
    sys.exit("Exiting...")


def info(mensaje):
    print(f"{Fore.BLUE}[i]{Fore.RESET} {mensaje}")


def error(mensaje):
    print(f" {Fore.RED}[i]{Fore.RESET} {mensaje}")
