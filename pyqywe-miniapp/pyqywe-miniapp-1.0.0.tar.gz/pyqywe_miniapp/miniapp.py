# -*- coding: utf-8 -*-

from pywe_storage import MemoryStorage
from pyqywe_token import BaseToken, final_access_token


class MiniApp(BaseToken):
    def __init__(self, appid=None, secret=None, storage=None):
        super(MiniApp, self).__init__()
        self.appid = appid
        self.secret = secret
        self.storage = storage or MemoryStorage()
        # wx.qy.login(OBJECT), Refer: https://work.weixin.qq.com/api/doc/90000/90136/91506
        # code2Session, Refer: https://work.weixin.qq.com/api/doc/90000/90136/91507
        self.JSCODE2SESSION = self.QYAPI_DOMAIN + '/cgi-bin/miniprogram/jscode2session?access_token={access_token}&js_code={code}&grant_type={grant_type}'

    def sessionKey(self, unid=None):
        # https://developers.weixin.qq.com/community/develop/doc/00088a409fc308b765475fa4351000?highLine=session_key
        # sessionKey 非共用
        return '{0}:{1}:sessionKey'.format(self.appid, unid or '')

    def update_params(self, appid=None, secret=None, storage=None):
        self.appid = appid or self.appid
        self.secret = secret or self.secret
        self.storage = storage or self.storage

    def store_session_key(self, appid=None, secret=None, session_key=None, unid=None, storage=None):
        # Update params
        self.update_params(appid=appid, secret=secret, storage=storage)
        # Store sessionKey
        return self.storage.set(self.sessionKey(unid=unid), session_key)

    def get_session_info(self, appid=None, secret=None, code=None, grant_type='authorization_code', unid=None, token=None, storage=None):
        """
        // 正常返回的JSON数据包
        {
            "userid": "USERID",
            "session_key": "SESSIONKEY",
        }
        """
        # Update params
        self.update_params(appid=appid, secret=secret, storage=storage)
        # Fetch sessionInfo
        access_token = final_access_token(self, appid=appid, secret=secret, token=token, storage=storage)
        session_info = self.get(self.JSCODE2SESSION, access_token=access_token, code=code, grant_type=grant_type) if code else {}
        # Store sessionKey
        if session_info and unid:
            self.storage.set(self.sessionKey(unid=unid), session_info.get('session_key', ''))
        return session_info

    def get_session_key(self, appid=None, secret=None, code=None, grant_type='authorization_code', unid=None, storage=None, only_frorage=False):
        # Update params
        self.update_params(appid=appid, secret=secret, storage=storage)
        # Only get sessionKey from storage
        if only_frorage:
            return self.storage.get(self.sessionKey(unid=unid))
        # Fetch sessionKey
        # From storage
        session_key = '' if code or not unid else self.storage.get(self.sessionKey(unid=unid))
        # From request api
        if not session_key:
            session_key = self.get_session_info(appid=self.appid, secret=self.secret, code=code, grant_type=grant_type, storage=self.storage).get('session_key', '')
        return session_key

    def get_userid(self, appid=None, secret=None, code=None, grant_type='authorization_code', storage=None):
        # Update params
        self.update_params(appid=appid, secret=secret, storage=storage)
        # Fetch userid
        userid = self.get_session_info(appid=self.appid, secret=self.secret, code=code, grant_type=grant_type, storage=self.storage).get('userid', '')
        return userid


miniapp = MiniApp()
store_session_key = miniapp.store_session_key
get_session_info = miniapp.get_session_info
get_session_key = miniapp.get_session_key
get_userid = miniapp.get_userid
