import os

import pandas as pd
from tqdm import tqdm
from load_write_database import load_dataframe, write_dataframe

states = load_dataframe("states.yaml")
provinces = load_dataframe("provinces.yaml")

languages = set(states.columns)

scripted_effects_folder = "common/scripted_effects"
if not os.path.exists(scripted_effects_folder):
    os.makedirs(scripted_effects_folder)

root_template = """apply_{}_endonyms = {{
    {}
}}
"""

state_template = """
if = {{
		limit = {{
			state = {}
			NOT = {{ has_state_flag = state_name_{} }}
		}}
		set_state_name = "{}"
		
		set_state_flag = state_name_{}
		{}
		
		{}
	}}
"""

clr_template = """
		clr_state_flag = state_name_{}"""

province_template = """
		set_province_name = {{ id = {} name = "{}" }}"""

# for each language
for language in tqdm(languages):
    dest_file = os.path.join(scripted_effects_folder, "endonyms_{}.txt".format(language))
    with open(dest_file, 'w') as file:
        clear_string = "".join([clr_template.format(lang) for lang in languages.difference(language)])
        state_string = ""
        for index, state_row in states.iterrows():
            translated_name = state_row[language]
            # get all the provinces of that state
            state_provices = provinces[provinces['StateID'] == index]
            # null removal
            state_provices = state_provices[state_provices[language].notna()]
            province_string = ""
            for provinceID, province_row in state_provices.iterrows():
                province_string += province_template.format(provinceID, province_row[language])
            state_string += state_template.format(index, language, translated_name, language, clear_string, province_string)
        file.write(root_template.format(language, state_string))
