#!/usr/bin/env python3

import requests
import json
import base64

import logging

import sys, getopt

#from . import __version__

from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient



def main():
    argv = sys.argv[1:]
    #log.debug('inforion ' + __version__)
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('inforion -i InforIONFile -url url -methode')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('inforion -i InforIONFile -url url -methode')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print ('Input file is "', inputfile)
    print ('Output file is "', outputfile)

if __name__ == "__main__":
    #sys.exit(run("-h"))
    main()

