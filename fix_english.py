# i realized a lot of missing translation is because paradox not always use english name for state province, let's fix this


from load_write_database import load_dataframe, write_dataframe
from translate_missing import get_localized_name, handle_non_latin_alphabets
from clean_string import clean_string
from google_translate import get_translation
import wikipediaapi
from tqdm import tqdm
from googletrans import Translator
import numpy as np

starting_from = 610 + 13

translator = Translator()

languages = [
        ('belarusian','be'),
        ('bulgarian','bg'),
        ('ukrainian','uk'),
        ('arab','ar'),
        ('japanese','ja'),
   #    ('english','en'),
         ('chinese','zh'),
         ('spanish','es'),
         ('portuguese','pt'),
         ('russian','ru'),
         ('dutch','nl'),
         ('italian','it'),
         ('albanian','sq'),
         ('czech','cs'),
         ('estonian','et'),
         ('finnish','fi'),
         ('french','fr'),
         ('german','de'),
        ('greek','el'),
         ('hungarian','hu'),
         ('latvian','lv'),
         ('lithuanian','lt'),
         ('polish','pl'),
         ('romanian','ro'),
         ('swedish','sv'),
        ('turkish','tr'),
        ('yugoslav','hr'),
       ('hindi','hi'),
    ('danish','da'),
    ('norwegian','no')
]

# when a wrong english translation use it to fix the other languages
def check_all_other_languages(dataframe, index,english_wiki,new_name):
    wiki_page_name = new_name
    res = input("other languages wikipedia or google translate? (w/t)")
    if res=='t':
        res3 = input("translating what? (k=keep or insert)")
        if res3=='k':
            to_translate = new_name
        else:
            to_translate = res3
    if res=='w':
        res4 = input("is the wikipedia page name {} ? (k=keep or insert)".format(wiki_page_name))
        if res4!='k':
            wiki_page_name = res4
    row = dataframe.loc[index]
    page = english_wiki.page(wiki_page_name)
    for lang,lang_code in languages:
        name_proposal = row[lang]
        if res=='w':
            if lang_code in page.langlinks:
                name_proposal = page.langlinks[lang_code].title
                handle_non_latin_alphabets(name_proposal,lang,lang_code)
                name_proposal = clean_string(name_proposal)
        elif res=='t':
            try:
                #name_proposal = ' '.join([translator.translate(word,dest=lang_code).text for word in  to_translate.split(" ")])
                name_proposal = get_translation(to_translate,dest=lang_code).text
            except ValueError:
                print("{} not possible".format(lang))
            name_proposal = handle_non_latin_alphabets(name_proposal,lang, lang_code)
            name_proposal = clean_string(name_proposal)
        if name_proposal!=row[lang]:
            # TODO remove this is only for speed
            if res=='t':
                if lang not in ['chinese','dutch']:
                    dataframe.loc[index,lang] = name_proposal
                continue
            res2 = input("{} to {} in {}?".format(row[lang],name_proposal,lang))
            if res2 == 'y':
                dataframe.loc[index,lang] = name_proposal
            elif res2!='n':
                dataframe.loc[index,lang] = res2
    return dataframe


def fix_english(dataframe,filename):
    english_wiki = wikipediaapi.Wikipedia('en')
    iterator = list(dataframe.iterrows())[starting_from:]
    for index,row in tqdm(iterator,total=len(iterator)):
        old_name = row['english']
        page = english_wiki.page(old_name)
        if not page.exists():
            print(old_name," does not exists!")
            new_name = get_localized_name(row, 'english', 'en')
            if new_name==None:
                print("no wiki found, attempt translation in english")
                # attempt translation
                new_name = get_translation(old_name,dest='en').text
                print("translation in english is ",new_name)
            new_name = clean_string(new_name)
            res = input("changing {} to {} in {}?".format(old_name,new_name,'english'))
            if res=='y':
                dataframe.loc[index,'english'] = new_name
            elif res!='n':
                dataframe.loc[index,'english'] = res
                new_name = res
            else:
                new_name = old_name
            # check other languages interactively
            dataframe = check_all_other_languages(dataframe,index,english_wiki,new_name)
            write_dataframe(dataframe,filename)
    return dataframe

if __name__ == '__main__':

    provinces = load_dataframe("new_provinces.yaml")
    states = load_dataframe("new_states.yaml")

 #   provinces_wiki = fix_english(provinces,"new_provinces.yaml")
    states_wiki = fix_english(states,"new_states.yaml")