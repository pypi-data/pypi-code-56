#!/usr/bin/python3

'''
Even/Odd/Prime number checker
'''

def EOP_Checker(n):

    try:
        n = int(n)
        for j in range(2,n+1):
            q = n/j   #quotient
            r = n % j #remainder
            #if quotient q is >= j and remainder r = 0 will exit for loop and number is not prime
            if (q > 1) and r == 0:
                break
            #if quotient q is = j and remainder r = 0 number is prime
            if (q == 1) and (r == 0) and (n !=2) :
                print(str(n) + " is a Prime number" + '\n')
                break
        if (n % 2 == 0) or (n == 2):
            print(str(n) + " is a Even number" + '\n')
        elif (n % 3 == 0):
            print(str(n) + " is a Odd number" + '\n')
        elif (n == 1) or (n == 0):
            print(str(n) + " is a Prime number" + '\n')
    except Exception as Error:
        print (Error)
