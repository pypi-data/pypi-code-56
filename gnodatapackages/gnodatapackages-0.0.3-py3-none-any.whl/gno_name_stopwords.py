import pandas as pd

def test():
    return ("hello am here at namestopwords")

def gno_inpersonname_remove():
    file = open("gnodatapackages/gnodatapackages/personname_wordsremove_gno.csv", "r", encoding = "utf8", errors = 'backslashreplace')
    NameStopWords = pd.read_csv(file, sep = ",", skipinitialspace = True, keep_default_na = False ,header="infer")
    file.close()
    return NameStopWords


def gno_honorifics_remove():
    file = open("gnodatapackages/gnodatapackages/honorifics_remove_gno.csv", "r", encoding = "utf8", errors = 'backslashreplace')
    NameStopWords = pd.read_csv(file, sep = ",", skipinitialspace = True, keep_default_na = False ,header="infer")
    file.close()
    return NameStopWords