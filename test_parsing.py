# check that province and states csv are parsable and correct, useful for pull request

import pandas as pd

def test_parsing_provinces():
    provinces = pd.read_csv("provinces.csv", index_col=0)

    assert not provinces.empty


def test_parsing_states():
    states = pd.read_csv("states.csv", index_col=0)
    assert not states.empty


