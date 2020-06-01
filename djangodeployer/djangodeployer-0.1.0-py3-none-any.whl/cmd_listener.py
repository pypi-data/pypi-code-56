import sys
from djangodeployer.installer import Djangodeployer


def main():
    try:
        command = sys.argv[1:]
        Djangodeployer().run_command(command)
    except Exception as exe:
        print(exe)


if __name__ == '__main__':
    main()
