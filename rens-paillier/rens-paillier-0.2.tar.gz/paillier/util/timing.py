import timeit
from decimal import Decimal

from paillier.util.prime_generation import naive_generation, miller_rabin_generation


def evaluate(func, k=8, number=1):
    total_time = Decimal(timeit.timeit(lambda: func(k), number=number))
    print(f"{func.__name__} (k={k}) took {total_time / number:.2E}s to run")


evaluate(naive_generation)
evaluate(naive_generation, k=16)
evaluate(naive_generation, k=32)
# evaluate(naive_generation, k=64)

evaluate(miller_rabin_generation)
evaluate(miller_rabin_generation, k=16)
evaluate(miller_rabin_generation, k=32)
evaluate(miller_rabin_generation, k=64)
evaluate(miller_rabin_generation, k=1024)
evaluate(miller_rabin_generation, k=2048)
