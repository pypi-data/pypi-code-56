# coding="utf-8"
import requests
import json
import config

class wechatntf():
    def __init__(self):
        self.url = "http://wxpusher.zjiecode.com/api/send/message"
        self.headers = {
            "Content-Type": "application/json"
        }

    def wechatsend(self, summary="", content=""):
        self.data = {
            "summary": summary,
            "content": content,
            "contentType": 1
        }
        self.data["appToken"] = config.appToken
        self.data["topicIds"] = config.topicIds
        # self.data["uids"] = config.uids
        self.data = json.dumps(self.data)
        return requests.post(url=self.url, headers=self.headers, data=self.data).content.decode()

if __name__ == '__main__':
    a = wechatntf()
    res = a.wechatsend(content="找不到满意的版本，这然后继续然后继续尝试发现还是不行")
    print(res)
