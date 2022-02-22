import pandas as pd
import yaml
import os

def load_dataframe(filepath):
    with open(filepath,'r') as stream:
        df = pd.json_normalize(yaml.safe_load(stream))
        return df.set_index(df.columns[0])

def load_provinces():
    if os.path.exists("new_provinces.yaml"):
        return load_dataframe("new_provinces.yaml")
    else:
        return load_dataframe("provinces.yaml")

def load_states():
    if os.path.exists("new_states.yaml"):
        return load_dataframe("new_states.yaml")
    else:
        return load_dataframe("states.yaml")

def write_dataframe(dataframe,filepath):
    dataframe = dataframe.reset_index()
    dict = dataframe.to_dict('records')
    with open(filepath,'w') as file:
        yaml.dump(dict,file,allow_unicode=True)

def write_states(dataframe):
    write_dataframe(dataframe,"new_states.yaml")

def write_provinces(dataframe):
    write_dataframe(dataframe,"new_provinces.yaml")
