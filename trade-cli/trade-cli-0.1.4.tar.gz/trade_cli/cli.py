import click
import os

@click.command()
@click.option('--endpoint', default="",  help='The endpoint to fetch from.')
@click.option('--key', default="",  help='The endpoint to fetch from.')
@click.option('--token', default="",  help='The endpoint to fetch from.')
def hello(key, token, endpoint):
    """Simple program that greets NAME for a total of COUNT times."""
    
    if key=="" or endpoint=="" or token=="" and not os.path('.config/creds.txt').exists():
        print('You need to specify token, key, and endpoint')
        exit()
    try:
        with open('.config/creds.txt','r') as f:
            linelist = f.readlines()

        print(linelist)
    except:
        print('No config was found, creating one based on your input.')
        with open('.config/creds.txt','w') as f:
            f.write('\n'.join([key,token,endpoint]))
if __name__ == "__main__":
    hello()
