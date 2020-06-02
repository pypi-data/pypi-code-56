import json
from pathlib import Path

import pytest

from syntaxgym import Suite


@pytest.fixture
def suite_regression_20200602():
    return Suite.from_dict(json.load((Path(__file__).parent / "mvrr.json").open()))


def test_prediction_eval(suite_regression_20200602):
    p = suite_regression_20200602.predictions[0]
    item = suite_regression_20200602.items[9]
    from pprint import pprint
    # pprint(item)
    print(p)

    raise RuntimeError
