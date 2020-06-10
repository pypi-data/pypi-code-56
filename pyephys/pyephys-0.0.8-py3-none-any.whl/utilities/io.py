import pickle
import numpy as np
from neo.io import AxonIO

def save_object(path, a):
    """Save an object in a file (.txt, .pic) with pickle."""

    with open(path, 'wb') as my_file:
        mon_pickler = pickle.Pickler(my_file)
        mon_pickler.dump(a)


def load_object(path):
    """Load an object from a file (.txt, .pic) with pickle."""

    with open(path, 'rb') as my_file:
        mon_depickler = pickle.Unpickler(my_file)
        a = mon_depickler.load()

    return a


def load_Axon_data(filelist, channel_names=['Ch1OUT', 'Ch1IN']):
    mydict = {}

    for channel_name in channel_names:
        mydict[channel_name] = []

    mydict['sf'] = []

    for filepath in filelist:

        f = AxonIO(filepath)
        r = f.read(signal_group_mode='split-all')

        asig_names = np.array([asig.name for asig in r[0].segments[0].analogsignals])

        for channel_name in channel_names:
            idx_channel = np.where(asig_names == channel_name)[0][0]
            mydict[channel_name].append(
                np.array([seg.analogsignals[idx_channel].as_array().T[0] for seg in r[0].segments]))

        mydict['sf'].append(float(r[0].segments[0].analogsignals[idx_channel].sampling_rate.magnitude))

    if np.unique(mydict['sf']).size == 1:
        for channel_name in channel_names:
            mydict[channel_name] = np.array(mydict[channel_name])

    mydict['sf'] = np.array(mydict['sf'])

    return mydict