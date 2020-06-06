import random
import string
def genGoodpass(n):
    '''
      This ohsgpgn is a simple good password generator. The generated password includes at least one number,one ascii,one capatalized ascii and one special chars(‘!@$%^&*()+’).With argument, length of password can be set. If the argument(n) is less than 10(n < 10), the generated password length will be at least 10.
    '''
    if n < 10:
        n = 10
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
