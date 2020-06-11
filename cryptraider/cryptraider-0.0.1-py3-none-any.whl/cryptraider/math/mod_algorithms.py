import gmpy2

def find_square_roots_mod_2power(n, power) :
    roots = list([1])
    mexp = 1
    while mexp <= power :
        old_m = 2**(mexp-1)
        m = 2**mexp
        target = n%m
        new_roots = list()
        for root in roots :
            root1 = root
            if (root1*root1) % m == target :
                new_roots.append(root1)

            root2 = (root + old_m)%m
            if (root2*root2) % m == target :
                new_roots.append(root2)
        roots = new_roots
        mexp += 1
    return sorted(roots)