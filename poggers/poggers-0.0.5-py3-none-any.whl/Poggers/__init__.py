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

def Banner(text):
    ascii_banner = pyfiglet.figlet_format(text)
    return ascii_banner

def Morse(text):
    result = pyfiglet.figlet_format(text, font = "morse")
    return result

def Block(text):
    result = pyfiglet.figlet_format(text, font = "block")
    return result

def Chunky(text):
    result = pyfiglet.figlet_format(text, font = "chunky")
    return result

def Cosmic(text):
    result = pyfiglet.figlet_format(text, font = "cosmic")
    return result

def Diamond(text):
    result = pyfiglet.figlet_format(text, font = "diamond")
    return result

def Isometric(text):
    result = pyfiglet.figlet_format(text, font = "isometric1")
    return result

def Italics(text):
    result = pyfiglet.figlet_format(text, font = "italic")
    return result

def Roman(text):
    result = pyfiglet.figlet_format(text, font = "roman")
    return result

def Shadow(text):
    result = pyfiglet.figlet_format(text, font = "shadow")
    return result

def Slant(text):
    result = pyfiglet.figlet_format(text, font = "slant")
    return result

def Speed(text):
    result = pyfiglet.figlet_format(text, font = "speed")
    return result





if __name__ == "__main__":
    exit()
