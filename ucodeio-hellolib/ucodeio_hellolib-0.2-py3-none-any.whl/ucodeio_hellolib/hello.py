import argparse

def get_hello_message(name=None):
    if name:
        return f"hello {name}"
    else:
        return "hello world!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print a hello message")
    parser.add_argument("name", nargs='?', type=str, default=None, help="Name to apply to hello message (optional)")
    parser.add_argument("--verbose", "-v", action="store_true", help="verbose output")
    args = parser.parse_args()
    if args.verbose:
        print('verbose: True')
        print(f'name: {args.name}')
    print (get_hello_message(args.name))