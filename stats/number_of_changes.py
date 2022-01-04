# generate for each language how many city names and states are different from english (vanilla)


import pandas as pd

provinces = pd.read_csv("../provinces.csv", index_col=0)
states = pd.read_csv("../states.csv", index_col=0)

not_implemented_language = [
    "japanese",
    "arab",
    "chinese",
    "greek",
    "russian",
    "ukrainian",
    "belarusian",
    "bulgarian"
]

languages = set(states.columns)
[languages.remove(lang) for lang in not_implemented_language]
languages.remove("english")

for language in languages:
    state_diff = sum(states[language] != states['english'])
    province_diff = sum(provinces[language] != provinces['english'])
    print("- {}: {} different states names and {} different cities names".format(language,state_diff,province_diff))