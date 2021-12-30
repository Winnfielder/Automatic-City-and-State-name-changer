# it is important that for at least all the states there is a name,
# so fill it with the english one

import pandas as pd

# change to state or to province
file = 'provinces'

languages = [
    ('albanian','sq'),
    #    ('belarusian','be'),
    ('czech','cs'),
    ('estonian','et'),
    ('finnish','fi'),
    ('french','fr'),
    ('german','de'),
    #   ('greek','el'),
    ('italian','it'),
    ('hungarian','hu'),
    ('latvian','lv'),
    ('lithuanian','lt'),
    ('polish','pl'),
    ('romanian','ro'),
    ('swedish','sv'),
    ('turkish','tr'),
    ('yuguslav','hr'),
]

df = pd.read_csv(file+".csv",index_col=0)


row_index = df['english'].notna()

percent_missing = df[row_index].isnull().sum() * 100 / len(df[row_index])
missing_value_df = pd.DataFrame({'column_name': df.columns,
                                 'percent_missing': percent_missing})


print(missing_value_df)

for language, _ in languages:
    df.loc[row_index,language] = df.loc[row_index,language].fillna(df.loc[row_index,'english'])

percent_missing = df[row_index].isnull().sum() * 100 / len(df[row_index])
missing_value_df = pd.DataFrame({'column_name': df.columns,
                                 'percent_missing': percent_missing})


print(missing_value_df)

df.to_csv(file+"_filled.csv")

