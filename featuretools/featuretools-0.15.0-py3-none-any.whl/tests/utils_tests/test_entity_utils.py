import pandas as pd

import featuretools as ft
from featuretools import variable_types as vtypes
from featuretools.utils.entity_utils import (
    convert_all_variable_data,
    convert_variable_data,
    get_linked_vars,
    infer_variable_types
)


def test_infer_variable_types():

    df = pd.DataFrame({'id': [0, 1, 2],
                       'category': ['a', 'b', 'a'],
                       'ints': ['1', '2', '1'],
                       'boolean': [True, False, True],
                       'date': ['3/11/2000', '3/12/2000', '3/13/2000'],
                       'integers': [1, 2, 1],
                       'link_var': [1, 2, 1],
                       'integers_category': [1, 2, 1],
                       'integers_object_dtype': [1, 2, 1]})

    df['integers_category'] = df['integers_category'].astype('category')
    df['integers_object_dtype'] = df['integers_object_dtype'].astype('object')
    variable_types = {'id': vtypes.Index}

    inferred_variable_types = infer_variable_types(df=df,
                                                   link_vars=["link_var"],
                                                   variable_types=variable_types,
                                                   time_index=None,
                                                   secondary_time_index={})

    # Check columns' types
    assert "id" not in inferred_variable_types
    assert inferred_variable_types['category'] == vtypes.Categorical
    assert inferred_variable_types['ints'] == vtypes.Categorical
    assert inferred_variable_types['boolean'] == vtypes.Boolean
    assert inferred_variable_types['date'] == vtypes.Datetime
    assert inferred_variable_types['integers'] == vtypes.Numeric
    assert inferred_variable_types['link_var'] == vtypes.Categorical
    assert inferred_variable_types['integers_category'] == vtypes.Categorical
    assert inferred_variable_types['integers_object_dtype'] == vtypes.Categorical

    # Check columns' number
    assert len(variable_types) + len(inferred_variable_types) == len(df.columns)


def test_infer_variable_types_empty_df():
    # test empty dataframe
    empty_df = pd.DataFrame({
        "id": [],
        "empty_int": [],
        "empty_category": [],
        "empty_object": [],
        "empty_date": [],
        "empty_boolean": [],
    })

    empty_df['empty_int'] = empty_df['empty_int'].astype('int')
    empty_df['empty_category'] = empty_df['empty_category'].astype('category')
    empty_df['empty_object'] = empty_df['empty_object'].astype('object')
    empty_df['empty_date'] = empty_df['empty_date'].astype('datetime64[ns]')
    empty_df['empty_boolean'] = empty_df['empty_boolean'].astype(bool)
    variable_types = {'id': vtypes.Index}

    inferred_variable_types = infer_variable_types(df=empty_df,
                                                   variable_types=variable_types,
                                                   link_vars=[],
                                                   time_index=None,
                                                   secondary_time_index={})

    # Check columns' types
    assert "id" not in inferred_variable_types
    assert inferred_variable_types['empty_int'] == vtypes.Numeric
    assert inferred_variable_types['empty_category'] == vtypes.Categorical
    assert inferred_variable_types['empty_object'] == vtypes.Categorical
    assert inferred_variable_types['empty_boolean'] == vtypes.Boolean
    assert inferred_variable_types['empty_date'] == vtypes.Datetime

    # Check columns' number
    assert len(variable_types) + len(inferred_variable_types) == len(empty_df.columns)


def test_convert_all_variable_data():

    df = pd.DataFrame({'id': [0, 1, 2],
                       'category': ['a', 'b', 'a'],
                       'ints': ['1', '2', '1'],
                       'boolean': [True, False, True],
                       'date': ['3/11/2000', '3/12/2000', '3/13/2000'],
                       'integers': [1, 2, 1]})

    variable_types = {
        'id': vtypes.Numeric,
        'category': vtypes.Categorical,
        'ints': vtypes.Numeric,
        'boolean': vtypes.Boolean,
        'date': vtypes.Datetime,
        'integers': vtypes.Numeric
    }

    df = convert_all_variable_data(df, variable_types)

    assert df['id'].dtype.name in vtypes.PandasTypes._pandas_numerics
    assert df['category'].dtype.name == 'object'
    assert df['ints'].dtype.name in vtypes.PandasTypes._pandas_numerics
    assert df['boolean'].dtype.name == 'bool'
    assert df['date'].dtype.name in vtypes.PandasTypes._pandas_datetimes
    assert df['integers'].dtype.name in vtypes.PandasTypes._pandas_numerics


def test_convert_variable_data():

    df = pd.DataFrame({'id': [0, 1, 2],
                       'category': ['a', 'b', 'a'],
                       'ints': ['1', '2', '1'],
                       'boolean': [True, False, True],
                       'date': ['3/11/2000', '3/12/2000', '3/13/2000'],
                       'integers': [1, 2, 1]})

    # Categorical -> Numeric
    init_dtype = df['ints'].dtype.name
    df = convert_variable_data(df=df,
                               column_id='ints',
                               new_type=vtypes.Numeric)

    assert init_dtype != df['ints'].dtype.name
    assert df['ints'].dtype.name in vtypes.PandasTypes._pandas_numerics

    # Numeric -> Boolean
    init_dtype = df['ints'].dtype.name
    df = convert_variable_data(df=df,
                               column_id='ints',
                               new_type=vtypes.Boolean,
                               true_val=1,
                               false_val=2)

    assert init_dtype != df['ints'].dtype.name

    # Categorical -> Datetime
    init_dtype = df['date'].dtype.name
    df = convert_variable_data(df=df,
                               column_id='date',
                               new_type=vtypes.Datetime)

    assert init_dtype != df['date'].dtype.name
    assert df['date'].dtype.name in vtypes.PandasTypes._pandas_datetimes


def test_get_linked_vars():
    es = ft.demo.load_mock_customer(return_entityset=True)

    transactions_linked_vars = get_linked_vars(es['transactions'])
    assert transactions_linked_vars == ['product_id', 'session_id']

    products_linked_vars = get_linked_vars(es['products'])
    assert products_linked_vars == ['product_id']

    sessions_linked_vars = get_linked_vars(es['sessions'])
    assert sessions_linked_vars == ['session_id', 'customer_id']

    customers_linked_vars = get_linked_vars(es['customers'])
    assert customers_linked_vars == ['customer_id']
