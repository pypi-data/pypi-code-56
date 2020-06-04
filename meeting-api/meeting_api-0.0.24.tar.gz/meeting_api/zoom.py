import requests
import time
import base64
import hashlib
import hmac


def get_signature(api_key, api_secret, meeting_number, role, **kwargs):
    ts = int(round(time.time() * 1000)) - 30000
    msg = api_key + str(meeting_number) + str(ts) + str(role)
    message = base64.b64encode(bytes(msg, 'utf-8'))
    secret = bytes(api_secret, 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256)
    hash = base64.b64encode(hash.digest())
    hash = hash.decode("utf-8")
    tmpString = "%s.%s.%s.%s.%s" % (
        api_key, str(meeting_number), str(ts),
        str(role), hash)
    signature = base64.b64encode(bytes(tmpString, "utf-8"))
    signature = signature.decode("utf-8")
    signature = signature.rstrip("=")

    return signature


class Zoom:
    def __init__(self, access_token):
        self.access_token = access_token
        self.message = None
        self.users = None
        self.user = None
        self.meeting = None

    def __get_users(self):
        url = 'https://api.zoom.us/v2/users/'
        headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
        rq = requests.get(url=url, headers=headers)

        json = rq.json()
        if 'code' in json.keys():
            self.message = json['message']
            return False
        else:
            self.users = json['users']
            return True

    def __create_user(self, email, first_name, last_name):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        json = {
            'action': 'create',
            'user_info': {
                'email': email,
                'type': 1,
                'first_name': first_name,
                'last_name': last_name
            }
        }
        url = 'https://api.zoom.us/v2/users/'

        rq = requests.post(url=url, headers=headers, json=json)

        json = rq.json()
        if 'code' in json.keys():
            raise Exception(json['message'])
        else:
            self.user = json

    def update_user(self, email, first_name='', last_name=''):
        get_users_success = self.__get_users()
        if get_users_success:
            # update user if existed
            is_existed = False
            for user in self.users:
                if user['email'] == email:
                    self.user = user
                    is_existed = True

            # create user if not existed
            if is_existed is False:
                self.__create_user(email, first_name, last_name)

            return True
        else:
            return False

    def create_meeting(
            self, schedule_for, first_name='', last_name='', **kwargs):
        if self.update_user(schedule_for, first_name, last_name) is False:
            return False

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        json = kwargs

        url = 'https://api.zoom.us/v2/users/{}/meetings'.format(
            self.user['id'])

        rq = requests.post(url, headers=headers, json=json)
        json = rq.json()
        if 'code' in json.keys():
            self.message = json['message']
            return False
        else:
            self.meeting = json
            return True
