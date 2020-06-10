import telnetlib
import time
from pprint import pprint

# Based on https://github.com/DerMitch/py-vlcclient

# https://n0tablog.wordpress.com/2009/02/09/controlling-vlc-via-rc-remote-control-interface-using-a-unix-domain-socket-and-no-programming/

class VLCController:

	def __init__( self , options={} ):
		self.options = options
		if "server_ip" not in self.options:
			self.options["server_ip"] = "127.0.0.1"
		if "port" not in self.options:
			self.options["port"] = 4212
		if "password" not in self.options:
			self.options["password"] = "admin"
		if "timeout" not in self.options:
			self.options["timeout"] = 5

		self.connected = False
		self.connect()

	def connect( self ):
		try:
			self.telnet = telnetlib.Telnet()
			self.telnet.open( self.options["server_ip"] , self.options["port"] , self.options["timeout"] )

			# Parse version
			connection_result = self.telnet.expect([
				r"VLC media player ([\d.]+)".encode( "utf-8" )
			])
			self.server_version = connection_result[ 1 ].group( 1 )
			self.server_version_tuple = self.server_version.decode( "utf-8" ).split( '.' )

			# Login
			self.telnet.read_until( "Password: ".encode( "utf-8" ) )
			self.telnet.write( self.options["password"].encode( "utf-8" ) )
			self.telnet.write( "\n".encode( "utf-8" ) )

			# Password correct?
			login_result = self.telnet.expect([
				"Password: ".encode( "utf-8" ) ,
				">".encode( "utf-8" )
			])
			if "Password".encode( "utf-8" ) in login_result[ 2 ]:
				raise WrongPasswordError()

			self.connected = True
		except Exception as e:
			print( e )

	def disconnect( self ):
		try:
			self.telnet.close()
			self.telnet = None
			self.connected = False
		except Exception as e:
			print( e )

	def send_command( self , command ):
		try:
			self.telnet.write( ( command + "\n" ).encode( "utf-8" ) )
			result = self.telnet.read_until( ">".encode( "utf-8" ) )[ 1:-3 ]
			result = result.decode( "utf-8" )
			return result
		except Exception as e:
			print( e )
			return False

	def raw( self , *args ):
		try:
			return self.send_command( " ".join( args ) )
		except Exception as e:
			print( e )
			return False

	def help( self ):
		try:
			return self.send_command( "help" )
		except Exception as e:
			print( e )
			return False

	def status( self ):
		try:
			result = self.send_command( "status" )
			if result == False:
				return result
			status = result.split( "\n" )
			final_status = {}
			for index , line in enumerate( status ):
				if line.find( "new input:" ) > -1:
					final_status["file_path"] = line.split( "new input: " )[ 1 ].strip()[ :-2 ]
				elif line.find( "volume:" ) > -1:
					final_status["volume"] = line.split( "volume: " )[ 1 ].strip()[ :-2 ]
				elif line.find( "state" ) > -1:
					final_status["state"] = line.split( "state " )[ 1 ].strip()[ :-2 ]
			return final_status
		except Exception as e:
			print( e )
			return False

	def info( self ):
		try:
			result = self.send_command( "info" )
			if result == False:
				return result
			info = result.split( "\n" )
			final_stats = {}
			for index , line in enumerate( info ):
				if line.find( "DURATION:" ) > -1:
					final_stats["duration"] = line.split( "DURATION: " )[ 1 ].strip()
				elif line.find( "title:" ) > -1:
					final_stats["title"] = line.split( "title: " )[ 1 ].strip()
				elif line.find( "showName:" ) > -1:
					final_stats["show_name"] = line.split( "showName: " )[ 1 ].strip()
				elif line.find( "seasonNumber:" ) > -1:
					final_stats["season_number"] = line.split( "seasonNumber: " )[ 1 ].strip()
				elif line.find( "episodeNumber:" ) > -1:
					final_stats["episode_number:"] = line.split( "episodeNumber: " )[ 1 ].strip()
				elif line.find( "filename:" ) > -1:
					final_stats["filename"] = line.split( "filename: " )[ 1 ].strip()
			return final_stats
		except Exception as e:
			print( e )
			return False

	def get_time( self ):
		try:
			return self.send_command( "get_time" )
		except Exception as e:
			print( e )
			return False

	def get_common_info( self ):
		try:
			current_time = self.get_time()
			status = self.status()
			info = self.info()
			duration = self.run_command( "get_length" )
			return { **status , **info , "current_time": current_time , "duration": duration }
		except Exception as e:
			print( e )
			return False

	def stats( self ):
		try:
			return self.send_command( "stats" )
		except Exception as e:
			print( e )
			return False

	def fullscreen_on( self ):
		try:
			return self.send_command( "fullscreen on" )
		except Exception as e:
			print( e )
			return False

	def fullscreen_off( self ):
		try:
			return self.send_command( "fullscreen on" )
		except Exception as e:
			print( e )
			return False

	def volume_get( self ):
		try:
			return self.send_command( "volume" ).strip()
		except Exception as e:
			print( e )
			return False

	def volume_set( self , volume_level ):
		try:
			return self.send_command( f"volume {volume_level}" )
		except Exception as e:
			print( e )
			return False

	def volume_up( self , steps=1 ):
		try:
			return self.send_command( f"volup {steps}" )
		except Exception as e:
			print( e )
			return False

	def volume_down( self , steps=1 ):
		try:
			return self.send_command( f"voldown {steps}" )
		except Exception as e:
			print( e )
			return False

	def add( self , file_path ):
		try:
			return self.send_command( f"add {file_path}" )
		except Exception as e:
			print( e )
			return False

	def enqueue( self , file_path ):
		try:
			return self.send_command( f"enqueue {file_path}" )
		except Exception as e:
			print( e )
			return False

	def seek( self , seconds=1 ):
		try:
			return self.send_command( f"seek {seconds}" )
		except Exception as e:
			print( e )
			return False

	def play( self ):
		try:
			return self.send_command( "play" )
		except Exception as e:
			print( e )
			return False

	def pause( self ):
		try:
			return self.send_command( "pause" )
		except Exception as e:
			print( e )
			return False

	def stop( self ):
		try:
			return self.send_command( "stop" )
		except Exception as e:
			print( e )
			return False

	def rewind( self ):
		try:
			return self.send_command( "rewind" )
		except Exception as e:
			print( e )
			return False

	def next( self ):
		try:
			return self.send_command( "next" )
		except Exception as e:
			print( e )
			return False

	def previous( self ):
		try:
			return self.send_command( "previous" )
		except Exception as e:
			print( e )
			return False

	def clear( self ):
		try:
			return self.send_command( "clear" )
		except Exception as e:
			print( e )
			return False

	def loop( self ):
		try:
			return self.send_command( "loop" )
		except Exception as e:
			print( e )
			return False

	def repeat( self ):
		try:
			return self.send_command( "repeat" )
		except Exception as e:
			print( e )
			return False

	def random( self ):
		try:
			return self.send_command( "random" )
		except Exception as e:
			print( e )
			return False