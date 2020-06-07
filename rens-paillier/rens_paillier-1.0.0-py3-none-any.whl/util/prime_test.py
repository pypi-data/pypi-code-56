from decimal import Decimal
from random import randrange


def large_sqrt(n):
    # Method which can handle large numbers
    n = Decimal(n)
    return int(n.sqrt())


def naive_test(n):
    if n % 2 == 0:
        return False

    for i in range(3, large_sqrt(n) + 1, 2):
        if n % i == 0:
            return False

    return True


def miller_rabin_test(n, k=128):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True
