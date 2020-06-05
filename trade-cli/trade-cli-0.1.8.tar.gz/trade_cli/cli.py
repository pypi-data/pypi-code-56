import click
import os.path
from tabulate import tabulate
import requests as rq
from time import sleep
from tqdm import tqdm
from pick import pick

cred_path = '.config/creds.txt'
@click.command()
@click.option('--endpoint', default="",  help='The endpoint to fetch from')
@click.option('--key', default="",  help='Trello key')
@click.option('--token', default="",  help='Trello token')
@click.option('-p','--paint',is_flag=True,help="Paint flag")
@click.option('-q','--quality', default='Unique', help="Item quality. Defaults to Unique")
@click.argument('item_set',nargs=1)
def hello(key, token, endpoint,item_set,paint,quality):
    """Simple program that fetches some API with some params."""
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
        print(tabulate([
            ['paint',paint],
            ['quality',quality],
            ['item_set',item_set]
        ]))
        url = "https://api.trello.com/1/cards/"
        listak = rq.get("https://trade.matyi.top/api/listak").json()
        option, index = pick(list(listak.keys()),"Choose a list")
        
        print(option)
        print(index)


        payload = {
            'key': key,
            'token': token,
            'idList': '5eaaba61b1b97881cf921d38',
            'name': '',
            'desc': '',
            'urlSource': '',
        }
        exit()
        for item in tqdm(listak['paints']+listak['taunts']+listak['strange_parts']+listak['tools']):
            r = rq.get(f'https://steam-trade-profit.matyi.now.sh/api/bsorder?item={item}&quality={quality}&paint_flag={int(paint)}')
        try:
            if r.json()['profitable']==1:
                payload['name'] = str(round(max(r.json()['profit']),2))+' '+str(r.json()['item'])
                payload['desc'] += str(','.join(str(x) for x in r.json()['profit']))+'\n'+str(','.join(r.json()['reason']))+'\n\n## Backpack\n'+str(r.json()['bptf_link'])+'\n\n## STN\n'+str(r.json()['stn_link'])
                payload['urlSource'] = str(r.json()['bptf_link'])
                rq.post(url,data=payload);
        except:
            print(item,'error')
        sleep(6)


if __name__ == "__main__":
    hello()