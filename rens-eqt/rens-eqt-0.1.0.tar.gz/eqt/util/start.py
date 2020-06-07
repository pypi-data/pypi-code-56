def get_a_b():
    a, b, l = 12313, 12312, 14
    import random
    if random.randrange(0, 2) == 1:
        b = a
    return a, b, l

    a = int(input("Input value a: "))
    b = int(input("Input value b: "))

    bitlengths = (len(f'{x:b}') for x in (a, b))
    return a, b, max(bitlengths)
