import requests, jsonpickle

class Client(object):
    def __init__(self, token):
        self.url = "https://db.neelr.dev/api/%s/" % token
    
    def store(self, key, data):
        r = requests.post(self.url + key, json={'data':jsonpickle.dumps(data)})
        return (r.status_code == 201), r.content.decode()
    
    def retrieve(self, key):
        r = requests.get(self.url + key)
        if r.status_code == 404:
            return None
        return jsonpickle.loads(r.json()['data'])
    
    def delete(self, key):
        r = requests.delete(self.url + key)
        return (r.status_code == 204), r.content.decode()