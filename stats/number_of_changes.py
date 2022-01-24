# generate for each language how many city names and states are different from english (vanilla)


import pandas as pd

from load_write_database import load_dataframe, write_dataframe

states = load_dataframe("states.yaml")
provinces = load_dataframe("provinces.yaml")

languages = set(states.columns)
languages.remove("english")

stat_list = []

for language in languages:
    state_diff = sum(states[language] != states['english'])
    province_diff = sum(provinces[language] != provinces['english'])
    stat_list.append((state_diff,province_diff,language))

print("[table] [tr] [th]Language[/th] [th]Different city names[/th] [th]Different state names[/th] [/tr]")
stat_list = sorted(stat_list,key=lambda x:x[0]+x[1],reverse=True)
for state_diff, province_diff, language in stat_list:
    print("[tr] [th] {} [/th] [th] {} [/th] [th] {} [/th] [/tr] ".format(language,province_diff,state_diff))
print("[/table]")