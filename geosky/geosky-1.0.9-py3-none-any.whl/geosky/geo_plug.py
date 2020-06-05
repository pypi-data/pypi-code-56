import json
import os
#r_path = os.path.abspath('cities.json')
#print(r_path)
#f = open(r_path,)
print("[Info] Loading Data")
import requests as r
url = 'https://raw.githubusercontent.com/jyotiprakash-work/geosky/master/cities.json'
data = r.get(url)
#data = json.load(f)
data=json.loads(data.text)
print("[Info] Loading Data completed")
def all_CountryNames():
	all_country = list()
	for dct in data:
		all_country.append(dct['country'])
	return list(dict.fromkeys(all_country))

def all_Country_StateNames():
	all_country = list()
	for dct in data:
		all_country.append(dct['country'])
	all_country = list(dict.fromkeys(all_country))
	state_list = list()
	for country in all_country:
		all_state = list()
		for dct in data:
			if dct['country'] == country:
				all_state.append(dct['subcountry'])
		all_state = list(dict.fromkeys(all_state))
		state_list.append({country:all_state})
	return json.dumps(state_list)

def all_State_CityNames(flag='all'):
	all_subcountry = list()
	all_city_list = list()
	for dct in data:
		all_subcountry.append(dct['subcountry'])
	all_subcountry = list(dict.fromkeys(all_subcountry))
	if flag == 'all':
		for subcountry in all_subcountry:
			city_list = list()
			for dct in data:
				if dct['subcountry'] == subcountry:
					city_list.append(dct['name'])
			city_list = list(dict.fromkeys(city_list))
			all_city_list.append({subcountry:city_list})
	else:
		city_list = list()
		subcountry = flag
		for dct in data:
			if dct['subcountry'] == subcountry:
				city_list.append(dct['name'])
		city_list = list(dict.fromkeys(city_list))
		all_city_list.append({subcountry:city_list})

	
	return json.dumps(all_city_list)





#print(all_State_CityNames())