import unidecode
import unicodedata


def clean_string(new_name):
    new_name = new_name.replace("'","").replace('.','').replace("~","")\
        .replace("=","").replace("/","").replace("-"," ").strip()
    # the is a parentesis remove it
    if new_name.find('(')!=-1:
        new_name = new_name[:new_name.find('(')-1]
    # removes comma
    if new_name.find(',')!=-1:
        new_name = new_name[:new_name.find(',')-1]
    #first make all the string lowercase
    new_name = new_name.lower()
    # then make all the initial letter of each word capital
    new_name = ' '.join(word.capitalize() for word in new_name.split(" "))
    # NOTE very important, hoi4 support utf-8 but with composite character (not NFD or NFKD)
    new_name = unicodedata.normalize('NFKC', new_name).encode('utf_8','ignore').decode()
    return new_name