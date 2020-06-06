from http.server import BaseHTTPRequestHandler, HTTPServer
import json,base64
from io import BytesIO

class alexa(BaseHTTPRequestHandler):

    launch_message = "Launched"
    intent_function = intent_function = lambda : None
    session_start_function=lambda : None
    session_end_function=lambda : None
    help_function=lambda : None
    intent_name = None
    reply_message = None
    auth_code = None

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Server up')

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        self.data = json.loads(self.rfile.read(length))
        self.request_handler()
        self.reply()

    def request_handler(self):
        if self.data["session"]["new"]:
            self.launch_request()
        if self.data["request"]["type"] == "LaunchRequest":
            self.launch_request()
        elif self.data["request"]["type"] == "IntentRequest":
            self.intent_handler()
        elif self.data["request"]["type"] == "SessionEndedRequest":
            self.session_ended()

    def launch_request(self):
        alexa.session_start_function()
        alexa.reply_message = self.build_speech_response(self.launch_message)

    def session_ended(self):
        alexa.session_end_function()
        alexa.reply_message = self.build_speech_response("closed",session_end = True)

    def get_help (self):
        alexa.help_function()
        alexa.reply_message = self.build_speech_response("Sent Help")

    def intent_handler(self):
        try:
             alexa.auth_code = self.data["user"]["accessToken"]
        alexa.intent_name = self.data["request"]["intent"]["name"]
        try:
            alexa.intent_function()
            if alexa.intent_name == "AMAZON.HelpIntent":
                self.get_help()
            elif alexa.intent_name == "AMAZON.CancelIntent" or alexa.intent_name == "AMAZON.StopIntent":
                self.session_ended()
        except:
            alexa.reply_message = self.build_speech_response("Invalid Intent")

    def reply(self):
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(json.dumps(alexa.reply_message).encode())
        self.wfile.write(response.getvalue())

    def intent_name(self):
        return self.data["request"]["intent"]["name"]

    def access_token(self):


    @staticmethod
    def build_speech_response(msg,session_end = False):
        return {"response": {"outputSpeech": {"text": msg , "type": "PlainText"}, "shouldEndSession": session_end}, "sessionAttributes": {}, "version": "1.0"}