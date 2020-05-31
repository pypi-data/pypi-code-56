import sys
import os
import subprocess
import socket
import netifaces
import platform

class Discover:

	def __init__( self , options={} ):
		self.options = options
		self.map = {}

	def find_tv( self ):
		self.platform = platform.system()
		self.get_interfaces()
		self.get_gateways()
		self.nmap_all_gateways()
		self.arp_all_interfaces()
		return self.get_ip_from_mac_address( self.options["mac_address"] )

	def get_interfaces( self ):
		interfaces = netifaces.interfaces()
		print( interfaces )
		self.map[ "interfaces" ] = {}
		for index , interface in enumerate( interfaces ):
			self.map[ "interfaces" ][ str( interface ) ] = {}

	def get_gateways( self ):
		gateways = netifaces.gateways()
		print( gateways )
		for index , gateway in enumerate( gateways ):
			for index_item , item in enumerate( gateways[ gateway ] ):
				if isinstance( item , tuple ):
					if item[ 1 ] in self.map[ "interfaces" ]:
						self.map[ "interfaces" ][ str( item[ 1 ] ) ][ "gateway_ip" ] = item[ 0 ]
						self.map[ "interfaces" ][ str( item[ 1 ] ) ][ "ips" ] = {}

	def nmap_all_gateways( self ):
		# AKA a Network "Probe"
		shell_command = [ "nmap" ]
		if self.platform == "Linux":
			shell_command.append( "-sn" )
		elif self.platform == "Darwin":
			shell_command.append( "-sP" )
		if self.platform == "Windows":
			sys.exit( 1 )
		for index , interface in enumerate( self.map[ "interfaces"] ):
			if "gateway_ip" in self.map[ "interfaces" ][ interface ]:
				#print( "Maping " + interface )
				shell_command.append( self.map[ "interfaces" ][ interface ][ "gateway_ip" ] + "/24" )
				#print( result.returncode, result.stdout, result.stderr )
				result = subprocess.run( shell_command , capture_output=True , universal_newlines=True )

	def arp_all_interfaces( self ):
		if self.platform == "Windows":
			sys.exit( 1 )
		for index , interface in enumerate( self.map[ "interfaces"] ):
			if "gateway_ip" in self.map[ "interfaces" ][ interface ]:
				print( f'Searching: {interface} : {self.map[ "interfaces" ][ interface ][ "gateway_ip" ]}' )
				shell_command = [ "arp" , "-na" , "-i" , interface ]
				result = subprocess.run( shell_command , capture_output=True , universal_newlines=True )
				lines = result.stdout.split( "\n" )
				for index , line in enumerate( lines ):
					#print( str( index ) + " === " + line )
					if "incomplete" in line:
						continue
					if len( line ) < 3:
						continue
					mac_address = line.split( "at " )
					if len( mac_address ) < 1:
						continue
					mac_address = mac_address[ 1 ].split( " on" )
					if ( len( mac_address ) < 1 ):
						continue
					line_interface = mac_address[ 1 ].strip()
					mac_address = mac_address[ 0 ].strip()
					mac_address = mac_address.split( " " )[ 0 ]
					line_interface = line_interface.split( " ifscope" )
					if len( line_interface ) < 1:
						continue
					line_interface = line_interface[ 0 ]
					ip = line[ line.find( "(" ) + 1 : line.find( ")" ) ]
					self.map[ "interfaces" ][ line_interface ][ "ips" ][ ip ] = { "mac_address": mac_address }

	def get_ip_from_mac_address( self , mac_address ):
		for index , interface in enumerate( self.map[ "interfaces"] ):
			if "ips" in self.map[ "interfaces" ][ interface ]:
				for index_ip , ip in enumerate( self.map[ "interfaces" ][ interface ][ "ips" ] ):
					if "mac_address" in self.map[ "interfaces" ][ interface ][ "ips" ][ ip ]:
						if mac_address == self.map[ "interfaces" ][ interface ][ "ips" ][ ip ][ "mac_address" ]:
							return ip