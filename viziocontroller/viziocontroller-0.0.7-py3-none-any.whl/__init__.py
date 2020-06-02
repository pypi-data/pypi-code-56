#!/usr/bin/env python3

# Based on https://github.com/vkorn/pyvizio

from .discover import Discover
from .api import API
from pprint import pprint
import sys

class VizioController:

	def __init__( self , options={} ):
		self.options = options
		if "mac_address" not in options:
			print("you have to send the mac adress of the tv")
			sys.exit( 1 )
		if "ip" not in options:
			self.discover = Discover( options )
			self.ip = self.discover.find_tv()
			options["ip"] = self.ip
			print( "IP == " )
			print( options["ip"] )
		else:
			self.ip = options["ip"]
		if "request_token" in options:
			if "code_displayed_on_tv" in options:
				self.api = API(options)
				options["access_token"] = self.api.pairing_stage_2( self.ip , options["request_token"] , options["code_displayed_on_tv"] )
				print( "access_token == " )
				print( str( options["access_token"] ) )
				sys.exit( 1 )
		if "access_token" not in options:
			self.api = API(options)
			request_token = self.api.pairing_stage_1( self.ip )
			print( "request_token ==" )
			print( str( request_token ) )
			print( f"Ok , now rerun this and set request_token and code_displayed_on_tv" )
			sys.exit( 1 )

		self.api = API( options )
		# print( "Retrieving Current Settings" )
		# self.current_volume = self.api.get_volume()
		# self.audio_settings = self.api.get_audio_settings()
		# self.audio_settings_options = self.api.get_all_audio_settings_options()
		# self.current_input = self.api.get_current_input()
		# self.available_inputs = self.api.get_available_inputs()
		# self.current_app = self.api.get_current_app()
		# self.settings_types = self.api.get_settings_types()
		# self.settings = {}
		# for index , setting in enumerate( self.settings_types["ITEMS"] ):
		# 	options = self.api.get_all_settings_for_type( setting["CNAME"] )
		# 	options = [ x["CNAME"] for x in options["ITEMS"] ]
		# 	self.settings[setting["CNAME"]] = {}
		# 	for option_index , option in enumerate( options ):
		# 		self.settings[setting["CNAME"]][ option ] = self.api.get_setting( setting["CNAME"] , option )
		# pprint( self.settings )
		print( f"IP == {self.ip}" )