import argparse

from FLF import RpcConnector


def main():
    parser = argparse.ArgumentParser(description="Example RPCServer for RabbitMQ")
    parser.add_argument("--host", default="localhost", type=str, help="host")
    parser.add_argument("--port", default=5672, type=int, help="port")
    parser.add_argument("--username", default="rabbitmq", type=str, help="username")
    parser.add_argument("--password", default="rabbitmq", type=str, help="password")
    args = parser.parse_args()

    connector = RpcConnector(host=args.host, port=args.port, username=args.username, password=args.password)

    file_bytes = b"hello, this is a file"
    r1 = connector.call_procedure("addition", {"a": 22, "b": 33}, {"file": file_bytes})
    r2 = connector.call_procedure("multiply", {"a": 33, "b": 33}, {"file": file_bytes})
    r3 = connector.call_procedure("addition", {"a": 234, "b": 33}, {"file": file_bytes})
    r4 = connector.call_procedure("multiply", {"a": 22, "b": 33}, {"file": file_bytes})

    print(r1[0], r2[0], r3[0], r4[0], r1[1], r2[1], r3[1], r4[1])


if __name__ == "__main__":
    main()

