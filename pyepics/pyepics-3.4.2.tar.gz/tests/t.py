import epics
import time
import debugtime
from collections import OrderedDict

dt = debugtime.debugtime()
def add(x):
    print(x)
    dt.add(x)

def read_list_pvs(fname='fastconn_pvlist.txt', max=10000):
    pvnames = []
    for line  in open(fname, 'r').readlines():
        if not line.startswith('#'):
            pvnames.append(line.strip())

    return pvnames[:max]

add('test of fast connection to many PVs')
pvnames = read_list_pvs()
add('read PV list')

time.sleep(0.001)
pvs = [epics.PV(name) for name in pvnames]
add('created PV objects')

time.sleep(0.001)
vals = [p.get() for p in pvs]
add('got values')

dt.show()

time.sleep(0.01)

for p in pvs:
   if not p.connected: print(p)
