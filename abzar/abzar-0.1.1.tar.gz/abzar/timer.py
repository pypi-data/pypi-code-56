import time


class Timer:
    """
    time execution of any with block aka Context Manager, retrieve the period it took from self.total
    """

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.total = (self.end - self.start) * 1000
