import numpy as np

def clearrepetition(wave,flam,eflam=None):
    unique = np.unique(wave)
    wavetmp,flamtmp,eflamtmp = [],[],[]
    for i in unique:
        m = np.where(wave == i)
        wavetmp.append(np.mean(wave[m]))
        flamtmp.append(np.mean(flam[m]))
        if len(eflam) > 0:
            eflamtmp.append(np.sqrt(np.sum(np.power(eflam[m],2))))
    return np.array(wavetmp),np.array(flamtmp),np.array(eflamtmp)    
