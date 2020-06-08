def outlierdetection(data,method):
    """
    # outlierdetection detects outliers given data and method.
    # method = dictionary where good data is defined.
    # data = array of data
    # return a mask (i.e., boolean array parallel to data) with True for good data.
    #####
    # method = {'name': 'method_name',
    #           'rule': dictionary}
    #####
    # 'method': 'median' for median clipping
    # 'rule': {'minp':minp,'maxp':maxp,'niter':niter,'initmask':initmask}
    # where [minp*median, max*median] defines good data (inclusive both sides) 
    # and median iteratively defined by good data
    # niter = integer 
    # initmask = array parallel to data with True for good data to initialize the process
    # initmask = array of True if not specified otherwise
    # Note: median clipping is good for global detection given some knowledge about global boundaries.
    # For example, if you have two epochs of a SN data, and we know that
    #####
    # 'method': 'sigma' for sigma clipping
    # 'rule': {'minp':minp,'maxp':maxp,'niter':niter,'initmask'} 
    # where [median - minp*std, median + maxp*std] defines good data (inclusive both sides)
    # where, respectively, median and std are median and standard deviation defined by good data iteratively.
    # initmask = array parallel to data with True for good data to initialize the process
    # initmask = array of True if not specified otherwise
    # Note: sigma clipping is good for examining outliers using local variation.
    #####
    # 'method': 'sn' for signal-to-noise ratio clipping (not iterative)
    # 'rule': {'minp':minp, 'noise':noise}
    # where noise is an array parallel to data (as standard deviation, not variance)
    # for calculating SN = data / noise
    # good data has SN >= minp
    # Note: sn clipping is good for excluding faint points, and data quality control.
    ##########
    """
    import numpy as np
    ##########
    # 0. Input
    data = np.array(data)
    methodname = method['name']
    rule = method['rule']
    try:
        mask = rule['initmask']
    except:
        mask = np.full_like(data,True,dtype=bool)
        rule['initmask'] = mask.copy()
    ##########
    # 1. Compute
    if methodname in {'median','sigma'}:
        minp,maxp = rule['minp'],rule['maxp']
        niter = rule['niter']
        for i in range(rule['niter']):
            gooddata = data[mask] # good data
            ### median or sigma
            if methodname=='median':
                median = np.median(gooddata)
                minbound = minp*median
                maxbound = maxp*median
            elif methodname=='sigma':
                std = np.std(gooddata)
                median = np.median(gooddata)
                minbound = median - minp*std
                maxbound = median + maxp*std
            else:
                pass
            ### update mask
            m = np.argwhere((data >= minbound) & (data <= maxbound)).flatten() # good data
            mask = np.full_like(data,False,dtype=bool)
            mask[m] = True
    elif methodname == 'sn':
        minp = rule['minp']
        noise = rule['noise']
        sn = data / noise
        m = np.argwhere(sn >= minp).flatten()
        mask = np.full_like(data,False,dtype=bool)
        mask[m] = True
    else:
        raise ValueError('method {0} does not support'.format(method))
    ##########
    # 2. Update with the initial mask and return
    return mask & rule['initmask']
