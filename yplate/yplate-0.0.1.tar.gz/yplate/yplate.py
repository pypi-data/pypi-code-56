import argparse
from yplate.ops import model_config,display_top

version = '0.0.1'

def main():
	parser = argparse.ArgumentParser(description="Detect car/vehicle number plates. This is a dev version and it doesn't detect anything for now")
	subparser = parser.add_subparsers(title="commands", dest="command")

	#Version
	parser.add_argument('-v', action='version', version=version)

	""" Model Configuration """
	### 3. Model config
	parser.add_argument('--config',action='store_const', const=lambda:'model_config', dest='cmd')

	try:
		args = parser.parse_args()

		if(args.cmd() == 'model_config'):
			## Display Model Config
			display_top()
			model_config()
			exit()
			

	except Exception as e:
		display_top()
		print("Command not found. Check the input commands again.\n For more info type 'yplate -h'")
		exit()

if __name__ == '__main__':
	main()
