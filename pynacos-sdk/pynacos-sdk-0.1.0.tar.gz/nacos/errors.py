
class RequestError(Exception):

    def __init__(self, message="failed to request data"):
        Exception.__init__(self, message)
