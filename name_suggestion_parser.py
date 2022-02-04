import pandas as pd
from load_write_database import load_dataframe, write_dataframe
from add_entries import add_new_province, add_new_state

filename = "../Dynamic States and Cities Rename/indian_name.txt"
language = "hindi"

states = load_dataframe("states.yaml")
provinces = load_dataframe("provinces.yaml")

starting_line = 0

file = open(filename,"r")
lines = file.readlines()
file.close()

def clear_line(line):
    return line.replace("\n",'').replace('#','').replace('\t','').strip(" ")

def get_name(line):
    line = clear_line(line)
    first_comma = line.find('"')
    second_comma = line[first_comma+1:].find('"')
    return line[first_comma+1:first_comma+second_comma+1]



for line in lines[starting_line:]:
    if line.find("state =")!=-1:
        state_id = int(clear_line(line).split(" ")[-1].strip())
        old_state_name = states.loc[states.index == state_id, language]
    elif line.find("set_state_name")!=-1:
        new_state_name = get_name(line)
        if old_state_name.empty:
            res = input("creating a new state {} called {}?".format(state_id, new_state_name))
            if (res=='y'):
                add_new_state(states, language, new_state_name, state_id)
                old_state_name = new_state_name
                write_dataframe(states,"new_states.yaml")
        else:
            old_state_name = old_state_name.item()
        if (old_state_name!=new_state_name):
            res = input("state {}: renaming {} to {} in {}?".format(state_id, old_state_name, new_state_name, language))
            if (res=='y'):
                states.loc[states.index == state_id, language] = new_state_name
                write_dataframe(states,"new_states.yaml")
            elif res!='n':
                states.loc[states.index == state_id, language] = res
                write_dataframe(states,"new_states.yaml")
            else:
                 new_state_name = old_state_name
    elif line.find("set_province_name")!=-1:
        new_province_name = get_name(line)
        province_id = int(clear_line(line).split(" ")[5])
        old_province_name = provinces.loc[provinces.index==province_id][language]
        if old_province_name.empty:
            # create province
            res = input("creating a new province {} called {} in state?".format(province_id, new_province_name, new_state_name))
            if res=='y':
                add_new_province(provinces, language, new_province_name, state_id, province_id)
                old_province_name = new_province_name
                write_dataframe(provinces,"new_provinces.yaml")
        else:
            old_province_name = old_province_name.item()
        if (old_province_name!=new_province_name):
            res = input("city {}: renaming {} to {} in {}?".format(province_id, old_province_name, new_province_name, language))
            if (res=='y'):
                provinces.loc[provinces.index==province_id,language] = new_province_name
                write_dataframe(provinces,"new_provinces.yaml")
            elif res!='n':
                provinces.loc[provinces.index==province_id,language] = res
                write_dataframe(provinces,"new_provinces.yaml")


