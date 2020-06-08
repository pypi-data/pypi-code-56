class py_counter():
    def __init__(self):
        return None

    def counter(self,arr):
        '''
        Function that takes in a list, tuple or a sequence of Integer or String type, as an argument and converts it to a hash map that has a (key-value) pair of (element-count of the element's occurrence in the list/tuple).
        '''
        try:
            d={}
            for x in range(len(arr)):
                y = arr.count(arr[x])
                d[arr[x]] = y
            return d
        except TypeError as t:
            return "Exception: Please enter a series of strings/integers or a List/Tuple."
