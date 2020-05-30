class LousyInitable:
    """
    Make it possible for @dataclass classes to be instantiated with extra kwargs.
    """

    @classmethod
    def init_lousy(cls, logger=None, **data):
        needed_data = {k: v for k, v in data.items() if k in cls.__annotations__.keys()}
        extra_keys = set(data) - set(needed_data)
        if extra_keys and logger:
            logger(f"Got extra keys in LousyInitable subclass: {', '.join(map(str, extra_keys))}")
        return cls(**needed_data)
