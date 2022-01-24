# print some general stats about the translation

import pandas as pd


from load_write_database import load_dataframe, write_dataframe

states = load_dataframe("states.yaml")
provinces = load_dataframe("provinces.yaml")


provinces = provinces[provinces['english'].notna()]
province_size = provinces.shape[0] * provinces.shape[1]
province_not_filled = provinces.isna().sum().sum()
province_filled = province_size-province_not_filled
print("filled {:.2f}% of provinces".format((province_filled/province_size)*100))


percent_missing = provinces.isnull().sum() * 100 / len(provinces)
missing_value_df = pd.DataFrame({'column_name': provinces.columns,
                                 'percent_missing': percent_missing})
print(missing_value_df)

states_size = states.shape[0] * states.shape[1]
states_not_filled = states.isna().sum().sum()
states_filled = states_size-states_not_filled
print("filled {:.2f}% of states".format((states_filled/states_size)*100))

percent_missing = states.isnull().sum() * 100 / len(states)
missing_value_df = pd.DataFrame({'column_name': states.columns,
                                 'percent_missing': percent_missing})
print(missing_value_df)

provinces = provinces.drop('StateID',axis=1)

max_index = 0
max_num = 0
max_names = None
for index, row in provinces.iterrows():
    if not pd.isnull(row['english']):
        row = row.dropna()
        names = set(row)
        num_names = len(names)
        if (num_names>max_num):
            max_index = index
            max_num = num_names
            max_names = names

print("the city with most names is the province {} with {}: {}".format(max_index,max_num,max_names))

max_index = 0
max_num = 0
max_names = None
for index, row in states.iterrows():
    if not pd.isnull(row['english']):
        row = row.dropna()
        names = set(row)
        num_names = len(names)
        if (num_names>max_num):
            max_index = index
            max_num = num_names
            max_names = names

print("the state with most names is the state {} with {}: {}".format(max_index,max_num,max_names))
