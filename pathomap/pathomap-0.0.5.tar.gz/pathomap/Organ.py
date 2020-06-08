"""
Miscellaneous information for the pathomap project
"""

import pandas as pd
import pathlib


def gene_values(organ_name, condition='healthy', normalize=False, desc=False, limit=10):
    """
    """
    if condition not in ['pathological', 'healthy']:
        print('Invalid condition. Choose either pathological or healthy')
        return

    if condition == 'pathological':
        filepath = pathlib.Path(__file__).parent / 'data/abstract_gene_weight_matrix.csv'
        with open(filepath) as f:
            df = pd.read_csv(filepath)
            df.rename(columns={"Unnamed: 0": "gene_name"}, inplace=True)

    else:
        filepath = pathlib.Path(__file__).parent / 'data/gene_tissue_similarity.csv'
        with open(filepath) as f:
            df = pd.read_csv(filepath)
            df.rename(columns={"0": "gene_name"}, inplace=True)

    try:
        df = df[['gene_name', organ_name]]
    except Exception as e:
        return 'Exception: Invalid organ name / unavailable data'

    if normalize:
        # apply z-scoring on the df
        df[organ_name] = (df[organ_name] - df[organ_name].mean())/df[organ_name].std(ddof=0)

    if desc:
        df = df.sort_values(by=organ_name, ascending=False)
    df.reset_index(inplace=True, drop=True)

    if limit == -1:
        # return all the values
        return df
    return df.iloc[0:limit]



if __name__ == '__main__':
    print(top_genes('vagina', 'healthy', True))
