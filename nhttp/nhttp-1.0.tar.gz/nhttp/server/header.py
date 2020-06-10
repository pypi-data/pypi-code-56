
class Header(dict):
    def __init__(self, **hd_kwargs):
        self.__hd = hd_kwargs

        super().__init__(hd_kwargs)

    @property
    def header_dict(self) -> dict :
        return self.__hd
