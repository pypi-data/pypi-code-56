"""
    This module contains the models used by the Umbrella API.
"""


class UmbrellaModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Site(UmbrellaModel):
    def __init__(self, name, **kwargs):
        self.name = name
        
        super().__init__(**kwargs)


class InternalNetwork(UmbrellaModel):
    def __init__(self, name, ip_address, prefix_length, **kwargs):
        self.name = name
        self.ip_address = ip_address
        self.prefix_length = prefix_length

        super().__init__(**kwargs)