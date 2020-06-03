import pprint
import os
import sys

try:
    import pyfiglet
except ImportError:
    os.system('cmd /k "pip install pyfiglet"')

def Add(x, y):
   r = x + y
   return r

def Minus(x, y):
   r = x - y
   return r

def Times(x, y):
   r = x * y
   return r

def Divide(x, y):
   r = x / y
   return r

def NiceJson(load):
    nicejson = pprint.pformat(load, indent=4, sort_dicts=True)
    nicejson2 = nicejson[:-1] + "\n}"
    nicejson3 = str(nicejson2).replace("'", '"')
    return nicejson3     
    
def Binary(text):
    result = pyfiglet.figlet_format(text, font = "binary" )
    return result

def Asciify(text):
    ascii_banner = pyfiglet.figlet_format(text)
    return ascii_banner

def Morsify(text):
    result = pyfiglet.figlet_format(text, font = "morse")
    return result

if __name__ == "__main__":
    exit()
