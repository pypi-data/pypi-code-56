#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:Ruci
# datetime:2020/6/7 13:56
# software: PyCharm

import os,requests,json

class Code(object):
    def __init__(self,url,path,account,passwd):
        '''
        :param url: 请求网址
        :param path: 图片路径
        :param account: 账号
        :param passwd: 密码
        '''
        self._url=url
        self._codeImgPath=path
        self._file=self.read_img()
        self._account=account
        self._passwd=passwd
        self._number=0  # 这个对象，请求了多少个验证码。
    def read_img(self):
        p=os.path.exists(self._codeImgPath)
        if p:
            file=open(self._codeImgPath,'rb')
            return file
        else:
            raise Exception('图片路径不存在！')
    def requestCode(self):
        files = {'img': ('code.jpg', self._file, 'image/jpg')}
        res = requests.post(self._url, data={'account': self._account,'passwd':self._passwd}, files=files)
        self._file.close()
        return res.content.decode()
    def run(self):
        # 发送请求
        response=self.requestCode()
        # 解析数据
        response=json.loads(response,encoding='utf-8')
        if response.get('status')==200:
            # 请求成功，number加1
            self._number+=1
        return response
    def get_number(self):
        '''
        :return: number值
        '''
        return self._number

if __name__=='__main__':
    a=Code('http://127.0.0.1:8000/req/yzm/','../app1/yzm/discuz/spxp.jpg','ruci','123456')
    b=a.run()
    print(b)
    c=a.get_number()
    print(c)