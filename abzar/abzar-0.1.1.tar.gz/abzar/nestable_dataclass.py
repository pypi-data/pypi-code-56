from dataclasses import dataclass, is_dataclass


def nested_dataclass(*args, **kwargs):
    """
    Allow dataclass classes as field types.
    Taken from: https://stackoverflow.com/a/51565863/1329429
    """

    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if isinstance(value, dict):
                    if is_dataclass(field_type):
                        # Handle simple Dataclass type
                        new_obj = field_type(**value)
                        kwargs[name] = new_obj
                    if (
                        hasattr(field_type, "__args__")
                        and len(field_type.__args__) == 2
                        and field_type.__args__[-1] == type(None)  # noqa: E721
                    ):
                        # Handle simple Dataclass type when it is in a list(e.g. When it is Optional)
                        field_type = [T for T in field_type.__args__ if is_dataclass(T)]
                        if field_type:
                            field_type = field_type[0]
                        new_obj = field_type(**value)
                        kwargs[name] = new_obj

            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper
