import os
import random
import string
import re


class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def is_valid_number(number, client, twilio_exception):
    # Checks for valid phone
    try:
        client.lookups.phone_numbers(number).fetch(type="carrier")
        return True
    except twilio_exception as e:
        if e.code == 20404:
            return False
        else:
            raise e


def convert_to_boolean(val):
    return 1 if val else 0


def format_date(x):
    return x.strftime('%Y-%m-%d') if x else None


def round_2_decimal(x):
    return float(round(x, 2))


# generates 6 digit random code
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# converts a phone string to us number adding + 1
def make_us_number(num):
    result = re.sub('[^0-9]', '', num)
    if result[0] == '1':
        result = '+' + result
    else:
        result = '+1' + result
    if len(result) != 12:
        return 0
    return result
