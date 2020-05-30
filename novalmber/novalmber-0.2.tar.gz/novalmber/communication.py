#coding=utf-8
'''
这是用来在NovalIDE和其他脚本之间通信的插件！
''' 

import socket

def communicate(port=37012,message='{\'website\':\'https://www.4399.com\'}'):
    '''
    进行通信的函数，输入为端口号和信息。
    '''
    host = 'localhost'
    port = port
    client = None
    if True:
        if client is None:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(1)
                client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #心跳检测
                client.connect((host, port))
            except Exception as  e:
                print(e)
                
        try:
            client.send(message.encode('utf8'))
            data = client.recv(1024)
            client.close()
            print(data)
            if data.decode('utf8').startswith('r'):
                return True
            else:
                return False
        except Exception as  e:
            print(e)
            return False

if __name__ =='__main__':           
    c=communicate(port=37012)# 37021是运行模式，37012是调试模式。
    print(c)