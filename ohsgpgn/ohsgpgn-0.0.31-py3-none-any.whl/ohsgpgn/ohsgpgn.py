import random
import string
def genGoodpass(n):
    #Generate n length of password that include at least one each lower and uppercase ascii,digit(at least one),speciat chars('!@#$%^&*()+')-at least one.
    goodPass=[]
    rc=random.choice
    sal=string.ascii_lowercase
    sau=string.ascii_uppercase
    spchar='!@#$%^&*()+'
    sd=string.digits
    passins=[sal,sau,spchar,sd]
    for i in range(n-4):
        passins.append(rc(passins))
    for i in passins:
        goodPass.append(rc(i))

    
    random.shuffle(goodPass)
    goodPass=''.join(goodPass)
    return goodPass
