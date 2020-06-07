#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:Ruci
# datetime:2020/5/13 0:43
# software: PyCharm
import os,shutil,json


PATH = os.getcwd()
def order_msg(*args, **kwargs):
    return kwargs
def create_user(path):
    '''
    创建用户目录
    :param path:
    :return:
    '''
    os.makedirs(path)  # 创建用户
    info_imgs_path=os.path.join(path,'info_imgs')
    os.makedirs(info_imgs_path)
    img_path=os.path.join(PATH,'static','home','imgs','user-1.png')
    shutil.copy(img_path,info_imgs_path+'/default.png')
    a={'head_img_path':info_imgs_path+'/default.png'}
    with open(path+'/config.json','w') as f:
        json.dump(a,f,ensure_ascii=False)

def relat_path(path):
    '''返回config中的相对路径，以users开头'''
    return 'users'+path.replace('\\','/').split('users')[1]