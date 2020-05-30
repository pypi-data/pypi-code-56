import pandas as pd
from pandashape import Columns
from pandashape.describers.GeneralDescriber import GeneralDescriber
from pandashape.internal.TransformerExecutor import TransformerExecutor


class PandaShaper:
    def __init__(self, df, inplace=False):
        assert(isinstance(df, pd.DataFrame))
        self.df = df.copy() if not inplace else df

    def describe(self, columnDefinitions=None):
        messages = []
        if columnDefinitions is None:
            describer = GeneralDescriber(self.df)
            messages.extend(describer.describe())

        print("########### PANDASHAPE REPORT ###########")
        print()
        print(f"*** {describer.get_section_header()} ***")
        for message in messages:
            print(message)
        print()

    def transform(self, columnDefinitions):
        executor = TransformerExecutor()
        newColumns = executor.transform(self.df, columnDefinitions)
        print(newColumns)
