import os, shutil
from zipfile import ZipFile

root_mod_dir = os.path.expanduser("~/.local/share/Paradox Interactive/Hearts of Iron IV/mod/")
mod_zip = os.path.join(root_mod_dir, "TWR_Localized_State_and_City_names")

if os.path.exists(mod_zip):
    os.remove(mod_zip)

shutil.make_archive(mod_zip, 'zip', root_dir=os.getcwd(),base_dir="common")
zipObj = ZipFile(mod_zip+".zip", 'a')
zipObj.write("descriptor.mod")

zipObj.close()

mod_file_dist = os.path.join(root_mod_dir, "TWR_Localized_State_and_City_names.mod")
if os.path.exists(mod_file_dist):
    os.remove(mod_file_dist)
shutil.copyfile("descriptor.mod", mod_file_dist)

exp = 1  # the line where text need to be added or exp that calculates it for ex %2

with open(mod_file_dist, 'r') as f:
    lines = f.readlines()

with open(mod_file_dist, 'w', encoding='utf8') as f:
    for i, line in enumerate(lines):
        if i == exp:
            f.write('archive="{}.zip"\n'.format(mod_zip))
        f.write(line)
