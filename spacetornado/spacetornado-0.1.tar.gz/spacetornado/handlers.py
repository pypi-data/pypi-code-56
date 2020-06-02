import json
import tornado.web
from .operations import *

content_type = "Content-Type", "application/json"


class Tokens(tornado.web.RequestHandler):
    def post(self):
        self.set_header(content_type[0], content_type[1])
        self.write(json.dumps(tokens(self.get_body_argument("text")), indent=4))


class NounChunks(tornado.web.RequestHandler):
    def post(self):
        self.set_header(content_type[0], content_type[1])
        self.write(json.dumps(noun_chunks(self.get_body_argument("text")), indent=4))


class Entities(tornado.web.RequestHandler):
    def post(self):
        self.set_header(content_type[0], content_type[1])
        self.write(json.dumps(entities(self.get_body_argument("text")), indent=4))


class Similarity(tornado.web.RequestHandler):
    def get(self):
        self.set_header(content_type[0], content_type[1])
        self.write(json.dumps(similarity(self.get_query_argument("left"), self.get_query_argument("right")), indent=4))

    def post(self):
        self.set_header(content_type[0], content_type[1])
        self.write(json.dumps(similarity(self.get_body_argument("left"), self.get_body_argument("right")), indent=4))
