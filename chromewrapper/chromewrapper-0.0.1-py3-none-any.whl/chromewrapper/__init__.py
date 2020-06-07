import time
from subprocess import getoutput , Popen , PIPE , STDOUT
from XDoToolWrapper import XDoToolWrapper

class ChromeWrapper:

	def __init__( self , options={} ):
		self.options = options

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
		return self.exec2( "sudo pkill -9 chrome" )

	def open( self , url ):
		pass

	def open_in_kiosk_mode( self , url ):
		self.stop()
		#command = f"/usr/bin/google-chrome-stable --password-store=basic --enable-extensions --app={ url } &"
		command = [ "/usr/bin/google-chrome-stable" , "--password-store=basic" , "--enable-extensions" , f"--app={url}" ]
		print( command )
		self.exec( command )
		self.xdotool = None
		self.xdotool = XDoToolWrapper()
		self.xdotool.attach_via_name( "Disney+ | Video Player" )

	def fullscreen( self ):
		self.xdotool.maximize_window()
