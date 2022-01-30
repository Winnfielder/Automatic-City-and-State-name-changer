import pandas as pd
from load_write_database import load_dataframe, write_dataframe
import os

def add_new_province(dataframe,language,new_province_name,state,province_id):
    if province_id not in dataframe.index:
        new_row = pd.Series({language:new_province_name,'StateID':state},name=province_id)
        dataframe = dataframe.append(new_row)
    else:
        print("warning provice already exists")
    return dataframe

def add_new_state(dataframe, language, new_state_name, state_id):
    if state_id  in dataframe.index:
        new_row = pd.Series({language:new_state_name}, name=state_id)
        dataframe = dataframe.append(new_row)
    else:
        print("warning state already exists")
    return dataframe

if __name__ == '__main__':
    res = input("inserting provinces or states? (p/s)")
    if os.path.exists("new_provinces.yaml"):
        provinces = load_dataframe("new_provinces.yaml")
    else:
        provinces = load_dataframe("provinces.yaml")
    if os.path.exists("new_states.yaml"):
        states = load_dataframe("new_states.yaml")
    else:
        states = load_dataframe("states.yaml")
    if (res=='p'):
        res2 = int(input("how many provinces?"))
        for _ in range(res2):
            state_id = int(input("state ID"))
            province_id = int(input("province ID"))
            province_name = input("province name in english")
            if (state_id not in states.index):
                print("warning, state id not in state database")
            add_new_province(provinces,'english', province_name, state_id, province_id)
        write_dataframe(provinces,"new_provinces.yaml")
    elif (res=='s'):
        res2 = int(input("how many states?"))
        for _ in range(res2):
            state_id = int(input("state ID"))
            state_name = input("state name in english")
            add_new_state(states,'english',state_name,state_id)
        write_dataframe(states,"new_states.yaml")