# load all dataframe
import unicodedata
import pandas as pd
from load_write_database import load_dataframe, write_dataframe
from supported_language_list import languages

def fix_encoding(dataframe_path):
    dataframe = load_dataframe(dataframe_path)
    for i, row in dataframe.iterrows():
        for language, language_code in languages:
            element = row[language]
            if not pd.isnull(element):
                new_name = unicodedata.normalize('NFKC', element).encode('utf_8','ignore').decode()
                dataframe.loc[i,language] = new_name
    write_dataframe(dataframe,dataframe_path)

#fix_encoding("new_provinces.yaml")
fix_encoding("new_states.yaml")