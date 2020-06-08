import time
from subprocess import getoutput , Popen , PIPE , STDOUT
from XDoToolWrapper import XDoToolWrapper

class ChromeWrapper:

	def __init__( self , options={} ):
		self.options = options
		if "window_name" not in self.options:
			self.options["window_name"] = "Chrome"

	def exec( self , bash_command ):
		p = Popen(
			bash_command ,
			cwd="/home/morphs" ,
			stdout=PIPE ,
			stderr=STDOUT
			)

	def exec2( self , bash_command ):
		return getoutput( bash_command )

	def stop( self ):
		return self.exec2( "pkill -9 chrome" )

	def open( self , url ):
		pass

	def open_in_kiosk_mode( self , url ):
		self.stop()
		command = [ "/usr/bin/google-chrome-stable" , "--password-store=basic" , "--enable-extensions" , f"--app={url}" ]
		print( command )
		self.exec( command )
		self.xdotool = None
		self.xdotool = XDoToolWrapper()
		self.xdotool.attach_via_name( self.options["window_name"] )

	def fullscreen( self ):
		self.xdotool.maximize_window()
