# run through the database and remove trailing and leading white spaces

import pandas as pd

provinces = pd.read_csv("provinces.csv", index_col=0, dtype=object)
states = pd.read_csv("states.csv", index_col=0, dtype=object)



states = states.apply(lambda x: x.str.strip())
provinces = provinces.apply(lambda x: x.str.strip())

states.to_csv('states.csv')
provinces.to_csv('provinces.csv')