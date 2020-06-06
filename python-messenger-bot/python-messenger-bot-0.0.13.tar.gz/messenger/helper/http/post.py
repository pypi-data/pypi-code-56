import requests

class Post:
    def __init__(self, page_access_token, **kwargs):
        self.page_access_token = page_access_token
        
        return super().__init__(**kwargs)

    def send(self, url, json):
        try:
            request_session = requests.Session()

            params = {'access_token': self.page_access_token}
            request = requests.Request('POST', url = url, params = params, json = json)
            prepare = request.prepare()
        
            response = request_session.send(prepare)
        finally:
            request_session.close()
            return response.text

    def send_multipart(self, url, message, filestream):
        try:
            request_session = requests.Session()

            params = {'access_token': self.page_access_token}
            request = requests.Request('POST', url = url, params = params, data = message, files = filestream)
            prepare = request.prepare()

            print(params)
            print('\n')
            print(message)
            print('\n')
            print(filestream)

            response = request_session.send(prepare)
        finally:
            request_session.close()
            return response.text