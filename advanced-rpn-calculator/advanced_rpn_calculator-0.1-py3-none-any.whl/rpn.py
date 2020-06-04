import argparse
from advanced_rpn_calculator.calculator import Calculator


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "statement", nargs="*", help="Single line statement",)
    parser.add_argument(
        "-f", "--file", type=str, help="full path (absolute) to the file"
    )
    return parser.parse_args()

def main():
    args = get_args()
    cal = Calculator()
    if args.statement:
        cal.evaluate(" ".join(args.statement))
        print(cal.stack)
        return
    if args.file:
        with open(args.file, 'r') as file:
            for string in file.readlines():
                cal.evaluate(string)
    cal.loop()

if __name__=="__main__":
    main()
