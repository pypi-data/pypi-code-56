import pandas as pd

def test():
    return ("hello am here at genstopwords")

def gno_generalstopwords():
    file = open("gnodatapackages/gnodatapackages/gen_stopwords_gno.csv", "r", encoding = "utf8", errors = 'backslashreplace')
    GenStopWords = pd.read_csv(file, sep = ",", skipinitialspace = True, keep_default_na = False ,header="infer")
    file.close()
    return GenStopWords
    
