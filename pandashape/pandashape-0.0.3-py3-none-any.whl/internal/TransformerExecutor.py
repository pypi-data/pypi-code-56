from pandas import DataFrame
from pandashape import Columns
from pandashape.transformers import GenericTransformer
from pandashape.internal import listify


class TransformerExecutor:
    def validate(self, df, columnDefinitions):
        for columnDef in columnDefinitions:
            for transformer in columnDef['transformers']:
                assert(isinstance(transformer, GenericTransformer))

    def transform(self, df, columnDefinitions):
        # convert the definitions to an array (so people can pass
        # either an array of definitions or just one)
        columnDefinitions = listify(columnDefinitions)

        # loop the definitions and resolve which columns are being targeted
        # (could be Columns.All, a single column name, or an array of them)
        for columnDef in columnDefinitions:
            transformColumns = []
            if columnDef['columns'] == Columns.All:
                transformColumns = df[df.columns]
            elif columnDef['columns'] == Columns.Numeric:
                transformColumns = df[df.select_dtypes(
                    include='number').columns]
            else:
                # note that this covers both a single string column name or an array of them
                transformColumns = df[columnDef['columns']]

        # if the user only passed a single column name for this def, it's possible that transformColumns
        # is a single series rather than an list of series - coerce to list
        transformColumns = listify(transformColumns)

        # transform all targeted columns
        columnsToReturn = []

        for transformColumn in transformColumns:
            columnsToReturn.append(
                self.__transformColumn(
                    transformColumn,
                    listify(columnDef['transformers'])
                )
            )

        print("columns to return", columnsToReturn)
        return columnsToReturn

    def __transformColumn(self, column, transformers):
        for transformer in transformers:
            column = transformer.transform(column)

        return column
