import pandas as pd
import yaml

def load_dataframe(filepath):
    with open(filepath,'r') as stream:
        df = pd.json_normalize(yaml.safe_load(stream))
        return df.set_index(df.columns[0])

def write_dataframe(dataframe,filepath):
    dict = dataframe.to_dict('records')
    with open(filepath,'w') as file:
        yaml.dump(dict,file,allow_unicode=True)
