# i realized a lot of missing translation is because paradox not always use english name for state province, let's fix this


import wikipediaapi
from googletrans import Translator
from tqdm import tqdm

from clean_string import clean_string
from google_translate import get_translation
from load_write_database import load_dataframe, write_dataframe
from translate_missing import fill_missing_in_row, interactive_check

starting_from = 0

translator = Translator()




# fix wrong translations (mostly from paradox) that are not in english
def fix_language(dataframe, filename, language, language_code):
    # get the wiki in the language we need
    language_wiki = wikipediaapi.Wikipedia(language_code)
    # iterate the dataframe from a choosen startin point
    iterator = list(dataframe.iterrows())[starting_from:]
    for index,row in tqdm(iterator,total=len(iterator)):
        # try to search the current name on wikipedia
        current_name = row[language]
        page = language_wiki.page(current_name)
        # if it doens't exists
        if not page.exists():
            print("current name {} does not exists in {} wikipedia!".format(current_name, language))
            # get it from the other languages
            # TODO FIX fill_missing_in_row return now dataframe
            new_name = fill_missing_in_row(dataframe,index)
            if new_name==None:
                print("no wiki found, attempt translation in english")
                # attempt translation
                new_name = get_translation(current_name,dest='en').text
                print("translation in english is ",new_name)
            new_name = clean_string(new_name)
            res = input("changing {} to {} in {}?".format(current_name,new_name,'english'))
            if res=='y':
                dataframe.loc[index,'english'] = new_name
            elif res!='n':
                dataframe.loc[index,'english'] = res
                new_name = res
            else:
                new_name = current_name
            # check other languages interactively
            dataframe = interactive_check(dataframe, index, language_wiki, new_name)
            write_dataframe(dataframe,filename)
    return dataframe

if __name__ == '__main__':

    provinces = load_dataframe("new_provinces.yaml")
    states = load_dataframe("new_states.yaml")

    provinces_wiki = fix_language(provinces, "new_provinces.yaml",'english','en')
    states_wiki = fix_language(states, "new_states.yaml",'english','en')