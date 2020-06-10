""""Run the whole pipeline
"""
import pandas as pd
from pprint import pprint
from pipeline import pipeline, prepare_NER

# file_location = 'csv.pubmed19n1034.csv'


def run(file_location):
    abstract_df = pd.read_csv(file_location)
    abstract_df = abstract_df.dropna()
    
    classification_result_dict = dict()
    NER_result_dict = dict()
    
    for _, row in abstract_df.iterrows():
        temp_result = pipeline(row['abstract'])
        if temp_result is not None:
            temp_title = row['title']
            classification_result_dict[temp_title] = temp_result

            NER_result_dict[temp_title] = prepare_NER(temp_result)
        
        # Prepare for the NER
    return classification_result_dict, NER_result_dict

