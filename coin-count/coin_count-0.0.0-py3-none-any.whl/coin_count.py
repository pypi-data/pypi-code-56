import argparse
import script

parser = argparse.ArgumentParser(description='Prints a change to be returned from a given sum amount in the number of coins')
parser.add_argument('amount', type=int, help='Enter number')
args = parser.parse_args()

if __name__ == '__main__':
    print(script.coin_count(args.amount))