#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple Python Mock HTTP Server
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# NOTE: as this resource needs to be shared by all requests,
# they need to run in the same process
_RESPONSES = {}
_RECORDED_REQUESTS = []


class Handler(BaseHTTPRequestHandler):
    def _handle_record_request(self, method):
        parsed_path = urlparse(self.path)
        _RESPONSES[(method, parsed_path.path)] = {
            # TODO: add support for specifying headers, errors, and more
            "body": self._read_body(),
            "status": int(self.headers.get("MOCK_STATUS", 200)),
        }
        self.send_response(200)
        self.end_headers()
        self.wfile.write("{} mock recorded\n".format(method).encode("ascii"))

    def _read_body(self):
        """Read the request body, as if it were a POST request"""
        content_len = int(self.headers.get("content-length", 0))
        return self.rfile.read(content_len)

    def do_MOCK_GET(self):
        self._handle_record_request("GET")

    def do_MOCK_POST(self):
        self._handle_record_request("POST")

    def do_MOCK_PUT(self):
        self._handle_record_request("PUT")

    def do_MOCK_DELETE(self):
        self._handle_record_request("DELETE")

    def do_MOCK_PATCH(self):
        self._handle_record_request("PATCH")

    def do_MOCK_RESET(self):
        _RESPONSES.clear()
        _RECORDED_REQUESTS.clear()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Mock resetted")

    def do_MOCK_RETRIEVE(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response_body = json.dumps(_RECORDED_REQUESTS).encode("utf-8")
        self.wfile.write(response_body)

    def _serialize_request(self):
        parsed_path = urlparse(self.path)
        return {
            "path": parsed_path.path,
            "query": parsed_path.query,
            "method": self.command,
            "body": self._read_body().decode("utf-8"),
            "headers": dict(self.headers),
        }

    def _play_response(self):
        parsed_path = urlparse(self.path)
        try:
            to_send = _RESPONSES[(self.command, parsed_path.path)]
            # TODO: consider decoding body according to request's declared encoding
            _RECORDED_REQUESTS.append(self._serialize_request())
        except KeyError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(
                b"Mock server got unexpected request:\n"
                + json.dumps(self._serialize_request(), indent=2).encode("utf-8")
            )
        else:
            self.send_response(to_send["status"])
            self.end_headers()
            self.wfile.write(to_send["body"])

    def do_GET(self):
        self._play_response()

    def do_POST(self):
        self._play_response()

    def do_PUT(self):
        self._play_response()

    def do_DELETE(self):
        self._play_response()

    def do_PATCH(self):
        self._play_response()


def start_server(host, port):
    server = HTTPServer((host, port), Handler)
    print(
        "Starting mock server on http://{}:{}, use <Ctrl-C> to stop".format(
            host, port
        )
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()


def main(args):
    start_server(args.host, args.port)


if "__main__" == __name__:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=7777)

    args = parser.parse_args()
    main(args)
