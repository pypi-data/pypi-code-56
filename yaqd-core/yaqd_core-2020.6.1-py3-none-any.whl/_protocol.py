import asyncio

from .exceptions import InvalidRequest, MethodNotFound
from . import msgpack


class Protocol(asyncio.Protocol):
    def __init__(self, daemon, *args, **kwargs):
        self._daemon = daemon
        self.logger = daemon.logger
        self._method_list = self._daemon.list_methods()
        asyncio.Protocol.__init__(self, *args, **kwargs)
        self._error_codes = {
            msgpack.exceptions.UnpackException: {
                "code": -32700,
                "message": "Parse error",
            },
            InvalidRequest: {"code": -32600, "message": "Invalid Request"},
            MethodNotFound: {"code": -32601, "message": "Method not found"},
            TypeError: {"code": -32602, "message": "Invalid params"},
        }

    def connection_lost(self, exc):
        peername = self.transport.get_extra_info("peername")
        self.logger.info(f"Connection lost from {peername} to {self._daemon.name}")
        self._daemon._connection_lost(peername)

    def connection_made(self, transport):
        """Process an incomming connection."""
        peername = transport.get_extra_info("peername")
        self.logger.info(f"Connection made from {peername} to {self._daemon.name}")
        self.transport = transport
        self._daemon._connection_made(peername)

    def data_received(self, data):
        """Process an incomming request."""
        self.logger.info(f"Data received: {repr(data)}")
        if not self._daemon._server.is_serving():
            self.transport.close()
        unpacker = msgpack.Unpacker()
        unpacker.feed(data)
        try:
            for o in unpacker:
                self.run_method(o)
        except (msgpack.exceptions.UnpackException, ValueError):
            # Handle invalid msgpack
            response = {
                "ver": "1.0",
                "error": self._error_codes[msgpack.exceptions.UnpackException],
                "id": None,
            }
            self.transport.write(msgpack.packb(response))

    def run_method(self, request):
        response = {"ver": "1.0"}
        # Ignoring "ver" in request
        notification = False
        shutdown = False
        try:
            if not isinstance(request, dict) or "method" not in request:
                request = {}
                raise InvalidRequest
            shutdown = request.get("method") == "shutdown"
            notification = "id" not in request

            method = request["method"]
            response["id"] = request.get("id")
            params = request.get("params", [])

            if not isinstance(method, str):
                notification = False
                raise InvalidRequest
            if method not in self._method_list:
                raise MethodNotFound(method)
            fun = getattr(self._daemon, method)
            if isinstance(params, list):
                response["result"] = fun(*params)
            else:
                response["result"] = fun(**params)
        except BaseException as e:
            self.logger.error(
                f"Caught exception in {request.get('method', 'RPC')}: {repr(e)}"
            )
            if type(e) in self._error_codes:
                response["error"] = self._error_codes[type(e)]
            else:
                response["error"] = {"code": -1, "message": repr(e)}
        if "error" in response:
            response.pop("result", None)
            try:
                response["id"] = request.get("id", None)
            except:
                response["id"] = None
        # Notifications get no response
        if response and not notification:
            self.transport.write(msgpack.packb(response))
        if shutdown:
            self.transport.close()
