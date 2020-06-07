class py_counter():
    def __init__(self):
        return self

    def counter(self,arr):
        '''
        Function that takes in a list or a tuple as an argument and converts it to a hash map that has a (key-value) pair of (element-count of the element's occurrence in the list/tuple).
        '''
        d={}
        for x in range(len(arr)):
            y = arr.count(arr[x])
            d[arr[x]] = y
        return d
