r"""Module for training a new model of the lemmatizer.

Basic usage:
python glemmazon/extract_exceptions.py \
  --conllu data/en_ewt-ud-train.conllu \
  --exceptions data/en_exceptions.csv
"""

from absl import app
from absl import flags

from glemmazon import cleanup
from glemmazon import preprocess

FLAGS = flags.FLAGS
flags.DEFINE_string("conllu", None, "Path to a CoNLL-U file.")
flags.DEFINE_string("exceptions", None,
                    "Path to a CSV with lemma exceptions [columns: "
                    "'word', 'pos', 'lemma'].")

flags.DEFINE_string("cleanup", "dummy",
                    "Name of the clean-up function to be used. Use "
                    "'dummy' for no clean-up.")
flags.DEFINE_integer("min_count", 0,
                     "The minimum number of counts a lemma suffix need "
                     "to have for it to be included for training.")

flags.mark_flags_as_required(['conllu', 'exceptions'])


# noinspection PyPep8Naming
def main(_):
    print('Reading sentences from CoNLL-U...')
    df = preprocess.conllu_to_df(FLAGS.conllu,
                                 getattr(cleanup, FLAGS.cleanup),
                                 min_count=FLAGS.min_count)
    df = df[['word', 'pos', 'lemma']][df['word'] != df['lemma']]
    df = preprocess.add_lemmatizer_info(df)

    print('Saving the exceptions .csv...')
    df.to_csv(FLAGS.exceptions, index=False)

    print('Done!')


if __name__ == '__main__':
    app.run(main)
