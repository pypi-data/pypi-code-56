import math

def getbinomialcoef(a,b):
	if b == 1 or a == b:
	    return 1
	if y > x:
	    print("Error ... the 2nd number is higher than the 1st.")
	    return 0   
	else:
	    fact_a = math.factorial(a)
	    fact_b = math.factorial(b)
	    div = fact_a // (fact_b*(a-b))
	    return div
	