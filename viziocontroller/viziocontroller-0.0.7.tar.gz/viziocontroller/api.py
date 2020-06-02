import requests
import json
import warnings
from pprint import pprint

warnings.simplefilter( "ignore" )

class API:

	def __init__( self , options={} ):
		self.options = options

	def pairing_stage_1( self , ip_address ):
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
		#pprint( result )
		return result["ITEM"]["PAIRING_REQ_TOKEN"]

	def pairing_stage_2( self , ip_address , pairing_request_token , code_displayed_on_tv ):
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
		url = f"https://{ip_address}:7345/pairing/pair"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return
		# {
		# 	'ITEM': {'AUTH_TOKEN': 'Zhehzvszfq' } ,
		# 	'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'}
		# }
		result = json.loads( response.text )
		#pprint( result )
		return result["ITEM"]["AUTH_TOKEN"]

	def get_power_state( self ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/state/device/power_mode"
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
		#pprint( result )
		return result

	def power_on( self ):
		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": "/key_command/" ,
			"KEYLIST": [{
				"CODESET": 11 ,
				"CODE": 1 ,
				"ACTION": "KEYPRESS"
			}]
		}
		url = f"https://{self.options['ip']}:7345/key_command/"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return
		# {'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'}, 'URI': '/key_command/'}
		result = json.loads( response.text )
		#pprint( result )
		return result

	def power_off( self ):
		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": "/key_command/" ,
			"KEYLIST": [{
				"CODESET": 11 ,
				"CODE": 0 ,
				"ACTION": "KEYPRESS"
			}]
		}
		url = f"https://{self.options['ip']}:7345/key_command/"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return
		# {'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'}, 'URI': '/key_command/'}
		result = json.loads( response.text )
		#pprint( result )
		return result

	def get_volume( self ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/dynamic/tv_settings/audio/volume"
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
		#pprint( result )
		return result["ITEMS"][0]["VALUE"]

	def volume_down( self ):
		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": "/key_command/" ,
			"KEYLIST": [{
				"CODESET": 5 ,
				"CODE": 0 ,
				"ACTION": "KEYPRESS"
			}]
		}
		url = f"https://{self.options['ip']}:7345/key_command/"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return
		# {"STATUS": {"RESULT": "SUCCESS", "DETAIL": "Success"}, "URI": "/key_command/"}
		result = json.loads( response.text )
		#pprint( result )
		return result

	def volume_up( self ):
		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": "/key_command/" ,
			"KEYLIST": [{
				"CODESET": 5 ,
				"CODE": 1 ,
				"ACTION": "KEYPRESS"
			}]
		}
		url = f"https://{self.options['ip']}:7345/key_command/"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return
		# {"STATUS": {"RESULT": "SUCCESS", "DETAIL": "Success"}, "URI": "/key_command/"}
		result = json.loads( response.text )
		#pprint( result )
		return result

	def mute_off( self ):
		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": "/key_command/" ,
			"KEYLIST": [{
				"CODESET": 5 ,
				"CODE": 2 ,
				"ACTION": "KEYPRESS"
			}]
		}
		url = f"https://{self.options['ip']}:7345/key_command/"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return
		# {"STATUS": {"RESULT": "SUCCESS", "DETAIL": "Success"}, "URI": "/key_command/"}
		result = json.loads( response.text )
		#pprint( result )
		return result

	def mute_on( self ):
		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": "/key_command/" ,
			"KEYLIST": [{
				"CODESET": 5 ,
				"CODE": 3 ,
				"ACTION": "KEYPRESS"
			}]
		}
		url = f"https://{self.options['ip']}:7345/key_command/"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return
		# {"STATUS": {"RESULT": "SUCCESS", "DETAIL": "Success"}, "URI": "/key_command/"}
		result = json.loads( response.text )
		#pprint( result )
		return result

	def mute_toggle( self ):
		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": "/key_command/" ,
			"KEYLIST": [{
				"CODESET": 5 ,
				"CODE": 4 ,
				"ACTION": "KEYPRESS"
			}]
		}
		url = f"https://{self.options['ip']}:7345/key_command/"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return
		# {"STATUS": {"RESULT": "SUCCESS", "DETAIL": "Success"}, "URI": "/key_command/"}
		result = json.loads( response.text )
		#pprint( result )
		return result

	def get_current_input( self ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/dynamic/tv_settings/devices/current_input"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()

		# Should Return
		# {'HASHLIST': [1209501159, 1519436522],
		#  'ITEMS': [{'CNAME': 'current_input',
		#             'ENABLED': 'FALSE',
		#             'HASHVAL': 2690294191,
		#             'HIDDEN': 'TRUE',
		#             'NAME': 'Current Input',
		#             'TYPE': 'T_STRING_V1',
		#             'VALUE': 'hdmi2'}],
		#  'PARAMETERS': {'FLAT': 'TRUE', 'HASHONLY': 'FALSE', 'HELPTEXT': 'FALSE'},
		#  'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'},
		#  'URI': '/menu_native/dynamic/tv_settings/devices/current_input'}
		result = json.loads( response.text )
		#pprint( result )
		return { "name": result["ITEMS"][0]["VALUE"] , "hash_value": result["ITEMS"][0]["HASHVAL"] }

	def get_available_inputs( self ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/dynamic/tv_settings/devices/name_input"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()
		result = json.loads( response.text )
		# pprint( result )
		inputs = [ { "name": x["NAME"] , "hash_value": x["HASHVAL"] } for x in result["ITEMS"] ]
		return inputs

	def set_input( self , input_name ):

		# For this one, you first need the hash value of the current input id
		current_input = self.get_current_input()

		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": "/menu_native/dynamic/tv_settings/devices/current_input" ,
			"item_name": "CURRENT_INPUT" ,
			"VALUE": input_name ,
			"HASHVAL": current_input["hash_value"] ,
			"REQUEST": "MODIFY"
		}
		url = f"https://{self.options['ip']}:7345/menu_native/dynamic/tv_settings/devices/current_input"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return

		result = json.loads( response.text )
		#pprint( result )
		return result

	def cycle_input( self ):
		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": "/key_command/" ,
			"KEYLIST": [{
				"CODESET": 7 ,
				"CODE": 1 ,
				"ACTION": "KEYPRESS"
			}]
		}
		url = f"https://{self.options['ip']}:7345/key_command/"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return
		# {"STATUS": {"RESULT": "SUCCESS", "DETAIL": "Success"}, "URI": "/key_command/"}
		result = json.loads( response.text )
		#pprint( result )
		return result

	def get_audio_settings( self ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/dynamic/tv_settings/audio"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()
		result = json.loads( response.text )
		#pprint( result )
		return result

	def get_audio_setting( self , audio_setting ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/dynamic/tv_settings/audio/{audio_setting}"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()

		# Should Return
		# {'HASHLIST': [3552915159, 3436748430],
		#  'ITEMS': [{'CNAME': 'tv_speakers',
		#             'HASHVAL': 4126758801,
		#             'INDEX': 0,
		#             'NAME': 'Speakers',
		#             'TYPE': 'T_LIST_V1',
		#             'VALUE': 'Auto'}],
		#  'PARAMETERS': {'FLAT': 'TRUE', 'HASHONLY': 'FALSE', 'HELPTEXT': 'FALSE'},
		#  'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'},
		#  'URI': '/menu_native/dynamic/tv_settings/audio/tv_speakers'}
		result = json.loads( response.text )
		#pprint( result )
		return { "setting": result["ITEMS"][0]["VALUE"] , "hash_value": result["ITEMS"][0]["HASHVAL"] }

	def get_all_audio_settings_options( self ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/static/tv_settings/audio"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()

		# Should Return
		result = json.loads( response.text )
		#pprint( result )
		return result

	def get_audio_settings_options( self , audio_setting_option ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/static/tv_settings/audio/{audio_setting_option}"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()

		# Should Return
		# {'HASHVAL': 1234567890,
		#  'ITEMS': [{'CNAME': 'tv_speakers',
		#             'ELEMENTS': ['Auto', 'On', 'Off'],
		#             'GROUP': 'G_AUDIO',
		#             'NAME': 'Speakers',
		#             'TYPE': 'T_LIST_V1'}],
		#  'PARAMETERS': {'FLAT': 'TRUE', 'HASHONLY': 'FALSE', 'HELPTEXT': 'FALSE'},
		#  'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'},
		#  'URI': '/menu_native/static/tv_settings/audio/tv_speakers'}
		result = json.loads( response.text )
		#pprint( result )
		return result

	def set_audio_setting( self , audio_setting , audio_setting_option ):

		# For this one, you first need the hash value of the current audio setting
		current_settings = self.get_audio_setting( audio_setting )

		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": f"/menu_native/dynamic/tv_settings/audio/{audio_setting}" ,
			"item_name": "SETTINGS" ,
			"VALUE": audio_setting_option ,
			"HASHVAL": current_settings["hash_value"] ,
			"REQUEST": "MODIFY"
		}
		url = f"https://{self.options['ip']}:7345/menu_native/dynamic/tv_settings/audio/{audio_setting}"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return
		# {'HASHLIST': [3552915159, 3436748430],
		#  'ITEMS': [{'HASHVAL': 2210383572, 'NAME': 'Mute'}],
		#  'PARAMETERS': {'HASHVAL': 1580137992, 'REQUEST': 'MODIFY', 'VALUE': 'Off'},
		#  'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'}
		result = json.loads( response.text )
		#pprint( result )
		return result

	def get_settings_types( self ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/dynamic/tv_settings"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()

		# Should Return
		result = json.loads( response.text )
		# pprint( result )
		return result

	def get_all_settings_for_type( self , setting_type ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/dynamic/tv_settings/{setting_type}"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()

		# Should Return
		result = json.loads( response.text )
		#pprint( result )
		return result

	def get_setting( self , setting_type , setting_name ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/dynamic/tv_settings/{setting_type}/{setting_name}"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()

		# Should Return
		# {'HASHLIST': [2880302639, 3367486168],
		#  'ITEMS': [{'CNAME': 'backlight',
		#             'HASHVAL': 1656752721,
		#             'NAME': 'Backlight',
		#             'TYPE': 'T_VALUE_V1',
		#             'VALUE': 100}],
		#  'PARAMETERS': {'FLAT': 'TRUE', 'HASHONLY': 'FALSE', 'HELPTEXT': 'FALSE'},
		#  'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'},
		#  'URI': '/menu_native/dynamic/tv_settings/picture/backlight'}
		result = json.loads( response.text )
		#pprint( result )
		return result

	def get_all_settings_options_for_type( self , settings_type ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/static/tv_settings/{settings_type}"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()

		# Should Return
		result = json.loads( response.text )
		#pprint( result )
		return result


	def get_settings_option( self , settings_type , setting_name ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/menu_native/static/tv_settings/{settings_type}/{setting_name}"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()

		# Should Return
		# {'HASHVAL': 1234567890,
		#  'ITEMS': [{'CNAME': 'backlight',
		#             'GROUP': 'G_PICTURE',
		#             'INCREMENT': 1,
		#             'MAXIMUM': 100,
		#             'MINIMUM': 0,
		#             'NAME': 'Backlight',
		#             'TYPE': 'T_VALUE_V1'}],
		#  'PARAMETERS': {'FLAT': 'TRUE', 'HASHONLY': 'FALSE', 'HELPTEXT': 'FALSE'},
		#  'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'},
		result = json.loads( response.text )
		#pprint( result )
		return result

	def set_settings_option( self , settings_type , setting_name , settings_option ):

		# For this one, you first need the hash value of the current setting
		current_setting = self.get_setting( settings_type , setting_name )

		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": f"/menu_native/dynamic/tv_settings/{settings_type}/{setting_name}" ,
			"item_name": "SETTINGS" ,
			"VALUE": int( settings_option ) ,
			"HASHVAL": current_setting["ITEMS"][0]["HASHVAL"] ,
			"REQUEST": "MODIFY"
		}
		url = f"https://{self.options['ip']}:7345/menu_native/dynamic/tv_settings/{settings_type}/{setting_name}"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()

		# Should Return
		# {'HASHLIST': [791350083, 2564833227],
		#  'ITEMS': [{'HASHVAL': 2398756231, 'NAME': 'Backlight'}],
		#  'PARAMETERS': {'HASHVAL': 1656752721, 'REQUEST': 'MODIFY', 'VALUE': 90},
		#  'STATUS': {'DETAIL': 'Success', 'RESULT': 'SUCCESS'},
		result = json.loads( response.text )
		#pprint( result )
		return result

	# Look Here to Find APP_ID 's , Namespace Integers , and Messages
	# https://github.com/vkorn/pyvizio/blob/master/pyvizio/const.py
	def launch_app_config( self , app_id , name_space , message="None" ):
		headers = {
			"Content-Type": "application/json" ,
			"AUTH": self.options["access_token"]
		}
		data = {
			"_url": "/app/launch",
			"VALUE": {
				"APP_ID": str( app_id ) ,
				"NAME_SPACE": int( name_space ) ,
				"MESSAGE": message
			}
		}
		url = f"https://{self.options['ip']}:7345/app/launch"
		response = requests.put( url , headers=headers , data=json.dumps( data ) , verify=False )
		response.raise_for_status()
		#print( response.text )
		result = json.loads( response.text )
		return result

	def get_current_app( self ):
		headers = {
			'AUTH': self.options["access_token"]
		}
		url = f"https://{self.options['ip']}:7345/app/current"
		response = requests.get( url , headers=headers , verify=False )
		response.raise_for_status()
		result = json.loads( response.text )
		# Should Return
		# {"STATUS": {"RESULT": "SUCCESS", "DETAIL": "Success"}
		#pprint( result )
		return result