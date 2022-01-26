
# use to fill up database quickly in the beginning


import wikipediaapi
import pandas as pd
from tqdm import tqdm
from googletrans import Translator

from clean_string import clean_string
from google_translate import get_translation
from load_write_database import load_dataframe, write_dataframe


manual_input = False
manual_checking = False

wiki_ref_dict = {}

translator = Translator()

def get_wiki_ref(language_code):
    if language_code in wiki_ref_dict:
        return wiki_ref_dict[language_code]
    else:
        wiki_ref_dict[language_code] = wikipediaapi.Wikipedia(language_code)
        return wiki_ref_dict[language_code]

def get_localized_name(row, language, language_code):
    new_name = None
    # Note: only latin alphabet languages
    languages_by_n_articles = [
        ('english','en'),
        ('swedish','sv'),
        ('german','de'),
        ('french','fr'),
        ('dutch','nl'),
        ('spanish','es'),
        ('italian','it'),
        ('polish','pl'),
        ('portuguese','pt')
    ]

    for reference_language, ref_language_code in languages_by_n_articles:
        if (not pd.isnull(row[reference_language])):
            reference_name = row[reference_language]
            # otherwise get wiki_page in the reference language
            wiki_ref = get_wiki_ref(ref_language_code)
            page_py = wiki_ref.page(reference_name)
            if page_py.exists() and language_code in page_py.langlinks:
                page_py_loc = page_py.langlinks[language_code].title
                if manual_checking:
                    res = input("{} -> {}".format(reference_name,page_py_loc))
                    if res=='y':
                        new_name = page_py_loc
                else:
                    new_name = page_py_loc
                break
    # if still the name is not found get trasnlation from english
    if new_name is None:
        new_name = get_translation(row['english'],dest=language_code).text
    new_name = handle_non_latin_alphabets(new_name,language,language_code)
    return new_name


def handle_non_latin_alphabets(new_name, language,language_code):
    if (language in ['chinese','arab','japanese','belarusian','hindi','russian','greek','ukrainian','bulgarian','armenian','georgian']):
        new_name = get_translation(new_name,dest=language_code).pronunciation
    return new_name

def translate_dataframe(dataframe,language,language_code,filename):
    for index,row in tqdm(dataframe.iterrows(),total=dataframe.shape[0]):
        if (pd.isnull(row[language])):
            new_name = get_localized_name(row, language, language_code)
            if new_name!=None:
                new_name = clean_string(new_name)
                #print(new_name)
                dataframe.loc[index,language] = new_name
                write_dataframe(dataframe,filename)
    #return dataframe

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
    ('hindi','hi'),
    ('danish','da'),
    ('norwegian','no')
]


if __name__ == '__main__':

    provinces = load_dataframe("new_provinces.yaml")
    states = load_dataframe("new_states.yaml")

#    for language, language_code in languages:
 #       provinces_wiki = translate_dataframe(provinces,language,language_code,"new_provinces.yaml")
    for language, language_code in languages:
        states_wiki = translate_dataframe(states,language,language_code,"new_states.yaml")

