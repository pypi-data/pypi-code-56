#!/usr/bin/env python3

# Based on https://github.com/vkorn/pyvizio

import discover
import api
from pprint import pprint

class VizioController:

	def __init__( self , options={} ):
		self.options = options
		if "mac_address" not in options:
			print("you have to send the mac adress of the tv")
			sys.exit( 1 )
		if "ip" not in options:
			self.discover = discover.Discover( options )
			self.ip = self.discover.find_tv()
			options["ip"] = self.ip
		else:
			self.ip = options["ip"]
		if "request_token" in options:
			if "code_displayed_on_tv" in options:
				self.api = api.API(options)
				options["access_token"] = self.api.pairing_stage_2( self.ip , options["request_token"] , options["code_displayed_on_tv"] )
		if "access_token" not in options:
			self.api = api.API(options)
			request_token = self.api.pairing_stage_1( self.ip )
			print( f"Ok , now rerun this and set options['request_token']: {request_token}" )
			print( f"and options['code_displayed_on_tv']: code on tv" )
			sys.exit( 1 )

		self.api = api.API( options )
		print( "Retrieving Current Settings" )
		self.current_volume = self.api.get_volume()
		self.audio_settings = self.api.get_audio_settings()
		self.audio_settings_options = self.api.get_all_audio_settings_options()
		self.current_input = self.api.get_current_input()
		self.available_inputs = self.api.get_available_inputs()
		self.current_app = self.api.get_current_app()
		self.settings_types = self.api.get_settings_types()
		self.settings = {}
		for index , setting in enumerate( self.settings_types["ITEMS"] ):
			options = self.api.get_all_settings_for_type( setting["CNAME"] )
			options = [ x["CNAME"] for x in options["ITEMS"] ]
			self.settings[setting["CNAME"]] = {}
			for option_index , option in enumerate( options ):
				self.settings[setting["CNAME"]][ option ] = self.api.get_setting( setting["CNAME"] , option )
		pprint( self.settings )


if __name__ == "__main__":
	tv = VizioController({
			"name": "Loft TV" ,
			"mac_address": "2c:64:1f:25:6b:3c" ,
			"ip": "192.168.1.100" ,
			"access_token": "Zhehzvszfq"
		})
	#print( tv.ip )

	#current_volume = tv.api.get_volume()
	#tv.api.volume_up()
	#tv.api.volume_down()
	#audio_settings = tv.api.get_audio_settings()
	#tv_speakers = tv.api.get_audio_setting( "tv_speakers" )
	#all_audio_settings_options = tv.api.get_all_audio_settings_options()
	#tv_speakers = tv.api.get_audio_settings_options( "tv_speakers" )
	#tv.api.set_audio_setting( "mute" , "Off" )

	#current_input = tv.api.get_current_input()
	#available_inputs = tv.api.get_available_inputs()
	# tv.api.set_input( "HDMI-1" )
	# tv.api.set_input( "HDMI-2" )
	#tv.api.cycle_input()

	#settings_types = tv.api.get_settings_types()
	#audio_settings = tv.api.get_all_settings_for_type( "audio" )
	#backlight = tv.api.get_setting( "picture" , "backlight" )
	#picture_settings = tv.api.get_all_settings_options_for_type( "picture" )
	#backlight_setting = tv.api.get_settings_option( "picture" , "backlight" )
	#tv.api.set_settings_option( "picture" , "backlight" , 100 )

	#tv.api.launch_app_config( "1" , 3 )
	#current_app = tv.api.get_current_app()

	# Whenever this is done, post it here:
	# https://github.com/vkorn/pyvizio/issues/5