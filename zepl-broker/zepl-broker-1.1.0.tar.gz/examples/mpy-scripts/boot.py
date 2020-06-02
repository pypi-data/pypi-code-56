# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
from wifi_util import *
wifi = do_connect()
import webrepl
webrepl.start()
