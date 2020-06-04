import argparse
from .add import main as add
from .delete import main as delete
from .init import main as init


def main():
    parser = argparse.ArgumentParser(description='shadowsocks 部署工具')
    parser.add_argument("action", help="可选 add | delete | init",
                        choices=["add", "delete", "init"])
    parser.add_argument("-p", "--port", type=int, dest="port",
                        help="指定监听的端口", default=0)
    parser.add_argument("--password", dest="password", help="指定密码")
    parser.add_argument("--encrypt", dest="encrypt",
                        help="指定加密算法", default="aes-256-gcm")
    args = parser.parse_args()
    if args.action == "add":
        add(port=args.port, encrypt=args.encrypt, password=args.password)
    elif args.action == "delete":
        delete(port=args.port)
    elif args.action == "init":
        init()
    else:
        raise
