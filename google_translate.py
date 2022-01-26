# only use google translate, not wikipedia faster


import pandas as pd
from googletrans import Translator
from tqdm import tqdm
from clean_string import clean_string
from load_write_database import load_dataframe, write_dataframe

translator = Translator()

def get_translation(word,dest,src=None):
    if dest=='zh':
        dest='zh-CN'
    if src!=None:
        return translator.translate(word,src=src,dest=dest)
    else:
        return translator.translate(word,dest=dest)

def translate_dataframe(dataframe,language,language_code):
    for index,row in tqdm(dataframe.iterrows(),total=dataframe.shape[0]):
        if (pd.isnull(row[language])):
            reference_name = row[reference_lang]
            new_name = translator.translate(reference_name,dest=language_code)
            if (language not in ['hindi']):
                new_name = new_name.text
            else:
                new_name = new_name.pronunciation
            new_name = clean_string(new_name)
            if new_name!=None:
                if (new_name!=reference_name):
                    print("{} -> {}".format(reference_name,new_name))
                dataframe.loc[index,language] = new_name
    return dataframe

languages = [
    #    ('belarusian','be'),
    #    ('bulgarian','bg'),
    #    ('ukrainian','uk'),
    #    ('arab','ar'),
    #    ('japanese','ja'),
    #   ('english','en'),
    #     ('chinese','zh'),
    #     ('spanish','es'),
    #     ('portuguese','pt'),
    #     ('russian','ru'),
    #     ('dutch','nl'),
    #     ('italian','it'),
    #     ('albanian','sq'),
    #     ('czech','cs'),
    #     ('estonian','et'),
    #     ('finnish','fi'),
    #     ('french','fr'),
    #     ('german','de'),
    #    ('greek','el'),
    #     ('hungarian','hu'),
    #     ('latvian','lv'),
    #     ('lithuanian','lt'),
    #     ('polish','pl'),
    #     ('romanian','ro'),
    #     ('swedish','sv'),
    #    ('turkish','tr'),
    #    ('yugoslav','hr'),
    #   ('hindi','hi'),
    ('danish','da'),
    ('norwegian','no')
]

if __name__ == "__main__":

    provinces = load_dataframe("provinces.yaml")
    states = load_dataframe("states.yaml")
    reference_lang = 'english'

    for language, language_code in languages:
        translated_provinces = translate_dataframe(provinces, language, language_code)
        write_dataframe(translated_provinces,"new_provinces.yaml")
        states_wiki = translate_dataframe(states,language,language_code)
        states_wiki.to_csv("new_states.csv")
