import requests
import datetime


class sbkTools():

    def chunks(self, l, n, total_list=[]):
        """将大列表切片为指定长度小列表"""
        for i in range(0, len(l), n):
            total_list.append(l[i:i + n])
        return total_list

    def traverse_take_field(self, data, fields, values=[], currentKey=None):
        """
        遍历嵌套字典列表，取出某些字段的值
        :param data: 嵌套字典列表
        :param fields: 列表，某些字段
        :param values: 返回的值
        :param currentKey: 当前的键值
        :return:
        """
        if isinstance(data, list):
            for i in data:
                self.traverse_take_field(i, fields, values, currentKey)
        elif isinstance(data, dict):
            for key, value in data.items():
                self.traverse_take_field(value, fields, values, key)
        else:
            if currentKey in fields:
                values.append(data)
        return values

    def traverse_dict_field(self, data, fields, values={}, currentKey=None):
        """
            取大字典中指定字段的值,作为小字典
            :param data: 完整字典，某些字段
            :param fields: 列表，某些字段
            :param values: 返回的值
            :param currentKey: 当前的键值
            :return:
            """
        if isinstance(data, dict):
            for key, value in data.items():
                self.traverse_dict_field(value, fields, values, key)
        else:
            if currentKey in fields:
                values[currentKey] = data
        return values

    def zip_sql_data(self, names, rows):
        """
        names = 'user_id jobNumber driverName  app_id'.split()
        :param names: 字段名
        :param rows: sql查询获取的元组((1,2),(3,4))
        :return:
        """
        return [dict(zip(names, d)) for d in list(rows)]

    def cx_page_func(self,objs,page,rows):
        return  objs[(page - 1) * rows:page * rows]


# 超导企业微信发送消息
class workWechatSms:
    host_name = "https://qyapi.weixin.qq.com/cgi-bin"

    def __init__(
            self,
            user_id="13801587423",
            corpid="wx1e49648e862a7758",
            corpsecret="H5MQZ36D1RjEfJCcS4VT8FlDezFpPk6t0lc4VkVZGwg",
            agent_id=1,
    ):
        self.user_id = user_id
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agent_id = agent_id
        self.token()

        # print(self.token)

    def request(self, url, data):

        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            TimeoutError("请求超时。")

    def token(self):
        url = (f"{self.host_name}/gettoken"
               f"?corpid={self.corpid}"
               f"&corpsecret={self.corpsecret}")
        response = requests.get(url)
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
            # print(self.access_token)
        else:
            ValueError("无法得到token")

    def send(self, message):
        send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = (
            f"{self.host_name}/message/send?access_token={self.access_token}")
        data = {
            "touser": self.user_id,
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {
                "content": f"{send_time}_{message}"
            },
            "safe": 0,
            "enable_id_trans": 0
        }
        return self.request(url, data)

    def send_group(self, message):
        send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = (
            f"{self.host_name}/message/send?access_token={self.access_token}")
        data = {
            "touser": self.user_id,
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {
                "content": f"{send_time}_{message}"
            },
            "safe": 0,
            "enable_id_trans": 0
        }
        self.request(url, data)
