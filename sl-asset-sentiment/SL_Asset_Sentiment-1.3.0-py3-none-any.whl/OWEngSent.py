# -*- coding: utf-8 -*-

import pandas as pd
import json
import os
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import model_from_json
import numpy as np
import pickle
import re

tokenizer_path="./OW_SL_Sentiment/OW_SL_Sentiment/eng_model/english_tweet_tokenizer.pickle"
model_path="./OW_SL_Sentiment/OW_SL_Sentiment/eng_model/english_tweet_model.json"
weights_path='./OW_SL_Sentiment/OW_SL_Sentiment/eng_model/english_tweet_weights.h5'


def _sentence_deep_sentiment(sentences, loaded_model, tokenizer, maxlen=80, special_characters = ""):
    sentences = list(map(lambda x: x.lower(), sentences))
    sentences = list(map(lambda x: re.sub('[^a-zA-z0-9\s\'{}]'.format(special_characters),'',x), sentences))
    sequences = tokenizer.texts_to_sequences(sentences)
    padded_sequences = sequence.pad_sequences(sequences, maxlen=maxlen)
    results = loaded_model.predict(padded_sequences)
    return [result[0] for result in results]

def create_sentence_deep_sentiment_columns(data_frame, tokenizer_path=tokenizer_path, model_path=model_path, weights_path=weights_path):
    """
    creates a sentiment per sentence using a deep learning model

    Returns:
    ----------
        data_frame: pandas data-frame
            altered data-frame with the sentence sentiment column

    Args:
    ----------
        data_frame: pandas data-frame
            data_frame containing the sentences in one column

        tokenizer_path: String
            path to the tokenizer file

        model_path: String
            path to the model json

        weights_path: String
            path to the weights
    """
    with open(tokenizer_path,'rb') as handle:
        tokenizer = pickle.load(handle)

    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(weights_path)

    #tqdm.pandas(desc="sentence sentiment")
    #data_frame["sentence_sentiment"] = data_frame["sentences"].apply(_sentence_deep_sentiment, loaded_model = loaded_model, tokenizer = tokenizer)
    sentiment=_sentence_deep_sentiment(list(data_frame["sentences"]),loaded_model = loaded_model, tokenizer = tokenizer)
    return sentiment
