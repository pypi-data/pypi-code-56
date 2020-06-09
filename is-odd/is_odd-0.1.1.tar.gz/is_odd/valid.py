def checkOdd(input):
    if (input % 2 !=0):
        return True
    return False
def valid(input):
    if isinstance(input, int):
        return checkOdd(input)
    else:
        try:
            float(input)
        except:
            raise ValueError('expected a number')
        else:
            if float(input).is_integer():
                return checkOdd(float(input))
    raise ValueError('expected an interger')
    return False