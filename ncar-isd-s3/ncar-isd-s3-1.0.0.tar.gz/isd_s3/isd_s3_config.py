#!/usr/bin/env python3

RDA_BASE = '/glade/u/home/rdadata'

logging = {
   'logpath': RDA_BASE+'/dssdb/log',
   'logfile': 'isd-s3.log',
   'dbgfile': 'isd-s3.dbg',
   'loglevel': 'info',
   'maxbytes': 2000000,
   'backupcount': 1,
   'logfmt': '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s',
   'dbgfmt': '%(asctime)s - %(name)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'
}