import os

class XVGReader:

    def __init__(self, filename):

        if not os.path.exists(filename):
            raise IOError('The XVG file {} does not exist.'.format(filename))

        with open(filename, 'r') as fin:
            data = fin.readlines()

        data = [v.split() for v in data]
        
        self._x = [float(v[0]) for v in data]

        self._y = [float(v[1]) for v in data]

        self._filename = filename

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def n_values(self):
        return len(self._x)

if __name__ == '__main__':

    import sys

    reader = XVGReader(sys.argv[1])



