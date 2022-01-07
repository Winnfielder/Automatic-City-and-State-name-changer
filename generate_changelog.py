import pandas as pd

old_provinces = pd.read_csv("provinces.csv", index_col=0)
old_states = pd.read_csv("states.csv",index_col=0)

new_provinces = pd.read_csv("new provinces.csv", index_col=0)
new_states = pd.read_csv("new_states.csv",index_col=0)

languages = [
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
]

print("============ CITIES =================")
for language,_ in languages:
    print("================= {} =================".format(language.capitalize()))
    for index,row in new_provinces.iterrows():
        new_name = row[language]
        if not pd.isnull(new_name):
            if index in old_provinces.index and not pd.isnull(old_provinces.loc[old_provinces.index == index][language].item()):
                old_name = old_provinces.loc[old_provinces.index == index][language].item()
            else:
                old_name = row['english']
            if (new_name!=old_name):
                print("{} -> {}".format(old_name,new_name))
print("============ STATES =================")
for language,_ in languages:
    print("================= {} =================".format(language.capitalize()))
    for index,row in new_states.iterrows():
        new_name = row[language]
        if index in old_states.index:
            old_name = old_states.loc[old_states.index == index][language].item()
        else:
            old_name = row['english']
        if (new_name!=old_name):
            print("{} -> {}".format(old_name,new_name))
