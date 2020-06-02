import typing as ty
import sys
from termcolor import colored
from fastdiff import compare


def format_line(line):
    line = line.rstrip('\n')
    if line.startswith('-'):
        return colored(line, 'red', attrs=['bold'])
    elif line.startswith('+'):
        return colored(line, 'green')
    elif line.startswith('?'):
        return (colored('') + colored(line, 'yellow', attrs=['bold']))

    return colored('') + colored(line, 'white', attrs=['dark'])


def diff(text1: str, text2: str, output: bool = False) -> ty.Tuple[colored, bool]:
    lines = []
    error = False
    for line in list(compare(text1, text2)):
        lines.append(format_line(line))
        if line.startswith(("-", "+", "?")):
            error = True
    return lines, error


if __name__ == "__main__":
    text1 = """
    I am
    some text
    here
    """

    text2 = """
    I am
    some texp
    here
    """

    res, error = diff(text1, text2, output=True)
    for line in res:
        sys.stdout.write("\n" + line)

    if error is True:
        print("ERROR")
