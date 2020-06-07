import unittest
from models.Address import Address

class TestAddress(unittest.TestCase):
    def set_addresses(self):
        self.rigth_addresses = [
            "117418, Московская область, г. Балашиха, дер.Черное, ул. НОВОЧЕРЕМУШКИНСКАЯ, дом 44, корп. 1, стр. 1, оф. 207",
            "117042, г.Москва, ул. Южнобутовская, дом 139, пом. II, ком. 2Е",
            "117042, г.Москва, ул. Южнобутовская, дом 139, эт. 1, пом. II, ком. 6 РМ 5",
            "117105, г. Москва, шоссе Варшавское, д. 1 стр. 6 ком. XXII/4, пом. 1 этаж 3(БЦ W Plaza 2)",
            "14200, Московская область, с.Богослово, 2 км Северо-Западнее, СНТ Елочка, Московская область, г Домодедово, мкр.Центральный, пр-д. Советский 1-й, дом 2, кв. 224, дом 2, кв. 224",
            "Город Москва столица Российской Федерации город федерального значения, г.Москва, Раменки, дом 18, кв. 108"
        ]

        self.wrong_addresses = [
            "142001, 142011, Московская область, с.Богослово, 2 км Северо-Западнее, СНТ Елочка, Московская область, г Домодедово, мкр.Центральный, пр-д. Советский 1-й, дом 2, кв. 224, дом 2, кв. 224"
        ]

    def test_address_zip(self):
        self.set_addresses()

        test_address = self.rigth_addresses[0]

        address = Address(test_address)
        address.extract_zip_code()

        print('\nZip code is ' + address.zip_code)

        self.assertIsNotNone(address.zip_code)

    def test_address_zip_double(self):
        self.set_addresses()

        test_address = self.wrong_addresses[0]

        address = Address(test_address)

        try:
            address.extract_zip_code()
        except Exception as e:
            print(str(e))
            self.assertFalse(False)

    def test_address_tokenize(self):
        self.skipTest('Private method')
        self.set_addresses()

        test_address = self.rigth_addresses[0]

        address = Address(test_address)
        tokens = address.tokenize()

        self.assertTrue(
           isinstance(tokens, list)  
        )

    def test_address_clear_characters(self):
        self.skipTest('Private method')
        self.set_addresses()

        test_address = self.rigth_addresses[0]

        address = Address(test_address)
        clear_address = address.clear_characters()

        print(clear_address)

    def test_address_preprocess(self):
        self.set_addresses()

        test_address = self.rigth_addresses[0]

        address = Address(test_address)
        address = address.extract_zip_code()
        process = address.preprocess()

        print(process.process_address)

    def test_address_extract_house_tokens(self):
        self.set_addresses()

        test_address = self.rigth_addresses[0]

        address = Address(test_address)

        print(address.extract_house_tokens())

    def test_address_string(self):
        self.set_addresses()

        test_address = self.rigth_addresses[1]

        address = Address(test_address)

        print(address.address_string())


