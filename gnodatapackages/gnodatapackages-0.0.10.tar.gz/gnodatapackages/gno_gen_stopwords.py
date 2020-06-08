import pandas as pd
import os

def test():
    print(__file__)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, "gen_stopwords_gno.csv")
    print(filepath)
    return ("hello am here at genstopwords")

def gno_generalstopwords():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, "gen_stopwords_gno.csv")
    print(filepath)
    file = open(filepath, "r", encoding = "utf8", errors = 'backslashreplace')
    GenStopWords = pd.read_csv(file, sep = ",", skipinitialspace = True, keep_default_na = False ,header="infer")
    file.close()
    return GenStopWords
    
