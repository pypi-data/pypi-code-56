import click
import os.path

cred_path = '.config/creds.txt'
@click.command()
@click.option('--endpoint', default="",  help='The endpoint to fetch from.')
@click.option('--key', default="",  help='The endpoint to fetch from.')
@click.option('--token', default="",  help='The endpoint to fetch from.')
def hello(key, token, endpoint):
    """Simple program that greets NAME for a total of COUNT times."""
    if not os.path.exists(cred_path):
        print("No creds found.\nCreating a .config folder")
        os.mkdir('.config')
        if not key == "" and not token == "" and not endpoint == "":

            with open(cred_path, 'w') as f:
                f.write('\n'.join([key, token, endpoint]))
                print("Credentials saved,restart the app.")
        else:
            print("You need to include all 3 parameters")

    else:
        with open(cred_path, 'r') as f:
            linelist = f.readlines()
            linelist = [a.strip() for a in linelist]
        key, token, endpoint = linelist


if __name__ == "__main__":
    hello()
