import libABCD

def add_handler(string,func):
    libABCD.cmd_switch[string]=func
