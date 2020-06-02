import re

def convert_to_boolean(val):
    return 1 if val else 0

def round_2_decimal(x):
    return float(round(x, 2))

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
