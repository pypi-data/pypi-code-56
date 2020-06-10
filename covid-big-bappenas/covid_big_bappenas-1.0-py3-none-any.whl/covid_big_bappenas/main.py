import click
import csv
import requests

from datetime import datetime

#host
host = "https://data.covid19.go.id"
#api-endpoint 
url_list_kab_kota = host + "/grafik/psbb-epidemic/epidemic-peta"
url_epidemic = host + "/grafik/psbb-epidemic/epidemic"
#list of prov_kab_kota data with their code
data_kab_kot = []

def welcome():
    """A helper pip package for Covid BIG BAPPENAS Project."""
    click.echo('Welcome to Covid-Big-Bappenas Package!')
    click.echo('===============================================')
    click.echo('Author: Muhammad Hasannudin Yusa')
    click.echo('Office: Pusat PPIG - Badan Informasi Geospasial')
    click.echo('Email: muhammad.hasannudin@big.go.id')
    click.echo('===============================================')
    insert_key()
	
@click.command()
@click.option('--key', prompt='Your key', help='The key to login.')
def insert_key(key):
    """A helper pip package for Covid BIG BAPPENAS Project."""
    init_harvester(key)
	
	
def init_harvester(key):
    click.echo('Harvester is initiated!')
    run_harvester(key)

def run_harvester(key):
    click.echo('Try to connect to BLC: %s' % host)
    listing_kab_kota(key)
	
def listing_kab_kota(key):
	HEADERS = {'Cookie': 'PHPSESSID='+key}
	r = requests.get(url = url_list_kab_kota,
		headers=HEADERS
    )
	if r.status_code != 200:
		# This means something went wrong.
		raise ApiError('GET /epidemic-peta/ {}'.format(r.status_code))
	
	if r.headers['Content-Type'] == 'application/json; charset=UTF-8':
		json_response = r.json()
		click.echo('Connected!')
		hits = json_response["hits"]["hits"]
		click.echo('Get list all regencies and municipalities')
		for i in hits: 
			item = {'prov':i["_source"]["prov"], 'kota':i["_source"]["kota"], 'kode_prov':i["_source"]["kode_prov"], 'kode_kota':i["_source"]["kode_kota"]}
			#print(item)
			data_kab_kot.append(item)
		data_kab_kot.sort(key = lambda x: (x["prov"], x["kota"]))
		click.echo('Done!')
		harvest_and_write_data(key)
	else:
		click.echo('Failed to connect to BLC. Please check your key.')

def harvest_and_write_data(key):
	HEADERS = {'Cookie': 'PHPSESSID='+key}
	click.echo('Harvesting is started')
	name_file = datetime.today().strftime('%Y%m%d-%H%M%S')
	with open(name_file+'.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["No", "Nama_Provinsi", "Kode_Provinsi", "Nama_Kab_Kota", "Kode_Kab_Kota", "Tanggal", "Positif", "Kasus_Kumulatif"])
		no = 1
		k = 1
		for o in data_kab_kot:
			filter_prov = o["kode_prov"]
			filter_kota = o["kode_kota"]
			tipe = 'day'
			akumulatif = 0
			nama_prov = o["prov"]
			kode_prov = o["kode_prov"]
			nama_kabkot = o["kota"]
			kode_kabkot = o["kode_kota"]
			click.echo('%s, %s - %s ' % (k, o["prov"], o["kota"]))
			PARAMS = {'filter_prov':filter_prov,'filter_kota':filter_kota,'tipe':tipe}
			harvest = requests.get(url = url_epidemic,
				params=PARAMS,
				headers=HEADERS
			)
			if harvest.status_code != 200:
				# This means something went wrong.
				raise ApiError('GET /epidemic/ {}'.format(harvest.status_code))
			
			if harvest.headers['Content-Type'] == 'application/json; charset=UTF-8':
				harvest_response = harvest.json()
				for l in harvest_response:
					akumulatif += l["kasus_positif"]
					writer.writerow([no, nama_prov, kode_prov, nama_kabkot, kode_kabkot, l["key_as_string"], l["kasus_positif"], akumulatif])
					no += 1
			else:
				click.echo('Failed to obtain data.')
			k += 1
		click.echo('Harvesting is finished') 
		click.echo('Data is saved successfully. The file name is %s.csv' % name_file)

if __name__ == '__main__':
    welcome()