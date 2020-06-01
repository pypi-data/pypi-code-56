#!python


'''
Lucas J. Koerner, koerner.lucas@stthomas.edu
2020/05/23 
Python code to read the sensor data from the 
Silicon Labs Thunderboard Sense2

command-line input parameters:
	--time [seconds]
	--sensor 

outputs: 
	CSV of all sensor data
	plot of all specific sensor

v0.1 : inital version
'''
import serial
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
import appnope
import glob 
import pandas as pd
import platform
import sys
import argparse


if __name__ == '__main__':

	now = datetime.datetime.now() # current date and time for saving files 
	date_time = now.strftime("%Y_%m_%d_%H_%M_%S")

	os_platform = platform.system()
	appnope.nope()
	plt.style.use('ggplot')

	# temporary sensor keys for input arguments (no spaces)
	sensor_keys = ['TVOC', 'Pressure', 'SoundLevel', 'AmbLight', 
			  	  'eCO2', 'HALL', 'Temp', 'Humidity', 'UVIndex']
	sensor_list = ', '.join(sensor_keys)

	parser = argparse.ArgumentParser()
	parser.add_argument("--time", 
						help="The time for data collection in seconds", 
						default = 10)
	parser.add_argument("--sensor", 
						help="The name of the sensor to plot and display (can be all)\nOptions are: {}".format(sensor_list), 
						default = 'Humidity')
	args = parser.parse_args()
	run_time = float(args.time) # seconds [TODO: input]
	sensor_to_display = str(args.sensor) # 'Humidity' # [TODO: input]

	if sensor_to_display == 'AmbLight':
		sensor_to_display = 'Amb light'
	if sensor_to_display == 'UVIndex':
		sensor_to_display = 'UV Index'

	# fix sensor keys to match the strings from the Thunderboard
	sensor_keys = ['TVOC', 'Pressure', 'SoundLevel', 'Amb light', 
			  	  'eCO2', 'HALL', 'Temp', 'Humidity', 'UV Index']

	def TimestampMillisec64():
	    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000) 

	# serial parameters and serial opening
	baudrate = 115200

	import serial.tools.list_ports
	ports = list(serial.tools.list_ports.comports())
	try:
		ser_addr = [x for x in ports if x[1]=='J-Link OB'][0][0]
	except IndexError:
		print('No serial address found.\n Is the thunderboard connected using USB?') 
		if os_platform in ['Darwin', 'Linux']:
			print('Check for /dev/tty.usbmodem by $ ls /dev/tty.*')	
		elif os_platform in ['Windows']:
			print('Check for COM in Device Manager')
		sys.exit(1) 	

	'''
	if os_platform == 'Darwin':  # MAC 
		print("Found these devices: " + glob.glob("/dev/tty.usbmodem*")[0])
		ser_addr = glob.glob("/dev/tty.usbmodem*")[0]
	elif os_platform == 'Windows':
		print("Found these devices: " + glob.glob("/dev/tty.usbmodem*")[0])
		ser_addr = glob.glob("/dev/tty.usbmodem*")[0]
	elif os_platform == 'Linux':
		print("Found these devices: " + glob.glob("/dev/tty.usbmodem*")[0])
		ser_addr = glob.glob("/dev/tty.usbmodem*")[0]
	'''

	ser = serial.Serial(ser_addr, baudrate = baudrate, timeout = 2)
	ser.is_open
	time.sleep(0.15)

	results = {}
	for k in sensor_keys:
		results[k] = {}
		results[k]['value'] = np.array([])
		results[k]['time'] = np.array([])
		results[k]['units'] = np.array([])

	# flush serial buffer
	ser.read(ser.in_waiting)
	t_junk = ser.readline()

	t_start = TimestampMillisec64()
	elapsed_time = (TimestampMillisec64() - t_start)/1000

	while(elapsed_time < run_time):
		t = str(ser.readline())
		if len(t) == 3:
			print('Serial read timeout. \n Is the bluetooth app connected and diplaying Environmental data?')
			sys.exit(2)		
		
		elapsed_time = (TimestampMillisec64() - t_start) / 1000

		for k in sensor_keys:
			if k in t:
				if k == 'UV Index':
					results[k]['value'] = np.append(results[k]['value'], 
													float(t.split('=')[1].split(' ')[1].replace("\\r\\n'",'')))
					results[k]['units'] = np.append(results[k]['units'], 'index')
				else:
					results[k]['value'] = np.append(results[k]['value'], 
													float(t.split('=')[1].split(' ')[1]))
					# fix units for TVOC and eCO2
					if k == 'eCO2':
						results[k]['units'] = np.append(results[k]['units'], 'ppm')
					elif k == 'TVOC':
						results[k]['units'] = np.append(results[k]['units'], 'ppb')
					else:
						results[k]['units'] = np.append(results[k]['units'], 
													t.split('=')[1].split(' ')[2].replace("\\r\\n'",''))

				results[k]['time'] = np.append(results[k]['time'], elapsed_time)
				if ((k == sensor_to_display) or (sensor_to_display == 'all')):
					print('At {:2.2f} [s] Measured {} sensor: {:4.2f} {}'.format(elapsed_time, 
						k, results[k]['value'][-1], results[k]['units'][-1]))

	# close serial port
	ser.close()

	# plot and save data
	if sensor_to_display == 'all':
		fig, axs = plt.subplots(3,3, figsize = (10, 10))
		sensors_to_plot = sensor_keys
		for idx,k in enumerate(sensors_to_plot):
			axs[int(idx/3)][idx % 3].plot(results[k]['time'], 
					results[k]['value'], marker='x', label = k)
			axs[int(idx/3)][idx % 3].legend() 
			axs[int(idx/3)][idx % 3].set_ylabel(results[k]['units'][-1])
			axs[int(idx/3)][idx % 3].set_xlabel('Time [s]')

	else:
		sensors_to_plot = [sensor_to_display]
		fig, axs = plt.subplots(figsize = (10, 10))
		for idx,k in enumerate(sensors_to_plot):
			axs.plot(results[k]['time'], 
						results[k]['value'], marker='x', label = k)
			axs.set_ylabel(results[k]['units'][-1])
		axs.set_xlabel('Time [s]')
		axs.legend() 


	fig.tight_layout()
	fig.savefig('measured_{}_{}.png'.format(sensor_to_display, date_time))
	# blocking show
	plt.ioff()
	plt.show()
				
	# https://stackoverflow.com/questions/13575090/construct-pandas-dataframe-from-items-in-nested-dictionary
	# save dictionary to CSV file by first converting to a pandas dataframe
	df = pd.DataFrame.from_dict({i + '_' + j: results[i][j] 
	                           for i in results.keys() 
	                           for j in results[i].keys()},
	                       orient='index')
	df = df.transpose()
	df.to_csv('data_{}.csv'.format(date_time), index=False)
