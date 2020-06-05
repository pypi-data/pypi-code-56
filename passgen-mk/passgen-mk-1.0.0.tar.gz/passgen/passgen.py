import string
import random

strings = {
    'lower': string.ascii_lowercase,
    'upper': string.ascii_uppercase,
    'digits': string.digits,
    'special': string.punctuation,
}


def get_sequence(**string_types):
    ''' Creates a string whose content depends on the sent parameters. '''
    sequence = ''
    for k, v in string_types.items():
        if v:
            sequence += strings[k]

    if sequence == '':
        raise TypeError('At least one type of characters must be set to get the sequence.')

    return sequence


def generate_password(sequence, length=16):
    return ''.join(random.choices(sequence, k=length))
