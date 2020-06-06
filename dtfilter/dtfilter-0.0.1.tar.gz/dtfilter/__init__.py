#Return the element with maximum frequency in a list
def maxfreq(x):
    y=max(set(x),key=x.count)
    return y

#Return the element with minimum frequency in a list
def minfreq(x):
    y=min(set(x),key=x.count)
    return y

#Return a List of all "keys" in a dictionary
def dkey(x):
    y=list(x.keys())
    return y

#Return a List of all "values" in a dictionary
def dvalue(x):
    y=list(x.values())
    return y
