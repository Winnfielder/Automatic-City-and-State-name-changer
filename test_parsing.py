# check that province and states yaml are parsable and correct, useful for pull request

import pandas as pd

from load_write_database import load_dataframe, write_dataframe

def test_parsing_provinces():
    provinces = load_dataframe("provinces.yaml")

    assert not provinces.empty


def test_parsing_states():
    states = load_dataframe("states.yaml")
    assert not states.empty


