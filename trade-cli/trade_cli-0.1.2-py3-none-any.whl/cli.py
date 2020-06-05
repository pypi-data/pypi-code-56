import click


@click.command()
@click.option('--endpoint', default="",  help='The endpoint to fetch from.')
@click.option('--key', default="",  help='The endpoint to fetch from.')
@click.option('--token', default="",  help='The endpoint to fetch from.')
def hello(key, token, endpoint):
    """Simple program that greets NAME for a total of COUNT times."""
    
    if key=="" or endpoint=="" or token=="":
        print('You need to specify token, key, and endpoint')
        exit()
    with open('demo.txt','r') as f:
        linelist = f.readlines()

        print(linelist)
    with open('creds.txt','w+') as f:
        f.write('\n'.join([key,token,endpoint]))
if __name__ == "__main__":
    hello()
