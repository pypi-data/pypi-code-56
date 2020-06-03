"""Welcome to embeddix.

This is the entry point of the application.
"""
import os

import argparse
import logging
import logging.config

import numpy as np

from tqdm import tqdm

import embeddix.utils.config as cutils


logging.config.dictConfig(
    cutils.load(
        os.path.join(os.path.dirname(__file__), 'logging', 'logging.yml')))

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


def _load_shared_vocab(vocabs_dirpath):
    vocabs_names = [filename for filename in os.listdir(vocabs_dirpath) if
                    filename.endswith('.vocab')]
    vocabs = [load_vocab(os.path.join(vocabs_dirpath, vocab_name))
              for vocab_name in vocabs_names]
    return _get_shared_vocab(vocabs)


def _reduce_model(model, vocab, shared_vocab):
    _model = np.empty(shape=(len(shared_vocab), model.shape[1]))
    idx_to_word = {idx: word for word, idx in shared_vocab.items()}
    for idx, word in idx_to_word.items():
        _model[idx] = model[vocab[word]]
    return _model


def _align_vocabs_and_models(args):
    logger.info('Aligning vocabularies under {}'
                .format(args.embeddings_dirpath))
    shared_vocab = _load_shared_vocab(args.embeddings_dirpath)
    logger.info('Shared vocabulary size = {}'.format(len(shared_vocab)))
    model_names = [filename.split('.npy')[0] for filename in
                   os.listdir(args.model_dir) if filename.endswith('.npy')]
    logger.info('Processing models = {}'.format(model_names))
    for model_name in model_names:
        model_filepath = os.path.join(args.model_dir,
                                      '{}.npy'.format(model_name))
        model = np.load(model_filepath)
        vocab_filepath = os.path.join(args.model_dir,
                                      '{}.vocab'.format(model_name))
        vocab = load_vocab(vocab_filepath)
        reduced_model = _reduce_model(model, vocab, shared_vocab)
        reduced_model_filepath = os.path.join(args.model_dir,
                                              '{}-reduced'.format(model_name))
        np.save(reduced_model_filepath, reduced_model)
        reduced_vocab_filepath = os.path.join(
            args.model_dir, '{}-reduced.vocab'.format(model_name))
        with open(reduced_vocab_filepath, 'w', encoding='utf-8') as output_str:
            for word, idx in shared_vocab.items():
                print('{}\t{}'.format(idx, word), file=output_str)


def _extract_words_and_vectors_from_txt(embeddings_filepath):
    words = []
    vectors = None
    with open(embeddings_filepath, 'r', encoding='utf-8') as input_str:
        for line in tqdm(input_str, total=count_lines(embeddings_filepath)):
            line = line.strip()
            if line:
                tokens = line.split(' ', 1)
                key = tokens[0].lower()
                words.append(key)
                value = np.fromstring(tokens[1], dtype='float32', sep=' ')
                if not np.any(vectors):
                    vectors = value
                else:
                    vectors = np.vstack((vectors, value))
    return words, vectors


def _convert_to_txt(embeddings_filepath, vocab_filepath):
    logger.info('Converting input numpy file to txt: {}'
                .format(embeddings_filepath))
    vocab = load_vocab(vocab_filepath)
    model = np.load(embeddings_filepath)
    txt_model_filepath = '{}.txt'.format(embeddings_filepath.split('.npy')[0])
    logger.info('Saving output to {}'.format(txt_model_filepath))
    with open(txt_model_filepath, 'w', encoding='utf-8') as otp:
        for word, idx in vocab.items():
            vector = ' '.join([str(item) for item in model[idx].tolist()])
            print('{} {}'.format(word, vector), file=otp)


def _convert_to_numpy(embeddings_filepath):

    logger.info('Converting input txt file to numpy: {}'
                .format(embeddings_filepath))
    output_filepath = '{}'.format(embeddings_filepath.split('.txt')[0])
    words, vectors = _extract_words_and_vectors_from_txt(embeddings_filepath)
    logger.info('Saving numpy vectors to {}.npy'.format(output_filepath))
    np.save(output_filepath, vectors)
    vocab_filepath = '{}.vocab'.format(output_filepath)
    logger.info('Saving vocabulary to {}'.format(vocab_filepath))
    with open(vocab_filepath, 'w', encoding='utf-8') as vocab_stream:
        for idx, word in enumerate(words):
            print('{}\t{}'.format(idx, word), file=vocab_stream)


def _convert(args):
    if args.to == 'numpy':
        if not args.embeddings.endswith('.txt'):
            raise Exception('Invalid input file: should be a text file '
                            'ending with .txt')
        _convert_to_numpy(args.embeddings)
    else:
        if not args.embeddings.endswith('.npy'):
            raise Exception('Invalid input file: should be a numpy file '
                            'ending with .npy')
        if not args.vocab:
            raise Exception('Converting to txt requires specifying the '
                            '--vocab parameter')
        _convert_to_txt(args.embeddings, args.vocab)


def _extract_vocab(args):
    words = []
    logger.info('Extracting vocabulary from {}'.format(args.embeddings))
    with open(args.embeddings, 'r', encoding='utf-8') as m_stream:
        for line in tqdm(m_stream, total=count_lines(args.embeddings)):
            line = line.strip()
            word = line.split(' ')[0]
            words.append(word)
    vocab_filepath = '{}.vocab'.format(
        os.path.abspath(args.embeddings).split('.txt')[0])
    with open(vocab_filepath, 'w', encoding='utf-8') as v_stream:
        for idx, word in enumerate(words):
            print('{}\t{}'.format(idx, word), file=v_stream)
    logger.info('Extracted {} words'.format(len(words)))


def main():
    """Launch embeddix."""
    parser = argparse.ArgumentParser(prog='embeddix')
    subparsers = parser.add_subparsers()
    parser_extract = subparsers.add_parser(
        'extract', formatter_class=argparse.RawTextHelpFormatter,
        help='extract vocab from embeddings txt file')
    parser_extract.set_defaults(func=_extract_vocab)
    parser_extract.add_argument('-e', '--embeddings', required=True,
                                help='input embedding in txt format')
    parser_convert = subparsers.add_parser(
        'convert', formatter_class=argparse.RawTextHelpFormatter,
        help='convert embeddings to and from numpy and txt formats')
    parser_convert.set_defaults(func=_convert)
    parser_convert.add_argument('-t', '--to', choices=['numpy', 'txt'],
                                help='output format: numpy or text')
    parser_convert.add_argument('-v', '--vocab',
                                help='absolute path to vocabulary')
    parser_convert.add_argument('-e', '--embeddings', required=True,
                                help='absolute path to embeddings file')
    parser_reduce = subparsers.add_parser(
        'reduce', formatter_class=argparse.RawTextHelpFormatter,
        help='align numpy model vocabularies. Will also align the .npy models')
    parser_reduce.set_defaults(func=_align_vocabs_and_models)
    parser_reduce.add_argument('-d', '--embeddings-dir', required=True,
                               help='absolute path to .npy models '
                                    'directory. The directory should '
                                    'contain the .vocab files '
                                    'corresponding to the .npy models.')
    args = parser.parse_args()
    args.func(args)
