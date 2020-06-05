import argparse
from passgen import get_sequence, generate_password
import sys

desc = 'Generates a password consisting of selected characters and the specified length.'
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('-l', '--lower', help='password should contain lowercase letters', action='store_true')
parser.add_argument('-u', '--upper', help='password should contain uppercase letters', action='store_true')
parser.add_argument('-d', '--digits', help='password should contain digits', action='store_true')
parser.add_argument('-s', '--special',
                    help='password should contain special characters',
                    action='store_true'
)
parser.add_argument('-a', '--all',
                    help='''password should contain all of the above character groups,
                            i.e. lowercase letters, uppercase letters, digits and special characters''',
                    action='store_true'
)
parser.add_argument('-c', '--custom',
                    help='''password should contain only characters passed as argument value,
                            e.g. "abcd"; if the custom option is selected, other options regarding
                            the password structure are not taken into account'''
)
parser.add_argument('-n', '--length', help='set password length', type=int, default=16)


def main(raw_args=None):
    sequence = ''
    args = parser.parse_args(raw_args)
    if args.custom:
        sequence = args.custom
    elif args.all:
        sequence = get_sequence(
            lower=True,
            upper=True,
            digits=True,
            special=True
        )
    else:
        try:
            sequence = get_sequence(
                lower=args.lower,
                upper=args.upper,
                digits=args.digits,
                special=args.special
            )
        except TypeError as e:
            print(str(e), file=sys.stderr)
            exit(1)

    print(generate_password(sequence, args.length), file=sys.stdout)


if __name__ == "__main__":
    main(sys.argv[1:])
