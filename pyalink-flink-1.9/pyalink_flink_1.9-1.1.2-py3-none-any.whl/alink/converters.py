# -*- coding: utf-8 -*-
import os

import numpy as np
import pandas as pd

from .py4j_util import get_java_class, get_java_gateway

__all__ = ["dataframeToOperator", "collectToDataframes"]

# Basic type conversion
_G_ALINK_TYPE_TO_PTYPE = {
    'BOOL': 'bool',
    'BOOLEAN': 'bool',
    'JAVA.LANG.BOOLEAN': 'bool',

    'TINYINT': 'Int8',
    'BYTE': 'Int8',
    'JAVA.LANG.BYTE': 'Int8',

    'SMALLINT': 'Int16',
    'JAVA.LANG.SHORT': 'Int16',

    'INT': 'Int32',
    'INTEGER': 'Int32',
    'JAVA.LANG.INTEGER': 'Int32',

    'BIGINT': 'Int64',
    'LONG': 'Int64',
    'JAVA.LANG.LONG': 'Int64',

    'FLOAT': 'float32',
    'JAVA.LANG.FLOAT': 'float32',

    'DOUBLE': 'float64',
    'JAVA.LANG.DOUBLE': 'float64',

    'STRING': 'object',
    'VARCHAR': 'object',
    'LONGVARCHAR': 'object',
    'JAVA.LANG.STRING': 'object',

    'DATETIME': 'datetime64',
    'JAVA.SQL.TIMESTAMP': 'datetime64',

    'VEC_TYPES_VECTOR': 'object',
    'COM.ALIBABA.ALINK.COMMON.LINALG.VECTOR': 'object',
    'ANY<COM.ALIBABA.ALINK.COMMON.LINALG.VECTOR>': 'object',

    'VEC_TYPES_DENSE_VECTOR': 'object',
    'COM.ALIBABA.ALINK.COMMON.LINALG.DENSEVECTOR': 'object',
    'ANY<COM.ALIBABA.ALINK.COMMON.LINALG.DENSEVECTOR>': 'object',

    'VEC_TYPES_SPARSE_VECTOR': 'object',
    'COM.ALIBABA.ALINK.COMMON.LINALG.SPARSEVECTOR': 'object',
    'ANY<COM.ALIBABA.ALINK.COMMON.LINALG.SPARSEVECTOR>': 'object'
}


def j_type_to_py_type(t):
    typeclass = t.getTypeClass()
    typeclass_name = typeclass.getName()
    if typeclass_name in ['java.lang.Double', 'java.lang.Float', 'double', 'float']:
        return np.float64
    elif typeclass_name in ['java.lang.Long', 'java.lang.Integer', 'int', 'long']:
        return pd.Int64Dtype()
    elif typeclass_name == 'java.lang.String':
        return np.object
    elif typeclass_name == 'java.sql.Timestamp':
        return np.datetime64
    elif typeclass_name == "com.alibaba.alink.common.linalg.Vector" or typeclass_name == "com.alibaba.alink.common.linalg.DenseVector" or typeclass_name == "com.alibaba.alink.common.linalg.SparseVector":
        return np.str
    elif typeclass_name in ["java.lang.Boolean", 'boolean']:
        return np.bool
    else:
        print("Java type is not supported in Python for automatic conversion of values: %s" % typeclass_name)
        return t


# basic value conversion

def j_value_to_py_value(value):
    import py4j
    if type(value) == py4j.java_collections.JavaArray:  # extract java array
        value = j_array_to_py_list(value)
        if len(value) > 0 and type(value[0]) == py4j.java_collections.JavaArray:  # extract java 2d array
            value = [j_array_to_py_list(row) for row in value]
    elif type(
            value) == py4j.java_gateway.JavaObject and value.getClass().getName() == "org.apache.flink.api.java.tuple.Tuple2":  # extract Tuple2
        return j_array_to_py_list(value.f0), j_array_to_py_list(value.f1)
    return value


# java array <-> python list

def j_array_to_py_list(arr):
    return [d for d in arr]


def py_list_to_j_array(type, num, items):
    arr = get_java_gateway().new_array(type, num)
    for i, item in enumerate(items):
        arr[i] = item
    return arr


# dict -> Params

def dict_to_j_params(d):
    j_params_cls = get_java_class("org.apache.flink.ml.api.misc.param.Params")
    j_params = j_params_cls()
    for (key, value) in d.items():
        j_params.set(key, value)
    return j_params


# Flink rows <-> pd dataframe

def schema_type_to_py_type(raw_type):
    t = raw_type.upper()
    if t in _G_ALINK_TYPE_TO_PTYPE:
        return _G_ALINK_TYPE_TO_PTYPE[t]
    else:
        print("Java type is not supported in Python for automatic conversion of values: %s" % t)
        return np.object


def adjust_dataframe_types(df, colnames, coltypes):
    for (colname, coltype) in zip(colnames, coltypes):
        col = df[colname]
        py_type = schema_type_to_py_type(coltype)
        if not pd.api.types.is_float_dtype(py_type) \
                and not pd.api.types.is_integer_dtype(py_type) \
                and col.isnull().values.any():
            print("Warning: null values exist in column %s, making it cannot be cast to type: %s automatically" % (
                colname, str(coltype)))
            continue
        df = df.astype({colname: py_type}, copy=False, errors='ignore')
    return df


# operator(s) -> dataframe(s)

def csv_content_to_dataframe(content, colnames, coltypes):
    from io import StringIO
    # Parse csv from content
    df = pd.read_csv(StringIO(content), names=colnames,
                     true_values=["True", "true"], false_values=["False", "false"])
    # As all empty strings are read as NaN, we transform them to None
    df = df.where(df.notnull(), None)
    # For float/int columns, there are specialized types to represent values with null values, we adjust their types
    df = adjust_dataframe_types(df, colnames, coltypes)
    return df


def collect_to_dataframes_memory(*ops):
    j_batch_operator_class = get_java_class('com.alibaba.alink.operator.batch.BatchOperator')
    j_op_list = py_list_to_j_array(j_batch_operator_class, len(ops), map(lambda op: op.get_j_obj(), ops))

    line_terminator = os.linesep
    field_delimiter = ","
    quote_char = "\""

    j_operator_csv_collector_cls = get_java_class('com.alibaba.alink.common.utils.OperatorCsvCollector')
    csv_contents = j_operator_csv_collector_cls.collectToCsv(j_op_list, line_terminator, field_delimiter, quote_char)

    return [
        csv_content_to_dataframe(content, ops[index].getColNames(), ops[index].getColTypes())
        for index, content in enumerate(csv_contents)
    ]


def collect_to_dataframes(*ops, **kwargs):
    if len(ops) == 0:
        return []
    return collect_to_dataframes_memory(*ops)


def collectToDataframes(*ops, **kwargs):
    return collect_to_dataframes(*ops, **kwargs)


# dataframe(s) ->  operator(s)

def dataframe_to_operator_memory(df, schema_str, op_type):
    j_csv_util_cls = get_java_class("com.alibaba.alink.operator.common.io.csv.CsvUtil")
    j_col_types = j_csv_util_cls.getColTypes(schema_str)

    df_copy = df.copy()
    for index, col_name in enumerate(df_copy.columns):
        j_col_type = j_col_types[index]
        # If the column is bool type, we need to convert 'True' to 'true', and 'False' to 'false'
        if j_col_type.toString() == "Boolean":
            df_copy[col_name] = df_copy[col_name].apply(lambda x: x if x is None else str(x).lower())

    content = df_copy.to_csv(index=False, header=False)
    j_multi_line_csv_parser = get_java_class("com.alibaba.alink.common.utils.MultiLineCsvParser")

    line_terminator = os.linesep
    field_delimiter = ","
    quote_char = "\""

    if op_type == "batch":
        j_op = j_multi_line_csv_parser.csvToBatchOperator(content, schema_str,
                                                          line_terminator, field_delimiter, quote_char)
        from .batch.base import BatchOperatorWrapper
        wrapper = BatchOperatorWrapper
    else:
        j_op = j_multi_line_csv_parser.csvToStreamOperator(content, schema_str,
                                                           line_terminator, field_delimiter, quote_char)
        from .stream.base import StreamOperatorWrapper
        wrapper = StreamOperatorWrapper
    return wrapper(j_op)


def dataframe_to_operator(df, schema_str, op_type):
    """
    Convert a dataframe to a batch operator in alink.
    If null values exist in df, it is better to provide schema_str, so that the operator can have correct type information.
    :param df:
    :param schema_str: column schema string, like "col1 string, col2 int, col3 boolean"
    :return:
    """
    return dataframe_to_operator_memory(df, schema_str, op_type)


def dataframeToOperator(df, schemaStr, op_type=None, opType=None):
    if opType is None:
        opType = op_type
    if opType not in ["batch", "stream"]:
        raise 'opType %s not supported, please use "batch" or "stream"' % opType
    return dataframe_to_operator(df, schemaStr, opType)
