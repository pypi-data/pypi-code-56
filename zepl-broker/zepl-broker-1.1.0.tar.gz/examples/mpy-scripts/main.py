import json, sys, os, machine, binascii, gc, hashlib, select
import neopixel as np
import time

# initialization
p = select.poll()
p.register(sys.stdin, select.POLLIN)

dev_id = binascii.hexlify(machine.unique_id()).decode()
NP_PIN = machine.Pin(0)

file_hashtab = {}
for f in os.listdir():
    with open(f, 'r') as fd:
        hasher = hashlib.sha1()
        lines = fd.readlines()
        hasher.update("".join(lines))
        file_hashtab[f] = binascii.hexlify(hasher.digest())
    del hasher

hashtab_json = json.dumps(file_hashtab)
del file_hashtab
gc.collect()

print('Waiting for input...')
led = np.NeoPixel(NP_PIN, 1)
led.fill((0,255,0))
led.write()

act=[]
ctrl_input=None
while True:
    while p.poll(100):
        ctrl_input = sys.stdin.read(1)
    #print('CTRL_INPUT {}'.format(ctrl_input))

    if ctrl_input == '1':
        print('DEV_MAC {}'.format(dev_id))
    elif ctrl_input == '2':
        print('F_HTAB {}'.format(hashtab_json))
    elif ctrl_input == '3':
        print('HEART BEAT')
        print('LOG sleeping 5 seconds')
        time.sleep(5)
    elif ctrl_input == 'a':
        try:
            import app_a
        except:
            print('ERROR problem in a')
    elif ctrl_input == 'b':
        try:
            import app_b
        except:
            print('ERROR problem in b')
    else:
        if ctrl_input:
            print('ERROR unknown control input: {}'.format(ctrl_input))
