from string import punctuation

PUNCTUATION = set(punctuation)

LOWERCASE = {
    'a': 'ԭ',
    'b': 'Ъ',
    'c': 'с́',
    'd': 'Ԁ',
    'e': 'Ҽ',
    'f': 'Ғ',
    'h': 'Һ',
    'i': 'ї',
    'k': 'Ҡ',
    'm': 'Ԡ',
    'n': 'Л',
    'o': 'Ө',
    'p': 'Ҏ',
    'q': 'ҩ',
    'r': 'я',
    's': 'ꙅ',
    't': 'Г',
    'u': 'Ч',
    'v': 'ѵ',
    'w': 'Ѡ',
    'x': 'х',
    'y': 'У',
    'z': 'ԅ',
}

UPPERCASE = {
    'A': 'Д',
    'B': 'Б',
    'C': 'Ҫ',
    'D': 'Ԃ',
    'E': 'Э',
    'F': 'Ӻ',
    'G': 'Ҁ',
    'H': 'Ӊ',
    'I': 'Ї',
    'J': 'Ј',
    'K': 'Ҡ',
    'L': 'Ꙇ',
    'M': 'Ӎ',
    'N': 'И',
    'O': 'Ф',
    'P': 'Р̌',
    'Q': 'Ҩ',
    'R': 'Я',
    'S': 'Ꙅ',
    'T': 'т',
    'U': 'Џ',
    'V': 'Ѷ',
    'W': 'Щ',
    'X': 'Ж',
    'Y': 'Ұ',
    'Z': 'Ꙁ',
}

COMBINATION = {
    'bl': 'Ы',
    'io': 'Ю',
    'oo': 'Ꚙ',
}


def lookup(letter: str, d: dict = LOWERCASE) -> str:
    """Returns a Cyrillic letter if available, otherwise the input"""
    return d.get(letter, letter)


def convert(string: str = 'Hello World!') -> str:
    """Convert a string of Latin characters to faux Cyrillic"""
    new = str()
    for letter in string:
        if letter.isspace() or letter.isnumeric():
            new += letter
        elif letter in PUNCTUATION:
            new += letter
        elif letter.isalpha():
            if letter.islower():
                new += lookup(letter, LOWERCASE)
            else:
                new += lookup(letter, UPPERCASE)
    return new


if __name__ == '__main__':
    print(convert())
