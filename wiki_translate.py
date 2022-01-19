# use wikipedia API to fill database
# use to fill up database quickly in the beginning

import wikipediaapi
import pandas as pd
from tqdm import tqdm
import pinyin # transliterate chinese
from transliterate import translit
from lang_trans.arabic import arabtex
from googletrans import Translator
import unidecode

provinces = pd.read_csv("provinces.csv", index_col=0)
states = pd.read_csv("states.csv",index_col=0)
reference_language = 'english'
reference_language_code = 'en'
backup_language = 'german'
backup_language_code = 'de'
manual_input = False
manual_checking = False
wiki_wiki = wikipediaapi.Wikipedia(reference_language_code)
wiki_backup = wikipediaapi.Wikipedia(backup_language_code)



def translate_dataframe(dataframe,language,language_code):
    translator = Translator()
    for index,row in tqdm(dataframe.iterrows(),total=dataframe.shape[0]):
        if (not pd.isnull(row[reference_language])):
            reference_name = row[reference_language]
            if (pd.isnull(row[language])):
                page_py = wiki_wiki.page(reference_name)
                if page_py == None:
                    reference_name = row[backup_language]
                    page_py = wiki_backup.page(wiki_backup)
                if (language_code in page_py.langlinks):
                    page_py_loc = page_py.langlinks[language_code]
                elif (backup_language_code in page_py.langlinks):
                    page_py_loc = page_py.langlinks[backup_language_code]
                else:
                    continue
                new_name = page_py_loc.title
                if (language=='chinese'):
                    new_name = pinyin.get(new_name,format="strip",)
                elif (language in ['russian','greek','ukrainian','bulgarian']):
                    new_name = translit(new_name,language_code,reversed=True)
                elif (language in ['arab','japanese','belarusian']):
                    new_name = translator.translate(new_name,dest=language_code).pronunciation
                new_name = unidecode.unidecode(new_name)
                new_name = new_name.replace("'","").replace('.','').replace("~","").replace("=","")
                new_name = new_name.capitalize()
                # the is a parentesis remove it
                if new_name.find('(')!=-1:
                    new_name = new_name[:new_name.find('(')-1]
                # removes comma
                if new_name.find(',')!=-1:
                    new_name = new_name[:new_name.find(',')-1]
                if manual_checking:
                    res = input("{} -> {}".format(reference_name,new_name))
                    if res=='y':
                        dataframe.loc[index,language] = new_name
                else:
                    dataframe.loc[index,language] = new_name
            elif manual_input:
                res = input("cant find {} in {}, what is it?".format(reference_name,language))
                dataframe.loc[index,language] = res
    return dataframe

languages = [
    ('belarusian','be'),
#    ('bulgarian','bg')
#    ('ukrainian','uk')
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
#     ('yugoslav','hr'),
]


for language, language_code in languages:
    provinces_wiki = translate_dataframe(provinces,language,language_code)
    provinces_wiki.to_csv("new_provinces.csv")
    states_wiki = translate_dataframe(states,language,language_code)
    states_wiki.to_csv("new_states.csv")
