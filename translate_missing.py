
# use to fill up database quickly in the beginning


import pandas as pd
import wikipediaapi
from googletrans import Translator
from tqdm import tqdm

from clean_string import clean_string
from supported_language_list import languages, language_code
from google_translate import get_translation
from load_write_database import load_dataframe, write_dataframe

manual_input = False
manual_checking = False

wiki_ref_dict = {}

translator = Translator()

startin_from = 800

# when a wrong english translation use it to fix the other languages
def interactive_check(dataframe, index, wiki_ref, new_name):
    wiki_page_name = new_name
    to_translate = new_name
    print(index, new_name)
    print("\n")
    res = input("other languages wikipedia or google translate? (w/t)")
    if res=='t':
        res3 = input("translating what? (k=keep or insert)")
        if res3!='k':
            to_translate = res3
    if res=='w':
        res4 = input("is the wikipedia page name {} ? (k=keep or insert)".format(wiki_page_name))
        if res4!='k':
            wiki_page_name = res4
    row = dataframe.loc[index]
    page = wiki_ref.page(wiki_page_name)
    for lang,lang_code in languages:
        name_proposal = row[lang]
        if res=='w' and lang_code in page.langlinks:
                name_proposal = page.langlinks[lang_code].title
        else:
            try:
                #name_proposal = ' '.join([translator.translate(word,dest=lang_code).text for word in  to_translate.split(" ")])
                name_proposal = get_translation(to_translate,src='en',dest=lang_code).text
            except ValueError:
                print("{} not possible".format(lang))
        name_proposal = handle_non_latin_alphabets(name_proposal,lang, lang_code)
        name_proposal = clean_string(name_proposal)
        if name_proposal!=row[lang]:
            res2 = input("{} to {} in {}?".format(row[lang],name_proposal,lang))
            if res2 == 'y':
                dataframe.loc[index,lang] = name_proposal
            elif res2!='n':
                dataframe.loc[index,lang] = res2
    return dataframe

def get_wiki_ref(language_code):
    if language_code in wiki_ref_dict:
        return wiki_ref_dict[language_code]
    else:
        wiki_ref_dict[language_code] = wikipediaapi.Wikipedia(language_code)
        return wiki_ref_dict[language_code]


def fill_missing_in_row(dataframe, index):
    row = dataframe.loc[index]
    # Note: only latin alphabet languages
    languages_by_n_articles = [
        ('english', 'en'),
        ('swedish', 'sv'),
        ('german', 'de'),
        ('french', 'fr'),
        ('dutch', 'nl'),
        ('spanish', 'es'),
        ('italian', 'it'),
        ('polish', 'pl'),
        ('portuguese', 'pt')
    ]
    reference_language = languages_by_n_articles[0][0]
    ref_language_code = languages_by_n_articles[0][1]
    if row.isnull().values.any():
        # if the reference languages has the word already transalted
        if (not pd.isnull(row[reference_language])):
            # get it
            reference_name = row[reference_language]
            # Optimization get wikiref only if there is a null
            wiki_ref = get_wiki_ref(ref_language_code)
            dataframe = interactive_check(dataframe, index, wiki_ref, reference_name)
    return dataframe


def handle_non_latin_alphabets(new_name, language,language_code):
    if (language in ['chinese','arab','japanese','belarusian','hindi','russian','greek','ukrainian','bulgarian','armenian','georgian']):
        new_name = get_translation(new_name,dest=language_code).pronunciation
    if (language == 'chinese'):
        new_name = ''.join(new_name.split(" "))
    return new_name

def translate_dataframe(dataframe,filename):
    for index in tqdm(dataframe.index):
            row = dataframe.loc[index]
            new_dataframe = fill_missing_in_row(dataframe,index)
            new_row = new_dataframe.loc[index]
            if not new_row.equals(row):
                dataframe = new_dataframe
                write_dataframe(dataframe,filename)


if __name__ == '__main__':

    provinces = load_dataframe("new_provinces.yaml")
    states = load_dataframe("new_states.yaml")


    provinces_wiki = translate_dataframe(provinces,"new_provinces.yaml")
#    states_wiki = translate_dataframe(states,"new_states.yaml")

