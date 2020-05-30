# This file was generated by Messi.

import asyncio
import logging
import bitstruct

from . import bunga_pb2


LOGGER = logging.getLogger(__name__)

CF_HEADER = bitstruct.compile('u8u24')


class MessageType:

    CLIENT_TO_SERVER_USER = 1
    SERVER_TO_CLIENT_USER = 2
    PING = 3
    PONG = 4


def parse_tcp_uri(uri):
    """Parse tcp://<host>:<port>.

    """

    try:
        if uri[:6] != 'tcp://':
            raise ValueError

        address, port = uri[6:].split(':')

        return address, int(port)
    except (ValueError, TypeError):
        raise ValueError(
            f"Expected URI on the form tcp://<host>:<port>, but got '{uri}'.")


class BungaClient:

    def __init__(self, uri):
        self._address, self._port = parse_tcp_uri(uri)
        self._uri = uri
        self._reader = None
        self._writer = None
        self._task = None
        self._keep_alive_task = None
        self._pong_event = None
        self._output = None

    def start(self):
        """Connect to the server. `on_connected()` is called once
        connected. Automatic reconnect if disconnected.

        """

        if self._task is None:
            self._task = asyncio.create_task(self._main())

    def stop(self):
        """Disconnect from the server. Call `start()` to connect again.

        """

        if self._task is not None:
            self._task.cancel()

    def send(self):
        """Send prepared message to the server.

        """

        encoded = self._output.SerializeToString()
        header = CF_HEADER.pack(MessageType.CLIENT_TO_SERVER_USER, len(encoded))
        self._writer.write(header + encoded)

    async def on_connected(self):
        """Called when connected to the server.

        """

    async def on_disconnected(self):
        """Called when disconnected from the server.

        """

    async def on_execute_command_rsp(self, message):
        """Called when a execute_command_rsp message is received from the server.

        """

    def init_execute_command_req(self):
        """Prepare a execute_command_req message. Call `send()` to send it.

        """

        self._output = bunga_pb2.ClientToServer()
        self._output.execute_command_req.SetInParent()

        return self._output.execute_command_req

    async def _main(self):
        while True:
            await self._connect()
            await self.on_connected()
            self._pong_event = asyncio.Event()
            self._keep_alive_task = asyncio.create_task(self._keep_alive_main())

            try:
                await self._reader_loop()
            except (Exception, asyncio.CancelledError) as e:
                LOGGER.info('Reader loop stopped by %r.', e)
                self._close()

            self._keep_alive_task.cancel()
            await self.on_disconnected()

    async def _connect(self):
        while True:
            try:
                self._reader, self._writer = await asyncio.open_connection(
                    self._address,
                    self._port)
                break
            except ConnectionRefusedError:
                LOGGER.info("Failed to connect to '%s:%d'.",
                            self._address,
                            self._port)
                await asyncio.sleep(1)

    async def _handle_user_message(self, payload):
        message = bunga_pb2.ServerToClient()
        message.ParseFromString(payload)
        choice = message.WhichOneof('messages')

        if choice == 'execute_command_rsp':
            await self.on_execute_command_rsp(message.execute_command_rsp)

    def _handle_pong(self):
        self._pong_event.set()

    async def _reader_loop(self):
        while True:
            header = await self._reader.readexactly(4)
            message_type, size = CF_HEADER.unpack(header)
            payload = await self._reader.readexactly(size)

            if message_type == MessageType.SERVER_TO_CLIENT_USER:
                await self._handle_user_message(payload)
            elif message_type == MessageType.PONG:
                self._handle_pong()

    async def _keep_alive_loop(self):
        while True:
            await asyncio.sleep(2)
            self._pong_event.clear()
            self._writer.write(CF_HEADER.pack(MessageType.PING, 0))
            await asyncio.wait_for(self._pong_event.wait(), 3)

    async def _keep_alive_main(self):
        try:
            await self._keep_alive_loop()
        except (Exception, asyncio.CancelledError) as e:
            LOGGER.info('Keep alive task stopped by %r.', e)
            self._close()

    def _close(self):
        if self._writer is not None:
            self._writer.close()
            self._writer = None
