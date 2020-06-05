import click
import os
CREDPATH = '.config/creds.txt'
@click.command()
@click.option('--endpoint', default="",  help='The endpoint to fetch from.')
@click.option('--key', default="",  help='The endpoint to fetch from.')
@click.option('--token', default="",  help='The endpoint to fetch from.')
def hello(key, token, endpoint):
    """Simple program that greets NAME for a total of COUNT times."""
    if not os.path(CREDPATH).exists():
        print("No creds found.")
        if not key == "" and not token == "" and not endpoint == "":

            with open(CREDPATH, 'w') as f:
                f.write('\n'.join([key, token, endpoint]))
        else:
            print("You need to include all 3 parameters")

    else:
        with open(CREDPATH, 'r') as f:
            linelist = f.readlines()
            linelist = [a.strip() for a in linelist]
        print(linelist)


if __name__ == "__main__":
    hello()
