from b1u3calculator import lexer, token, parser, evaluator
import sys

PROMPT = ">> "

def lexer_main():
    print("Let's go!!!")
    print(PROMPT, end='')
    line = input()
    while line != "":
        lex = lexer.Lexer(line)
        tok = lex.next_token()
        while tok.type != token.EOF:
            print(f"<type: {tok.type}, literal: {tok.literal}>")
            tok = lex.next_token()
        print(PROMPT, end='')
        line = input()


def parser_main():
    print("Let's go!!!")
    print(PROMPT, end='')
    line = input()
    while line != "":
        lex = lexer.Lexer(line)
        par = parser.Parser(lex)
        program = par.parse_program()
        if len(par.errors) != 0:
            for msg in par.errors:
                print(msg)
            print(PROMPT, end='')
            line = input()
            continue
        print(str(program))
        print(PROMPT, end='')
        line = input()


def eval_main():
    print("Let's go!!!")
    print(PROMPT, end='')
    line = input()
    env = {}
    funcs = {}
    while line != "":
        lex = lexer.Lexer(line)
        par = parser.Parser(lex)
        program = par.parse_program()
        if len(par.errors) != 0:
            for msg in par.errors:
                print(msg)
            print(PROMPT, end='')
            line = input()
            continue
        try:
            res = evaluator.eval(program, env, funcs)
            print(res.inspect())
        except evaluator.EvaluatedError as e:
            print(e.msg)
        print(PROMPT, end='')
        line = input()


def file_main(f):
    res = None
    env = {}
    funcs = {}
    lex = lexer.Lexer(f.read())
    par = parser.Parser(lex)
    program = par.parse_program()
    if len(par.errors) != 0:
        for msg in par.errors:
            print(msg, file=sys.stderr)
    try:
        res = evaluator.eval(program, env, funcs)
        print(res.inspect())
    except evaluator.EvaluatedError as e:
        print(e.msg, file=sys.stderr)
    
