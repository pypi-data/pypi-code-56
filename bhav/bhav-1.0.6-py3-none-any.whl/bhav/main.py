from PyInquirer import prompt
from dotenv import load_dotenv
from datetime import datetime
import click
from os.path import expanduser
import os, sys, subprocess, json, logging
from bhav.util import today, fetch, unzip, writeCSV, readCSV, dateList

home = expanduser("~")
config_dir = home + '/.bhav'
config_file = config_dir + '/config'
config = dict()

# read configuration if present
if os.path.exists(config_file):
    with open(config_file, 'r') as handle:
        config = json.loads(handle.read())

@click.group()
def cli():
    pass

@click.group()
def conf():
    pass

@click.command()
def ls():
    if os.path.exists(config_file):
        with open(config_file, 'r') as handle:
            config = json.loads(handle.read())
            for key in config:
                print(key, ":", config[key])
    else:
        print('No configuration exists')

@click.command()
@click.option('-o', '--output-dir', default=None, help='e.g. C:/mydir . This is where the stock price data (bhavcopy) will be stored')
@click.option('-b', '--bse-url', default=None, help='BSE bhavcopy url template. Default- http://www.bseindia.com/download/BhavCopy/Equity/eq#-#day#-##-#month#-##-#year#-#_csv.zip')
@click.option('-B', '--bse-columns', default=None, help='BSE bhavcopy column order, default - SYMBOL,NAME,SC_GROUP,SC_TYPE,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,NO_TRADES,VOLUME,NET_TURNOV,TDCLOINDI')
@click.option('-n', '--nse-url', default=None, help='NSE bhavcopy url template. Default - https://www.nseindia.com/content/historical/EQUITIES/#-#year#-#/#n#month#n#/cm#-#day#-##n#month#n##-#year#-#bhav.csv.zip')
@click.option('-N', '--nse-columns', default=None, help='NSE bhavcopy column order, default - SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,VOLUME,TOTTRDVAL,DATE,TOTALTRADES,ISIN')
def update(output_dir, bse_url, bse_columns, nse_url, nse_columns):
    if not os.path.exists(config_file):
        # creating config directory if absent
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

    # set output directory
    if output_dir is not None:
        config['output_dir'] = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    elif 'output_dir' not in config:
        print("Setting output directory : ", home+ '/bhav')
        if not os.path.exists(home+ '/bhav'):
            os.makedirs(home+ '/bhav')
        config['output_dir'] = home+ '/bhav'
    
    # set bse bhavcopy url format
    if bse_url is not None:
        config['bse_url'] = bse_url
    elif 'bse_url' not in config:
        # https://www.bseindia.com/download/BhavCopy/Equity/EQ290520_CSV.ZIP
        config['bse_url'] = 'http://www.bseindia.com/download/BhavCopy/Equity/EQ#-#day#-##-#month#-##-#YY#-#_CSV.zip'
    
    # set bse bhavcopy url format
    if nse_url is not None:
        config['nse_url'] = nse_url
    elif 'nse_url' not in config:
        config['nse_url'] = 'https://archive.nseindia.com/content/historical/EQUITIES/#-#year#-#/#n#month#n#/cm#-#day#-##n#month#n##-#year#-#bhav.csv.zip'

    # set bse bhavcopy column order
    if bse_columns is not None:
        config['bse_columns'] = bse_columns
    elif 'bse_columns' not in config:
        config['bse_columns'] = 'SYMBOL,NAME,,,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,,VOLUME,,'
    
    # set nse bhavcopy column order
    if nse_columns is not None:
        config['nse_columns'] = nse_columns
    elif 'nse_columns' not in config:
        config['nse_columns'] = 'SYMBOL,,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,VOLUME,,DATE,,'
    
    # write config file
    with open(config_file, 'w') as fp:
        json.dump(config, fp)

@click.command()
@click.argument('date', default=today())
@click.option('-s', '--start-date', default=None, help='start date if downloading for a range of dates')
@click.option('-e', '--end-date', default=None, help='end date if downloading for a range of dates')
@click.option('-z', '--zipped', is_flag=True, help='if unzip required')
def bse(date, zipped, start_date, end_date):
    if not start_date:
        dates = [date]
    else:
        if not end_date:
            end_date = today()
        dates = dateList(start_date, end_date)
    
    print("fetching for dates : %s", dates)

    for process_date in dates:
        if not zipped:
            print("fetching uncompressed BSE bhavcopy for %s" % process_date)
            zipped = False
        else:
            print("fetching compressed BSE bhavcopy for %s" % process_date)
            zipped = True

        bse_root = config['output_dir'] + '/bse'
        if not os.path.exists(bse_root):
            os.mkdir(bse_root)
        target_directory = bse_root+ '/' + process_date[:4]
        if not os.path.exists(target_directory):
            os.mkdir(target_directory)
        fetch(config['bse_url'], process_date, target_directory, zipped, config['bse_columns'])
    

@click.command()
@click.argument('date', default=today())
@click.option('-s', '--start-date', default=None, help='start date if downloading for a range of dates')
@click.option('-e', '--end-date', default=None, help='end date if downloading for a range of dates')
@click.option('-z', '--zipped', is_flag=True, help='if unzip required')
def nse(zipped, date, start_date, end_date):
    if not start_date:
        dates = [date]
    else:
        if not end_date:
            end_date = today()
        dates = dateList(start_date, end_date)
    print("fetching for dates : %s", dates)
    for process_date in dates:
        if not zipped:
            print("fetching uncompressed NSE bhavcopy for %s" % process_date)
            zipped = False
        else:
            print("fetching compressed NSE bhavcopy for %s" % process_date)
            zipped = True
        
        nse_root = config['output_dir'] + '/nse'
        if not os.path.exists(nse_root):
            os.mkdir(nse_root)

        target_directory = nse_root +'/'+ process_date[:4]
        if not os.path.exists(target_directory):
            os.mkdir(target_directory)
        fetch(config['nse_url'], process_date, target_directory, zipped, config['nse_columns'])

conf.add_command(ls)
conf.add_command(update)
cli.add_command(conf)
cli.add_command(bse)
cli.add_command(nse)

if __name__ == '__main__':
    cli()