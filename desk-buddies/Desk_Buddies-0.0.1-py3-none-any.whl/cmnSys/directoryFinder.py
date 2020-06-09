from pathlib import Path

from appdirs import AppDirs

appdirs = AppDirs('DeskBuddies', 'Murphy & Gu')


def client_config_file():
    return appdirs.user_config_dir / Path("ClientConfig.txt")


def server_config_file():
    return appdirs.user_config_dir / Path("ServerConfig.txt")


def server_schedule_dir():
    return appdirs.user_data_dir / Path("ServerSchedule")


def server_adjacency_file():
    return appdirs.user_data_dir / Path("ServerAdjacencyMatrix.csv")
