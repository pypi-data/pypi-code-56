def sort(lst):
    max_val = lst[0]

    def add_val(num):
        nonlocal max_val
        max_val = num
        return num

    return [add_val(x) for x in l if x >= max_val]
