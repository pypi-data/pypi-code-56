import re
import csv
import itertools
import operator
from presets import clear_characters, fias_types
from models.RomanInteger import RomanInteger


class Address:
    input_address = None
    tokens = None

    zip_code = None

    def __init__(self, input_address: str):
        self.input_address = input_address
        self.processing_address = input_address

        self.house_types_inv = self.__inverse_dict(fias_types.house_signs)

        self.prepared_address = self.__prepare_to_tokenize()
        self.tokens = self.__tokenize(self.prepared_address)

    def address_string(self):
        prepared_address = self.prepared_address
        house_tokens, house_types = self.extract_house_tokens()
        slice_ = self.tokens_to_string(house_tokens, prepared_address)
        house = self.clearify_address(house_tokens, house_types)

        prepared_address = prepared_address[:slice_]

        address = self.extract_other_tokens(prepared_address)

        final_address = ""

        for i, j in address.items():
            if j:
                final_address += "{0} {1}, ".format(i, j)
            else:
                final_address += "{0}, ".format(i)

        for i, j in house.items():
            final_address += "{0} {1}, ".format(i, j)

        if self.zip_code:
            self.zip_code = str(self.zip_code) + ", "

        final_address = self.zip_code + final_address[:-2]

        return final_address

    def __clear_characters(self, preparing_address: str):
        for char in clear_characters.clear_characters:
            preparing_address = preparing_address.replace(char, ' ')

        return re.sub(r"[\d]+", ' \g<0> ', preparing_address)

    def __get_token_type(self, token):
        if token.isdigit():
            return "число"
        elif token == ',':
            return "препинания"
        else:
            return "не распознано"

    def __roman_to_arabic(self, preparing_address: str):
        romans = re.findall(
            r'(?=\b[MDCLXVI]+\b)M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})',
            preparing_address
        )

        for roman in romans:
            preparing_address = preparing_address.replace(
                roman,
                str(RomanInteger(roman).to_integer())
            )

        return preparing_address

    def __inverse_dict(self, dict):
        resdic = {}
        for key, value in dict.items():
            for index in value:
                if type(value) == set or type(value) == list:
                    if index in resdic.keys():
                        if isinstance(resdic[index], set):
                            resdic[index].add(key)
                        elif isinstance(resdic[index], list):
                            resdic[index].append(key)
                        else:
                            resdic[index] = [resdic[index]]
                            resdic[index].append(key)
                    else:
                        resdic[index] = key
                elif type(value) == dict:
                    resdic.update(self.__inverse_dict(value))
        return resdic

    def __prepare_to_tokenize(self):
        preparing_address = self.extract_zip_code()
        preparing_address = self.__roman_to_arabic(preparing_address)
        preparing_address = preparing_address.lower()
        preparing_address = self.__clear_characters(preparing_address)
        preparing_address = re.sub(r' +', ' ', preparing_address)
        preparing_address = preparing_address.replace(' / ', '/')

        return preparing_address

    def __tokenize(self, prepared_address: str):
        return re.findall(r'[\d]+|[\w]+|,|-', prepared_address)

    def extract_zip_code(self):
        processing_address = self.input_address
        zip_code = re.findall(r'[^| |,][\d]{5}[ |$|, ]', processing_address)

        if len(zip_code) > 1:
            raise Exception("Два индекса в строке \"%s\" ?" %
                            processing_address)

        if zip_code != []:
            zip_code = zip_code[0]
            processing_address = processing_address.replace(
                zip_code, '').strip()
            zip_code = zip_code.replace(',', '')
        else:
            zip_code = ''

        self.processing_address = processing_address
        self.zip_code = zip_code

        return processing_address

    def extract_house_tokens(self):
        tokens = self.tokens
        house_types_inv = self.house_types_inv

        types = [
            house_types_inv.get(
                token,
                self.__get_token_type(token)
            )
            for token in tokens
        ]

        j = 0
        for i in range(len(types) - 1):
            i = i - j
            if types[i] == '"не распознано"':
                var = ' '.join([tokens[i], tokens[i + 1]])
                ss = house_types_inv.get(var, self.__get_token_type(var))

                if ss != '"не распознано"':
                    tokens[i], types[i] = var, ss
                    del tokens[i + 1], types[i + 1]
                    j += 1

                elif types[i] in house_types_inv and types[i + 1] == "число":
                    types[i+1] = types[i]
                    del tokens[i], types[i]
                    j += 1

            types_bin = [0 if x == "не распознано" else 1 for x in types]
            array = list((list(y) for (x, y) in itertools.groupby((enumerate(types_bin)), operator.itemgetter(1)) if x == 1))
            if len(array) == 0:
                return [], []
            longest_seq = max(reversed(array), key=len)

            return [tokens[i] for (i, _) in longest_seq], [types[i] for (i, _) in longest_seq]

    def extract_other_tokens(self, string):
        address_types = self.__inverse_dict(fias_types.address_types)
        dict_ = {}
        tokens = [self.__tokenize(i) for i in string.split(',')]
        for token in tokens:
            counter = 0
            for tag in range(len(token)-1):
                tag = tag-counter
                if len(token)-1 >= 2:
                    if token[tag+1] == "-":
                        try:
                            token[tag] = token[tag]+token[tag+1]+token[tag+2]
                            counter += 2
                            del token[tag + 2], token[tag + 1]
                        except IndexError:
                            pass

        for token in tokens:
            types = [address_types.get(x, self.__get_token_type(x)) for x in token]
            if len(types) > 1:
                for index, word in enumerate(types):
                    if word not in ("не распознано", "число"):
                        del token[index]
                        dict_[word] = " ".join(token)
                        break
            elif len(types) == 1:
                if types[0] not in ("не распознано", "число"):
                    del token[0]
                    dict_[types[0]] = None
        return dict_

    def tokens_to_string(self, tokens, string):
        pattern = r".?.?".join(tokens)

        found = re.search(pattern, string.lower())

        if found is None:
            split = len(string)
        else:
            split = found.start()
        return split

    def clearify_address(self, tokens, types):
        house_types_inv = self.house_types_inv

        for i, token in enumerate(tokens):
            if types[i] == "число":
                if "дом" not in types:
                    types[i] = "дом"
                elif "корпус" not in types:
                    types[i] = "корпус"
                elif "квартира" not in types:
                    types[i] = "квартира"
                elif types[i - 1] in fias_types.house_signs and types[i - 1] not in ('литера', 'дробь'):
                    types[i] = types[i - 1]
                elif i >= 2 and types[i - 1] == 'дробь':
                    types[i] = types[i - 2]
                    types[i - 1] = types[i - 2]
            elif types[i] == 'литера' and i != 0:
                tokens[i - 1] += tokens[i]

        dic = {}
        for token, typ in zip(tokens, types):
            if token not in house_types_inv and typ != 'препинания':
                if typ not in dic:
                    dic[typ] = token
        return dic
