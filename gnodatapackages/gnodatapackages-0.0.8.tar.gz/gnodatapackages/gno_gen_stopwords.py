import pandas as pd
import os

def test():
    print(__file__)
    return ("hello am here at genstopwords")

def gno_generalstopwords():
    file = open("gnodatapackages/gnodatapackages/gen_stopwords_gno.csv", "r", encoding = "utf8", errors = 'backslashreplace')
    GenStopWords = pd.read_csv(file, sep = ",", skipinitialspace = True, keep_default_na = False ,header="infer")
    file.close()
    return GenStopWords
    
