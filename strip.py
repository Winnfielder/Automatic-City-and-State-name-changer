# run through the database and remove trailing and leading white spaces

import pandas as pd
from load_write_database import load_dataframe, write_dataframe

provinces = load_dataframe("provinces.yaml")
states = load_dataframe("states.yaml")



states = states.apply(lambda x: x.str.strip())
provinces = provinces.apply(lambda x: x.str.strip())

write_dataframe(states,'states.yaml')
write_dataframe(provinces,'provinces.yaml')