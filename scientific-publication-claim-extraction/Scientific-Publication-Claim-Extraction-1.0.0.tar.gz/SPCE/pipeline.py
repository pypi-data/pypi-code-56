"""Pipeline wrapper for the sentence classification model.

"""
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

from claim import get_claim
import pandas as pd
import numpy as np


def pipeline(abstract=""):

    # removing unnecessary punctuation because problems in tokenization
    punctuation = '!"#$%&\'()*+-/:;?@[\]^_`{|}~'
    output_df = None
    if type(abstract)==str:
        for c in punctuation:
            if c in abstract:
                abstract = abstract.replace(c, ' ')
        
        result = get_claim(abstract)

        output_df = pd.DataFrame({'label': result['labels'], 
                    'sentence': result['sents'], 
                    'score': result['scores']})

    return output_df

def prepare_NER(classification_df):
    temp_abs = classification_df
    usable_sent_list = temp_abs[temp_abs['label'].isin(['BACKGROUND', \
        'METHODS', 'RESULTS', 'CONCLUSIONS'])]['sentence'].to_list()

    output_df = pd.DataFrame(columns = ['Sentence', 'Placeholder'])
    temp_token_list = []

    for sentence in usable_sent_list:
        # The tokens denote the end of a sentence
        temp_token_list += word_tokenize(sentence) + [' ']   

    temp_token_list += ['END'] # This was a bug in bioBERT, it always ignores the last sentence

    output_df['Sentence'] = temp_token_list
    output_df['Placeholder'] = 'O'
    # output.loc[output['Sentence'] == '[SEP]', 'Placeholder'] = '[SEP]'
    # output.loc[output['Sentence'] == '[CLS]', 'Placeholder'] = '[CLS]'
    output_df.loc[output_df['Sentence'] == ' ', 'Placeholder'] = [' ']
    return output_df
