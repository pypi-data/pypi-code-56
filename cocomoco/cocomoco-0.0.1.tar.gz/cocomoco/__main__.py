import sys
import cocomoco


def main():
    cm = cocomoco.calculate(100000, model=cocomoco.Embedded())
    print(cm)


if __name__ == "__main__":
    sys.exit(main() or 0)
