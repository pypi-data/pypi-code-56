class Map:
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return iter(self.iterable)

    def __getattr__(self, key):
        return Each(getattr(i, key) for i in self.iterable)

    def __call__(self, *args, **kwargs):
        return Each(i(*args, **kwargs) for i in self.iterable)
