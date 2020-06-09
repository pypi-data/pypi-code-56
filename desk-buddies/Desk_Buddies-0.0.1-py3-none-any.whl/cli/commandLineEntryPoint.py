from cli import argsParser
from cmnSys.action import Action
from client import cliClient
from server import cliServer


def main():
    args = argsParser.parse_args()
    if args:
        if args.action == Action.SERVE:
            cliServer.main(args)
        else:
            cliClient.main(args)


if __name__ == "__main__":
    main()
