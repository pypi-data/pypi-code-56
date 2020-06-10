# -*- coding: utf-8 -*-

import pandas as pd
import json
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import model_from_json
import numpy as np
import pickle
import re

def _sentence_deep_sentiment(sentences, loaded_model, tokenizer, maxlen=80, special_characters = ""):
    sentences = list(map(lambda x: x.lower(), sentences))
    sentences = list(map(lambda x: re.sub('[^a-zA-z0-9\s\'{}]'.format(special_characters),'',x), sentences))
    sequences = tokenizer.texts_to_sequences(sentences)
    padded_sequences = sequence.pad_sequences(sequences, maxlen=maxlen)
    results = loaded_model.predict(padded_sequences)
    return [result[0] for result in results]

def _sentence_deep_sentiment_de(sentences, loaded_model, tokenizer, maxlen=80, special_characters = ""):
    
    de_sentiment_dict={0:"negative",1:'neutral',2:'positive'}
    sentences = list(map(lambda x: x.lower(), sentences))
    sentences = list(map(lambda x: re.sub('[^a-zA-z0-9\s\'{}]'.format(special_characters),'',x), sentences))
    sequences = tokenizer.texts_to_sequences(sentences)
    padded_sequences = sequence.pad_sequences(sequences, maxlen=maxlen)
    results = loaded_model.predict_classes(padded_sequences)
    results = [de_sentiment_dict[x] for x in results]
    return results

def create_sentence_deep_sentiment_columns(data_frame,language):
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

        language: String
            Review language: "EN" = English; "FR" = French; "DE" = German

        tokenizer_path: String
            path to the tokenizer file

        model_path: String
            path to the model json

        weights_path: String
            path to the weights
    """


    if language in ['EN']:
        tokenizer_path="./SL_Asset_Sentiment/SL_Asset_Sentiment/EN_model/english_tweet_tokenizer.pickle"
        model_path="./SL_Asset_Sentiment/SL_Asset_Sentiment/EN_model/english_tweet_model.json"
        weights_path='./SL_Asset_Sentiment/SL_Asset_Sentiment/EN_model/english_tweet_weights.h5'

    if language in ['FR']:
        tokenizer_path="./SL_Asset_Sentiment/SL_Asset_Sentiment/FR_model/french_tweet_tokenizer.pickle"
        model_path="./SL_Asset_Sentiment/SL_Asset_Sentiment/FR_model/french_tweet_model.json"
        weights_path='./SL_Asset_Sentiment/SL_Asset_Sentiment/FR_model/french_tweet_weights.h5'

    if language in ['DE']:
        tokenizer_path="./SL_Asset_Sentiment/SL_Asset_Sentiment/DE_model/german_tokenizer.pickle"
        model_path="./SL_Asset_Sentiment/SL_Asset_Sentiment/DE_model/german_model.json"
        weights_path='./SL_Asset_Sentiment/SL_Asset_Sentiment/DE_model/german_weights.h5'

    with open(tokenizer_path,'rb') as handle:
        tokenizer = pickle.load(handle)

    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    
    
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(weights_path)
    
    if language in ['EN','FR']:
        sentiment=_sentence_deep_sentiment(list(data_frame["sentences"]),loaded_model = loaded_model, tokenizer = tokenizer)
    elif language in ['DE']:
        sentiment=_sentence_deep_sentiment_de(list(data_frame["sentences"]),loaded_model = loaded_model, tokenizer = tokenizer)
    return sentiment
