from . import repl
import argparse
import sys


def entry():
    ap = argparse.ArgumentParser()
    ap.add_argument("-l", "--lexer", help="execute lexer repl", action="store_true")
    ap.add_argument("-p", "--parser", help="execute parser repl", action="store_true")
    ap.add_argument("-f", "--file", help="execute parser repl", nargs=1)
    args = ap.parse_args()
    if args.lexer:
        repl.lexer_main()
    elif args.parser:
        repl.parser_main()
    elif args.file:
        try:
            repl.file_main(open(args.file[0]))
        except OSError as e:
            print(e.strerror, file=sys.stderr)
    else:
        repl.eval_main()

