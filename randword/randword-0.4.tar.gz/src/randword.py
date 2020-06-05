from random import choice

from os import path
from distutils.sysconfig import get_python_lib


def get_path_to_pos_file(part_of_speech: str) -> str:
    if path.isfile(get_python_lib() + '/plateDetect'):
        package_path = get_python_lib() + '/plateDetect'
    else:
        package_path = path.dirname(__file__)

    return f'{package_path}/words/{part_of_speech}.txt'



# From now on abbreviation "pos" means "part of speech"


def get_random_word(include_pos: list or None = None,
                    exclude_pos: list or None = None,
                    min_length: int = 1,
                    max_length: int or None = None,
                    starts_with: str or None = None,
                    ends_with: str or None = None,
                    pattern: str or None = None) -> str or -1:
    if not include_pos:
        include_pos = ['adj', 'adv', 'conj', 'interj', 'noun', 'prep', 'pron', 'verb']

    if exclude_pos:
        parts_of_speech = list(set(include_pos) - set(exclude_pos))
    else:
        parts_of_speech = include_pos

    words = []
    for part_of_speech in parts_of_speech:
        pos_file_path = get_path_to_pos_file(part_of_speech)
        with open(pos_file_path, 'r') as pos_file:
            pos_words = pos_file.readlines()
            words.extend(pos_words)
    words = [word.rstrip() for word in words]

    if max_length:
        filtered_words = list(filter(lambda word: min_length <= len(word) <= max_length, words))
    else:
        filtered_words = list(filter(lambda word: min_length <= len(word), words))

    if starts_with:
        filtered_words = list(filter(lambda word: word.startswith(starts_with), filtered_words))
    if ends_with:
        filtered_words = list(filter(lambda word: word.endswith(ends_with), filtered_words))
    if pattern:
        filtered_words = list(filter(lambda word: pattern in word, filtered_words))

    try:
        return choice(filtered_words)
    except IndexError:
        return -1


if __name__ == "__main__":
    print(get_random_word())
