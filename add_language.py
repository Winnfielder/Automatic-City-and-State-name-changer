import argparse
import numpy as np
from translate_missing import get_wiki_ref, get_translation, handle_non_latin_alphabets
from clean_string import clean_string
from tqdm import tqdm

from load_write_database import write_dataframe, write_states, write_provinces, load_states, load_provinces

def process_dataframe(dataframe,filename, language,language_code):
    if language not in dataframe.columns:
        dataframe[language] = np.nan
    eng_wiki = get_wiki_ref('en')
    to_translate = dataframe[~ dataframe[language].notna()]
    for index, row in tqdm(to_translate.iterrows(),total=to_translate.shape[0]):
        eng_name = row['english']
        # wikipedia
        eng_page = eng_wiki.page(eng_name)
        translation = None
        if eng_page.exists():
            if language_code in eng_page.langlinks:
                translation = eng_page.langlinks[language_code].title
        if translation is None:
            # translate
            translation = get_translation(eng_name,language_code,src='en').text
        translation = handle_non_latin_alphabets(translation,language,language_code)
        translation = clean_string(translation)
        dataframe.loc[index,language] = translation
        if index%200 == 0:
            write_dataframe(dataframe,filename)
    return dataframe

def add_language(language,language_code):
    states = load_states()
    provinces = load_provinces()
    print("translating states...")
    new_states = process_dataframe(states,"new_states.yaml",language,language_code)
    write_states(new_states)
    print("translating provinces...")
    new_provinces = process_dataframe(provinces,"new_provinces.yaml",language,language_code)
    write_provinces(new_provinces)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--language',required=True)
    parser.add_argument('--language_code',required=True)

    args = vars(parser.parse_args())

    language = args['language']
    language_code = args['language_code']

    add_language(language,language_code)