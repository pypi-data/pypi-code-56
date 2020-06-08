import os
import time
from subprocess import call , getoutput , Popen , PIPE , STDOUT
from XDoToolWrapper import XDoToolWrapper

class ChromeWrapper:

	def __init__( self , options={} ):
		self.options = options
		if "window_name" not in self.options:
			self.options["window_name"] = "Chrome"
		if "number_of_tries" not in self.options:
			self.options["number_of_tries"] = 20

	def exec_string( self , bash_command_string ):
		p = Popen(
			bash_command_string ,
			cwd=os.getcwd() ,
			stdout=PIPE ,
			stderr=STDOUT ,
			shell=True
			)

	def exec_array( self , bash_command_array ):
		p = Popen(
			bash_command_array ,
			cwd=os.getcwd() ,
			stdout=PIPE ,
			stderr=STDOUT ,
			shell=False
			)

	def exec2( self , bash_command ):
		return getoutput( bash_command )

	def exec3( self , bash_command ):
		return call( bash_command , shell=True )

	def stop( self ):
		self.exec2( "pkill -9 chrome" )
		time.sleep( 1 )
		return

	def open( self , url ):
		pass

	def open_in_kiosk_mode( self , url ):
		self.stop()
		#command = [ "/usr/bin/google-chrome-stable" , "--password-store=basic" , "--enable-extensions" , f"--app={url}" ]
		command = [ "/usr/bin/google-chrome-stable" , "--password-store=basic" , f"--app={url}" ]
		if "extension_paths" in self.options:
			for index , path in enumerate( self.options["extension_paths"] ):
				#command.append( f'--load-extension="{path}"' )
				command.append( '--load-extension' )
				command.append( path )
		#print( command )
		#self.exec( command )
		combined = " ".join( command )
		print( combined )
		self.exec_string( combined )
		self.xdotool = None
		self.xdotool = XDoToolWrapper()
		self.xdotool.attach_via_name( self.options["window_name"] , self.options["number_of_tries"] )

	def fullscreen( self ):
		self.xdotool.maximize_window()
