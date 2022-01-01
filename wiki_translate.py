# use wikipedia API to fill database
# use to fill up database quickly in the beginning

import wikipediaapi
import pandas as pd
from tqdm import tqdm

provinces = pd.read_csv("provinces.csv", index_col=0)
states = pd.read_csv("states.csv",index_col=0)
wiki_wiki = wikipediaapi.Wikipedia('en')

def translate_dataframe(dataframe,language,language_code):
    print(language)
    for index,row in tqdm(dataframe.iterrows(),total=dataframe.shape[0]):
        if (not pd.isnull(row['english'])):
            english_name = row['english']
            if (pd.isnull(row[language])):
                page_py = wiki_wiki.page(english_name)
                if (language_code in page_py.langlinks):
                    page_py_it = page_py.langlinks[language_code]
                    it_name = page_py_it.title
                    # the is a parentesis remove it
                    if it_name.find('(')!=-1:
                        it_name = it_name[:it_name.find('(')-1]
                    # removes comma
                    if it_name.find(',')!=-1:
                        it_name = it_name[:it_name.find(',')-1]
                    dataframe.loc[index,language] = it_name
    return dataframe

languages = [
#    ('albanian','sq'),
#    ('belarusian','be'),
    ('czech','cs'),
    ('estonian','et'),
    ('finnish','fi'),
#    ('french','fr'),
#    ('german','de'),
#   ('greek','el'),
    ('hungarian','hu'),
    ('latvian','lv'),
    ('lithuanian','lt'),
#    ('polish','pl'),
    ('romanian','ro'),
    ('swedish','sv'),
 #   ('turkish','tr'),
    ('yugoslav','hr'),
]


for language, language_code in languages:
    provinces_wiki = translate_dataframe(provinces,language,language_code)
    provinces_wiki.to_csv("provinces_wiki.csv")
