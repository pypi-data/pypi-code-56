from cmnSys import directoryFinder
from cmnUtils.configManager import user_config_interface
from networking.tcpServer import TcpServer
from server.adjacencyMatrix import AdjacencyMatrix
from server.serverConfig import ServerConfig


def main(args):
    # get settings
    settings = ServerConfig(directoryFinder.server_config_file())
    # get adjacency file up to date
    if not directoryFinder.server_adjacency_file().is_file():
        get_adjmat().write_to_csv(directoryFinder.server_adjacency_file())
    else:
        if input("Would you like to update or change your adjacency file (y/n):") == 'y':
            get_adjmat().write_to_csv(directoryFinder.server_adjacency_file())

    user_config_interface(settings)


    # runs server in another thread
    TcpServer(settings['port']).run()


def get_adjmat() -> AdjacencyMatrix:
    csv = input("Please provide a path to your adjacency file here: ")
    while True:
        try:
            adj = AdjacencyMatrix(csv, False)
            print(adj)
            break
        except FileNotFoundError:
            csv = input("The file provided could not be opened. Please try again:")
    return adj
