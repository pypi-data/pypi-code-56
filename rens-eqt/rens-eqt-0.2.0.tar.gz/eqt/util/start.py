def get_a_b():
    a, b, l = 12313, 12312, 14
    import random
    if random.randrange(0, 2) == 1:
        b = a
    return a, b

    a = int(input("Input value a: "))
    b = int(input("Input value b: "))

    return a, b
