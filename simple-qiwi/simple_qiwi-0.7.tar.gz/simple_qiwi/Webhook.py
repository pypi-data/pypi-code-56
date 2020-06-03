import time
import sys
import threading
import requests
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class Webhook:
    def __init__(self, echof):
        self.myip = requests.get('https://api.ipify.org').text
        global _echo
        _echo = echof
    
    def register(self, s :requests.Session):
        self.server = HTTPServer((self.myip, 80), Handler)
        self.r = s.request('PUT', 'https://edge.qiwi.com/payment-notifier/v1/hooks', params={
            'hookType': 1,
            'param': 'http://{0}/wq'.format(self.myip),
            'txnType': 0,
        })
        if self.r.status_code == 200:
            print('qiwi webhook ok')
        elif self.r.status_code == 422:
            print('qiwi webhook already created')
        self.cth = threading.Thread(target=self.cb_thread, daemon=True)
        self.cth.start()

    def cb_thread(self):
        self.server.serve_forever()

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "Server working!"

        self.wfile.write(bytes(message, "utf8"))
        return
    
    def do_POST(self):
        if self.path != '/wq':
            self.send_error(404)
            return
        try:
            _echo(json.loads(self.rfile.read()))
            self.send_response(200)
        except:
            self.send_error(500)
            print("Unexpected error in callback (или ты даун):", sys.exc_info()[0])
            raise