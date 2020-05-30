class Singleton:
    """
    Singleton Superclass
    Usage:
        class MyClass(Singleton):
            ...

    Retrieved from: https://stackoverflow.com/a/11517201/1329429
    """

    def __new__(cls, *args, **kwargs):
        cls._instance = cls.__dict__.get("_instance")
        if cls._instance is not None:
            return cls._instance
        cls._instance = object.__new__(cls)
        # First time initializing a singleton subclass
        cls._instance.__init__(*args, **kwargs)
        return cls._instance
