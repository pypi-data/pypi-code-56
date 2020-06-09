import socket


# sends a packet and waits for a response
# this means the server has to respond with something, so we will make a null packet for this reason
import struct

from networking.packets import packet
from networking.packets.packet import Packet


def send_packet(pack: Packet, host, port) -> Packet:
    print(pack.encode().decode('utf-8'))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(pack.encode())
    # receive and reconstruct a possibly large message
    data = recv_msg(s).decode('utf-8')
    pack = packet.from_str(data)
    return pack


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
