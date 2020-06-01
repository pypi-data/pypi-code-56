class BaseError(Exception):
    message = "An unknown error occurred ({reason})."

    def __init__(self, **kwargs: str) -> None:
        super().__init__(self.message.format(**kwargs))
