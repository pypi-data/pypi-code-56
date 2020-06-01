#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pandastools` package."""

import pandas as pd
import pytest

from pandastools import accessors


def test_uniquify_cols():
    df = pd.DataFrame(dict(a=[1, 2, 5]))
    df2 = df.pt.uniquify_columns()
    assert df.equals(df2)
    df3 = pd.concat([df, df], axis=1)
    df3.pt.uniquify_columns()
    assert df3.columns.to_list() == ["a", "a_2"]
