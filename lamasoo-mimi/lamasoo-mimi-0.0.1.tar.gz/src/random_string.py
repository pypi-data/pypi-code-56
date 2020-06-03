import string, random

letters = string.ascii_uppercase


def generate_random_code(length): ''.join(random.choice(letters) for i in range(length))
