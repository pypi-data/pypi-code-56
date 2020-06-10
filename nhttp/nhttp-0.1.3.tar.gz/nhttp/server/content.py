

class ContentType:
    def __init__(self, raw_type :str, main_type :str, sub_type :str, params :dict):
        self.__raw_type = raw_type
        self.__main_type = main_type
        self.__sub_type = sub_type
        self.__params = params
    
    @property
    def raw_type(self) -> str:
        return self.__raw_type

    @property
    def main_type(self) -> str:
        return self.__main_type

    @property
    def sub_type(self) -> str:
        return self.__sub_type

    @property
    def parameters(self) -> dict:
        return self.__params
    
    @staticmethod
    def parse(type_str :str):
        try:
            raw = type_str
            rawns = type_str.replace(' ', '')
            
            tdes, *params = rawns.split(';')

            main, sub = tdes.split('/')
            params = {pstr[0] : pstr[1] for pstr in params}

            return ContentType(raw, main, sub, params)

        except (IndexError) :
            return None
