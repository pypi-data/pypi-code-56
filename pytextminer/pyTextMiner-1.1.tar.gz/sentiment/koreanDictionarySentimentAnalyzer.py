# -*- coding: UTF-8 -*-

import io
import re


class DictionarySentimentAnalyzer:
    def __init__(self):
        name = 'DictionarySentimentAnalyzer'
        self.dict_list={}

    def readPolarityDictionary(self, file):
        fh = open(file, mode="r", encoding="utf-8")
        for line in fh:
            fields = line.split(',')
            n_token = ''
            toks = fields[0].split(";")
            for tok in toks:
                n_token += tok.split("/")[0]
            print("element " + n_token + " -- " + fields[len(fields)-2] + " : " + fields[len(fields)-1])
            sent_dict = {}
            sent_dict['word'] = n_token
            sent_dict['polarity'] = fields[len(fields)-2]
            sent_dict['score'] = fields[len(fields)-1].replace("\n","")
            self.dict_list[n_token] = sent_dict

    def readKunsanUDictionary(self, file):
        with open(file, encoding='utf-8-sig', mode='r') as f:
            for line in f:
                fields = line.split('\t')
                escaped = fields[0]
                sent_dict = {}
                if len(fields) < 2: continue

                if escaped not in self.dict_list:
                    sent_dict['word'] = escaped
                    sent_dict['score'] = float(fields[1])
                    print('term ' + escaped + " : " + fields[1])
                    if float(fields[1]) < 0:
                        sent_dict['polarity'] = 'NEG'
                    elif float(fields[1]) > 0:
                        sent_dict['polarity'] = 'POS'
                    else:
                        sent_dict['polarity'] = 'NEU'

                    self.dict_list[escaped] = sent_dict

    def readCurseDictionary(self, file):
        with open(file, encoding='utf-8-sig', mode='r') as f:
            for line in f:
                term = line.strip()
                sent_dict={}
                if term not in self.dict_list:
                    sent_dict['word'] = term
                    sent_dict['score'] = -2.0
                    print('term ' + term)
                    sent_dict['polarity'] = 'NEG'
                    self.dict_list[term] = sent_dict

    def readNegativeDictionary(self, file):
        with open(file, encoding='utf-8-sig', mode='r') as f:
            for line in f:
                term = line.strip()
                sent_dict={}
                if term not in self.dict_list:
                    sent_dict['word'] = term
                    sent_dict['score'] = -1.0
                    print('term ' + term)
                    sent_dict['polarity'] = 'NEG'
                    self.dict_list[term] = sent_dict

    def readPositiveDictionary(self, file):
        with open(file, encoding='utf-8-sig', mode='r') as f:
            for line in f:
                term = line.strip()
                sent_dict={}
                if term not in self.dict_list:
                    sent_dict['word'] = term
                    sent_dict['score'] = 1.0
                    print('term ' + term)
                    sent_dict['polarity'] = 'POS'
                    self.dict_list[term] = sent_dict

    def getSentiDictionary(self):
        return self.dict_list

if __name__ == '__main__':
    import pyTextMiner as ptm
    import io
    import nltk

    sentiAnalyzer = DictionarySentimentAnalyzer()

    file_name = './data/polarity.csv'
    sentiAnalyzer.readPolarityDictionary(file_name)
    file_name = './data/SentiWord_Dict.txt'
    sentiAnalyzer.readKunsanUDictionary(file_name)
    file_name = './data/korean_curse_words.txt'
    sentiAnalyzer.readCurseDictionary(file_name)
    file_name = './data/negative_words_ko.txt'
    sentiAnalyzer.readNegativeDictionary(file_name)
    file_name = './data/positive_words_ko.txt'
    sentiAnalyzer.readPositiveDictionary(file_name)

    dict_list = sentiAnalyzer.getSentiDictionary()

    corpus = ptm.CorpusFromFile('../data/donald.txt')
    pipeline = ptm.Pipeline(ptm.splitter.NLTK(), ptm.tokenizer.Komoran(),
                            ptm.helper.SelectWordOnly(),
                            ptm.helper.StopwordFilter(file='../stopwords/stopwordsKor.txt'))

    result = pipeline.processCorpus(corpus)

    for doc in result:
        for sent in doc:
            total_score = 0.0
            count = 0
            for _str in sent:
                if len(_str) > 0:
                    score = 0.0
                    dictionary_ele = dict_list.get(_str)
                    if (dictionary_ele != None):
                        polarity = dictionary_ele.get('polarity')
                        score = float(dictionary_ele.get('score'))
                        if (polarity == 'NEG'):
                            score = -float(score)
                            count += 1
                        elif (polarity == 'POS'):
                            score = float(score)
                            count += 1
                        #print(_str + " == " + polarity + " " + str(score))
                        total_score += score
                    else:
                        total_score += score

            if (count != 0):
                avg_score = total_score/count
                print("AVG SCORE " + str(avg_score))