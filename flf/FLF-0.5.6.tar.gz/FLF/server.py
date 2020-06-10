import argparse

from FLF import RpcServer


def addition(params, files):
    file_bytes = b"yes, this is response"

    return {"response": "hello" + str(params["a"])}, {"file": file_bytes}


def multiply(params, files):
    file_bytes = b"yes, this is response"

    return {"response": "hello" + str(params["a"] * 10)}, {"file": file_bytes}


def default(params, files):
    return {"response": "hello world"}, {}


def main():
    parser = argparse.ArgumentParser(description="Example RPCServer for RabbitMQ")
    parser.add_argument("--host", default="localhost", type=str, help="host")
    parser.add_argument("--port", default=5672, type=int, help="port")
    parser.add_argument("--username", default="rabbitmq", type=str, help="username")
    parser.add_argument("--password", default="rabbitmq", type=str, help="password")
    args = parser.parse_args()

    app = RpcServer(host=args.host, port=args.port, username=args.username, password=args.password,
                    procedures={"addition": addition, "multiply": multiply, "default": default})


if __name__ == "__main__":
    main()
