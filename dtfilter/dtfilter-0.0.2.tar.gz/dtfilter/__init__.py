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


#Return keys of a dictionary as a list whose values are greater than some input value
def vgreaterthan(d,i):
    l=list()
    for key, value in d.items():
        if value>i:
            l.append(key)
    return l

#Return keys of a dictionary as a list whose values are lesser than some input value 
def vlesserthan(d,i):
    l=list()
    for key, value in d.items():
        if value<i:
            l.append(key)
    return l

#Return keys of a dictionary as a list whose values are equal to some input value 
def vequalto(d,i):
    l=list()
    for key, value in d.items():
        if value==i:
            l.append(key)
    return l


#Check if multiple keys are present in a dictionary
def mulkey(d,*args):
    y=args[0]
    for i in args:
        y=d.keys() >= {i}
        print(i,y) 

#Returns a dictionary of frequencies of items in a list
def itemfreq(l):
    count = {} 
    for i in l:
       count[i] = count.get(i, 0) + 1
    return count
