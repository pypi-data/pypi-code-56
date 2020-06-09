import socketserver
import struct
import threading
from multiprocessing import Process

from networking.packets import packet
from server.serverQueryManager import ServerQueryManager


class TcpHandler(socketserver.BaseRequestHandler):

    manager = ServerQueryManager()

    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024).decode('utf-8')
        query = packet.from_server_str(data)
        response = self.manager.respond(query)
        self.request.sendall(response.encode())


class TcpServer:

    def __init__(self, port):
        self.server = socketserver.ThreadingTCPServer(('', port), TcpHandler)

    def run(self):
        threading.Thread(target=self.server.serve_forever).start()




