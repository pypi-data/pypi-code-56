def clearrepetition(wave,flam):
    unique = np.unique(wave)
    wavetmp,flamtmp = [],[]
    for i in unique:
        m = np.where(wave == i)
        wavetmp.append(np.mean(wave[m]))
        flamtmp.append(np.mean(flam[m]))
    return np.array(wavetmp),np.array(flamtmp)
