# use wikipedia API to fill database
# use to fill up database quickly in the beginning

import wikipediaapi
import pandas as pd
from tqdm import tqdm
import pinyin # transliterate chinese
from transliterate import translit

provinces = pd.read_csv("provinces.csv", index_col=0)
states = pd.read_csv("states.csv",index_col=0)
wiki_wiki = wikipediaapi.Wikipedia('en')

def translate_dataframe(dataframe,language,language_code):
    for index,row in tqdm(dataframe.iterrows(),total=dataframe.shape[0]):
        if (not pd.isnull(row['english'])):
            english_name = row['english']
            if (pd.isnull(row[language])):
                page_py = wiki_wiki.page(english_name)
                if (language_code in page_py.langlinks):
                    page_py_it = page_py.langlinks[language_code]
                    new_name = page_py_it.title
                    if (language=='chinese'):
                        new_name = pinyin.get(new_name,format="strip",)
                    if (language=='russian' or language=='greek'):
                        new_name = translit(new_name,language_code,reversed=True)
                    # the is a parentesis remove it
                    if new_name.find('(')!=-1:
                        new_name = new_name[:new_name.find('(')-1]
                    # removes comma
                    if new_name.find(',')!=-1:
                        new_name = new_name[:new_name.find(',')-1]
                    print("{} -> {}".format(english_name,new_name))
                    dataframe.loc[index,language] = new_name
    return dataframe

languages = [
#    ('chinese','zh'),
#    ('spanish','es'),
#    ('portuguese','pt'),
    ('russian','ru'),
#    ('dutch','nl')
#    ('albanian','sq'),
#    ('belarusian','be'),
#    ('czech','cs'),
#    ('estonian','et'),
#    ('finnish','fi'),
#    ('french','fr'),
#    ('german','de'),
   ('greek','el'),
#    ('hungarian','hu'),
#    ('latvian','lv'),
#    ('lithuanian','lt'),
#    ('polish','pl'),
#    ('romanian','ro'),
#    ('swedish','sv'),
 #   ('turkish','tr'),
#    ('yugoslav','hr'),
]


for language, language_code in languages:
    provinces_wiki = translate_dataframe(provinces,language,language_code)
    provinces_wiki.to_csv("provinces.csv")
    states_wiki = translate_dataframe(states,language,language_code)
    states_wiki.to_csv("states.csv")
