import pandas as pd
import os

def test():
    return ("hello am here at genstopwords")

def gno_generalstopwords():
    cwd = os.getcwd()  # Get the current working directory (cwd)
    path = cwd+"/"+"gen_stopwords_gno.csv"
    file = open(path, "r", encoding = "utf8", errors = 'backslashreplace')
    GenStopWords = pd.read_csv(file, sep = ",", skipinitialspace = True, keep_default_na = False ,header="infer")
    file.close()
    return GenStopWords
    
