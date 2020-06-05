"""Files utils."""
import os
import logging

__all__ = ('load_vocab', 'count_lines', 'load_shared_vocab')

logger = logging.getLogger(__name__)


def load_vocab(vocab_filepath):
    """Load word_to_idx dict mapping from .vocab filepath."""
    word_to_idx = {}
    logger.info('Loading vocabulary from {}'.format(vocab_filepath))
    with open(vocab_filepath, 'r', encoding='utf-8') as input_stream:
        for line in input_stream:
            linesplit = line.strip().split('\t')
            word_to_idx[linesplit[1]] = int(linesplit[0])
    return word_to_idx


def count_lines(input_filepath):
    """Count number of non-empty lines in file."""
    counter = 0
    with open(input_filepath, 'r', encoding='utf-8') as input_str:
        for line in input_str:
            if line.strip():
                counter += 1
    return counter


def _get_shared_vocab(vocabs):
    shared_words = set()
    for word in vocabs[0].keys():
        is_found_in_all = True
        for vocab in vocabs[1:]:
            if word not in vocab:
                is_found_in_all = False
                break
        if is_found_in_all:
            shared_words.add(word)
    return {word: idx for idx, word in enumerate(shared_words)}


def load_shared_vocab(vocabs_dirpath):
    """Get intersection of all vocabularies under dirpath."""
    vocabs_names = [filename for filename in os.listdir(vocabs_dirpath) if
                    filename.endswith('.vocab')]
    vocabs = [load_vocab(os.path.join(vocabs_dirpath, vocab_name))
              for vocab_name in vocabs_names]
    return _get_shared_vocab(vocabs)
