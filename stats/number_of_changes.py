# generate for each language how many city names and states are different from english (vanilla)


import pandas as pd

provinces = pd.read_csv("../provinces.csv", index_col=0)
states = pd.read_csv("../states.csv", index_col=0)

not_implemented_language = [
    "japanese",
    "arab",
    "ukrainian",
    "belarusian",
    "bulgarian"
]

languages = set(states.columns)
[languages.remove(lang) for lang in not_implemented_language]
languages.remove("english")

stat_list = []

for language in languages:
    state_diff = sum(states[language] != states['english'])
    province_diff = sum(provinces[language] != provinces['english'])
    stat_list.append((state_diff,province_diff,language))

stat_list = sorted(stat_list,key=lambda x:x[0]+x[1],reverse=True)
for state_diff, province_diff, language in stat_list:
    print("- {}: {} different cities names and {} different states names".format(language,province_diff,state_diff))