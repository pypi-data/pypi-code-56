import sys, Ice, os.path, time ,argparse, datetime
from xtermcolor import colorize
from prettytable import PrettyTable
from random import randrange
from dotenv import load_dotenv
from ACJudge_Pkg import OJMod

__name__ = 'Client'

load_dotenv()

def list_problems(problems):
    problem_table = PrettyTable(['ID', 'Title'])
    problem_table.title = 'Problems'

    for p in problems:
        problem_table.add_row([p.id, p.title])
    print(problem_table)

def fetch_id(judge, _id):
    print(judge.problemDescription(_id))

def get_supported_ext():
    return [str(OJMod.SupportedLanguages.valueOf(i)).lower() for i in range(len(OJMod.SupportedLanguages._enumerators))]

def fetch_current(judge):
    print(judge.fetch())

def supported_lang_help():
    return f'[Invalid Language] Currently we only support {", ".join(get_supported_ext())}'

def parse_extension(filename):
    ext = os.path.splitext(filename)[1][1:].lower()
    for i, e in enumerate(get_supported_ext()):
        if e == ext:
            return OJMod.SupportedLanguages.valueOf(i)
    return None

def setup_env():
    address = input("Please enter the ip-address: ")
    port = input("Please enter the port: ")
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/.env', 'w') as f:
        f.write(f'export ASYMPTOTIC_COMPLEXITY_ADDRESS={address}\nexport ASYMPTOTIC_COMPLEXITY_PORT={port}')
    os.environ['ASYMPTOTIC_COMPLEXITY_ADDRESS'] = address
    os.environ['ASYMPTOTIC_COMPLEXITY_PORT'] = port

def _extract_source(f):
    source = None
    with open(f, 'r') as file:
        source = file.read()

    return source

def _process_testcase(test_case, res, test):
    status = None
    if not test:
        status = colorize("Passed", 0x06BA84) if res == OJMod.Results.A else colorize("Failed", 0xBA2A06)
    else: # Was a test run
        if res == OJMod.Results.A:
            status = colorize("Passed", 0x06BA84)
        elif res == OJMod.Results.WA:
            status = colorize("Wrong Answer", 0xBA2A06)
        else:
            issue = None
            if res == OJMod.Results.TLE:
                issue = "Time Limit Exceeded"
            elif res == OJMod.Results.MLE:
                issue = "Memory Limit Exceeded"
            elif res == OJMod.Results.CE:
                issue = "Compliation Error"
            elif res == OJMod.Results.RE:
                issue = "Runtime Error"
            else:
                issue = "ISSUE"
            status = colorize(issue, 0xDBC51C)
    return status

def _pending_testcase(test_case, cycle_tick):
    cycle_tick = cycle_tick % 4
    text = ''
    if cycle_tick == 0:
        text = '\\'
    elif cycle_tick == 1:
        text = '|'
    elif cycle_tick == 2:
        text = '/'
    elif cycle_tick == 3:
        text = '-'
    
    text += " Running..."
    print(f'[Test: {test_case}]: {colorize(text, 0x0596B9)}', end="\r"),

def _attempt(judge, args):
    f = args.test if args.test else args.submit
    ext = parse_extension(f)

    if not ext:
        raise RuntimeError(supported_lang_help())

    print()
    print(f'Creating New Submission.....')
    print(f'Submission({colorize(datetime.datetime.now(), 0x0596B9)})------------------------------------------------\n')
    
    source = _extract_source(f)

    if not source:
        raise RuntimeError("Invalid source file")

    results = None

    if not args.id:
        results = judge.test(source, ext) \
                        if args.test      \
                        else judge.submit(source, ext)
    else:
        results = judge.testWithID(int(args.id), source, ext) \
                        if args.test      \
                        else judge.submitWithID(int(args.id), source, ext)

    for test_case, res in enumerate(results):
        test_case += 1
        for i in range(13 + randrange(5)):
            _pending_testcase(test_case, i)
            time.sleep(randrange(5)/10)

        sys.stdout.write("\033[K")
        status = _process_testcase(test_case, res, args.test != None)
        print(f'[Test: {test_case}]: {status}', end="\r"),
        print()
        time.sleep(0.5)

    if not args.test:
        print()
        final_result = colorize("Accepted", 0x06BA84) \
                        if (results[-1] == OJMod.Results.A) \
                        else colorize("Not Accepted", 0xBA2A06)
        print(f'Submission({colorize(datetime.datetime.now(), 0x0596B9)}): {final_result}')
    print(f'\n----------------------Submission End--------------------------')

def _fetch(judge, args):
    print(colorize("Fetching....", 0x0596B9))
    print("\n")
    if not args.id:
        fetch_current(judge)
    else:
        fetch_id(judge, int(args.id))

def _list(judge):
    print(colorize("Fetching....", 0x0596B9))
    print("\n")
    list_problems(judge.listProblems())

def run(judge, args):
    if args.fetch:
        _fetch(judge, args)
    elif args.list:
        _list(judge)
    elif args.test or args.submit:
        _attempt(judge, args)


def parser():
    parser = argparse.ArgumentParser(
        description='ACJudge is terminal judge for the Asymptotic Complexity Group.')
    parser.add_argument('-t', '--test', help="Path to file for which you'd like to test")
    parser.add_argument('-s', '--submit', help="Path to file for which you'd like to submit")
    parser.add_argument('-f', '--fetch', action='store_true', help="Retrieve the current problem statement")
    parser.add_argument('-l', '--list', action='store_true', help="List all the available problems")
    parser.add_argument('-i', '--id', help="Focus on a specific problem id (this can be added to the --fetch, --test and --submit commands)")
    return parser

def parse():
    return parser().parse_args()

def main(): 

    if "ASYMPTOTIC_COMPLEXITY_ADDRESS" not in os.environ or "ASYMPTOTIC_COMPLEXITY_PORT" not in os.environ:
        setup_env()

    with Ice.initialize(sys.argv) as communicator:
        base = communicator.stringToProxy(f'Judge:tcp -h {os.environ.get("ASYMPTOTIC_COMPLEXITY_ADDRESS")} -p {os.environ.get("ASYMPTOTIC_COMPLEXITY_PORT")}')
        judge = OJMod.ComsPrx.checkedCast(base)

        if not judge:
            raise RuntimeError("Invalid proxy")
        
        args = parse()
        if args.fetch or args.test or args.submit or args.list:
            run(judge, args)
        else:
            parser().print_help()
