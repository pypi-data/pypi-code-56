from .req_info import Request


class RequestInfoHelper:
    @staticmethod
    def read_content_safe(req :Request) -> bytes:
        l = req.get_header('content-length')
        
        if l is None:
            return b''
        
        return req.request_file.read(l)
