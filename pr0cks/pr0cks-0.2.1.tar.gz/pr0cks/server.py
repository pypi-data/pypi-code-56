"""
pr0cks
Copyright (C) 2020 LoveIsGrief

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import asyncore
import logging
import socket
import struct
import sys
import typing

import socks

# Python socket module does not have this constant
SO_ORIGINAL_DST = 80


class ErrorHandler:

    # pylint:disable=no-self-use,unused-variable
    def handle_error(self):
        _type, value, traceback = sys.exc_info()
        logging.error("[-] Socks5conn Error: %s : %s", _type, value, exc_info=True)


def make_socks_socket(original_socket):
    # get the original dst address and port
    odestdata = original_socket.getsockopt(socket.SOL_IP, SO_ORIGINAL_DST, 16)
    _, port, addr1, addr2, addr3, addr4 = struct.unpack("!HHBBBBxxxxxxxx", odestdata)
    address = "%d.%d.%d.%d" % (addr1, addr2, addr3, addr4)
    logging.debug(
        'Forwarding incoming connection from %s to %s through the proxy',
        original_socket.getpeername(),
        (address, port)
    )
    # connect to the socket destination over the SOCKS proxy
    socks_socket = socks.socksocket()
    # TODO Add connection timeout in CLI args
    # sock.settimeout(15)
    socks_socket.connect((address, port))
    logging.debug("Connected to %s:%s", address, port)

    return socks_socket


class SocketForwarder(ErrorHandler, asyncore.dispatcher):
    """
    Takes care of forwarding data from one socket to another.

    Since this is async reading is done in a loop or epoll.
    Data that is read will be written to the forward socket.

    In order to be able to receive a response from the forward socket
     the forward socket also needs a SocketForwarder.

    The buffer and sending logic was taken from @see{asyncore.dispatcher_with_send}
    """

    def __init__(
            self,
            backward_socket: socket.socket,
            forward_socket: typing.Union[socket.socket, "SocketForwarder"],
            chunk_size: int = 4096
    ):
        # Use this for the logger name
        #  otherwise readable and writable will return True
        #  while we're still initializing
        self.initialized = False
        super(SocketForwarder, self).__init__(backward_socket)
        self.out_buffer = b""
        self.chunk_size = chunk_size

        # Creates a forwarder for receiving data
        # It will forward data from the other socket to this one
        if not isinstance(forward_socket, SocketForwarder):
            self.other_socket = SocketForwarder(forward_socket, self)
        else:
            self.other_socket = forward_socket
            forward_socket = forward_socket.socket

        self.log = logging.getLogger("{classname}({backward}->{forward})".format(
            classname=self.__class__.__name__,
            backward=backward_socket.getpeername(),
            forward=forward_socket.getpeername(),
        ))
        self.initialized = True

    def initiate_send(self):
        num_sent = asyncore.dispatcher.send(
            self,
            self.out_buffer[:self.chunk_size]
        )
        self.out_buffer = self.out_buffer[num_sent:]

    def readable(self):
        return self.initialized

    def writable(self):
        return self.initialized and ((not self.connected) or len(self.out_buffer))

    def send(self, data: bytes):
        """
        Sends responses by the forward socket back to the client
        """
        self.log.debug('Sending %s bytes', len(data) if data else 0)
        self.out_buffer = self.out_buffer + data
        self.initiate_send()

    def handle_write(self):
        self.initiate_send()

    def handle_read(self):
        """
        Reads from backward socket and forwards it
        """
        data = self.recv(8192)
        self.log.debug("Read %s bytes", len(data))
        self.other_socket.send(data)

    def handle_close(self):
        self.log.debug("Closing connection")
        leftover_size = len(self.out_buffer)
        while leftover_size > 0:
            self.log.debug("Sending %s leftover data", leftover_size)
            self.initiate_send()
            leftover_size = len(self.out_buffer)

        self.close()


class Pr0cks5Server(ErrorHandler, asyncore.dispatcher):
    """
    The server accepting connections on a specified port.

    Accepted connections are handled in a new async channel
    """

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(20)
        self.sock = None

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            return
        sock, addr = pair  # pylint: disable=unused-variable

        # TODO is this necessary?
        self.sock = sock

        # Handle the connection asynchronously
        SocketForwarder(sock, make_socks_socket(sock))

    def handle_close(self):
        self.sock.close()
        self.close()
