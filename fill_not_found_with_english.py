# it is important that for at least all the states there is a name,
# so fill it with the english one

import pandas as pd
from load_write_database import load_dataframe, write_dataframe

languages = [
    #    ('english','en')
    ('belarusian','be'),
    ('bulgarian','bg'),
    ('ukrainian','uk'),
    ('japanese','ja'),
    ('arab','ar'),
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

# fill not found shuld be done only with states
for file in ["states"]:

    df = load_dataframe(file+".yaml")


    row_index = df['english'].notna()

    percent_missing = df[row_index].isnull().sum() * 100 / len(df[row_index])
    missing_value_df = pd.DataFrame({'column_name': df.columns,
                                     'percent_missing': percent_missing})


    for language, _ in languages:
        df.loc[row_index,language] = df.loc[row_index,language].fillna(df.loc[row_index,'english'])

    percent_missing = df[row_index].isnull().sum() * 100 / len(df[row_index])
    missing_value_df = pd.DataFrame({'column_name': df.columns,
                                     'percent_missing': percent_missing})

    print(missing_value_df)

    write_dataframe(df,file+".yaml")

