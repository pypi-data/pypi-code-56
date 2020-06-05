import numpy as np

def lsr2helio(l, b, vlsr, reverse=False):
    c1=-10.27
    c2=15.32
    c3=7.74

    ut=-np.cos(b)*np.cos(l)
    vt=np.cos(b)*np.sin(l)
    wt=np.sin(b)
    s=ut*c1+vt*c2+wt*c3
    if reverse==False:
        vhelio=vlsr-s
        print(vhelio)
        return vhelio
    else:
        vhelio=vlsr+s
        print(vhelio)
        return vhelio

