import requests
import json
import warnings
from pprint import pprint

warnings.simplefilter( "ignore" )

def pairing_stage_1( ip_address ):
	headers = {
		"Content-Type": "application/json" ,
	}
	data = {
		"_url": "/pairing/start" ,
		"DEVICE_ID": "pyvizio" ,
		"DEVICE_NAME": "Python Vizio" ,
	}
	url = f"https://{ip_address}:7345/pairing/start"
	response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
	response.raise_for_status()

	# Should Return
	# {
	# 	'ITEM': {'CHALLENGE_TYPE': 1, 'PAIRING_REQ_TOKEN': 802927 } ,
	# 	'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'}
	# }
	result = json.loads( response.text )
	pprint( result )
	return result

def pairing_stage_2( ip_address , pairing_request_token , code_displayed_on_tv ):
	headers = {
		"Content-Type": "application/json" ,
	}
	data = {
		"_url": "/pairing/pair" ,
		"DEVICE_ID": "pyvizio" ,
		"DEVICE_NAME": "Python Vizio" ,
		"CHALLENGE_TYPE": 1 ,
		"PAIRING_REQ_TOKEN": pairing_request_token ,
		"RESPONSE_VALUE": str( code_displayed_on_tv )
	}
	print( data )
	url = f"https://{ip_address}:7345/pairing/pair"
	response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
	response.raise_for_status()

	# Should Return
	# {
	# 	'ITEM': {'AUTH_TOKEN': 'Zhehzvszfq' } ,
	# 	'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'}
	# }
	result = json.loads( response.text )
	pprint( result )
	return result


def get_volume( ip_address , access_token ):
	headers = {
		'AUTH': access_token
	}
	url = f"https://{ip_address}:7345/menu_native/dynamic/tv_settings/audio/volume"
	response = requests.get( url , headers=headers , verify=False )
	response.raise_for_status()

	# Should Return
	# {'HASHLIST': [2308455925, 729988045],
	#  'ITEMS': [{'CNAME': 'volume',
	#             'ENABLED': 'FALSE',
	#             'HASHVAL': 1731828541,
	#             'NAME': 'Volume',
	#             'TYPE': 'T_VALUE_V1',
	#             'VALUE': 10}],
	#  'PARAMETERS': {'FLAT': 'TRUE', 'HASHONLY': 'FALSE', 'HELPTEXT': 'FALSE'},
	#  'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'},
	#  'URI': '/menu_native/dynamic/tv_settings/audio/volume'}

	result = json.loads( response.text )
	pprint( result )
	return result


if __name__ == "__main__":

	#pairing_stage_1( "192.168.1.102" )

	#pairing_stage_2( "192.168.1.102" , 434136 , 3232 )

	get_volume( "192.168.1.102" , "Zhehzvszfq" )

	# Found where it was calling with: https://codeburst.io/how-i-use-python-debugger-to-fix-code-279f11f75866?gi=fed84a534cf9
	# Put debugger on cli.py --> pair()

	# Somehow it calls the sitepackages , I just put print commands in
	# /home/morphs/.local/lib/python3.8/site-packages/pyvizio/_protocol.py

	# Continue Testing via
	# cd /home/morphs/WORKSPACE/PYTHON/VizioController/pyvizio/
	# python3 pyvizio/cli.py --ip=192.168.1.102:7345 --auth=Zhehzvszfq get-volume-level

	# Just keep converting http request into functions, then to class