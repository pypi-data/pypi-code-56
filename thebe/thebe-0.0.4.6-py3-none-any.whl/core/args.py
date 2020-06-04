import argparse

#Parse commandline argument
parser = argparse.ArgumentParser(description='Display python information live in browser.')
parser.add_argument('file', metavar='F', help='python file to run')
parser.add_argument('--port', '-p', default='5000', metavar='P', help='port number')
parser.add_argument('--debug', '-d', action='store_true', help='enable logging')
args = parser.parse_args()

def getDebug():
    return args.debug

def getFile():
    return args.file

def getPort():
    return int(args.port)
