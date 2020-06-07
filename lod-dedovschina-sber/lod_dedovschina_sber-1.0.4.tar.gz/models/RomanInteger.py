class RomanInteger:
    """
    Class RomanInteger

    Transform roman integer to arabic integer
    """

    roman_ints = {
        'I': 1, 
        'V': 5, 
        'X': 10, 
        'L': 50, 
        'C': 100, 
        'D': 500, 
        'M': 1000
    }

    def __init__(self, roman_int: str):
        self.roman_int = roman_int

    def to_integer(self):
        roman_ints = self.roman_ints
        roman_int = self.roman_int
        integer = 0

        for digit in range(len(roman_int)):
            if digit > 0 and roman_ints[roman_int[digit]] > roman_ints[roman_int[digit - 1]]:
                integer += roman_ints[roman_int[digit]] - 2 * roman_ints[roman_int[digit - 1]]
            else:
                integer += roman_ints[roman_int[digit]]

        return integer