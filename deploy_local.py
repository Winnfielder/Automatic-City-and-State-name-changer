import os, shutil
from zipfile import ZipFile

deploy_as_zip = False

root_mod_dir = os.path.expanduser("~/.local/share/Paradox Interactive/Hearts of Iron IV/mod/")
mod_dest_name = os.path.join(root_mod_dir, "Automatic City and State name changer")
if os.path.exists(mod_dest_name):
    shutil.rmtree(mod_dest_name)

if deploy_as_zip:

    shutil.make_archive(mod_dest_name, 'zip', root_dir=os.getcwd(), base_dir="common")
    zipObj = ZipFile(mod_dest_name + ".zip", 'a')
    zipObj.write("descriptor.mod")
    zipObj.write("thumbnail.png")

    zipObj.close()

else:

    shutil.copytree("common",os.path.join(mod_dest_name,"common"))
    shutil.copy("descriptor.mod",os.path.join(mod_dest_name,"descriptor.mod"))
    shutil.copy("thumbnail.png",os.path.join(mod_dest_name,"thumbnail.png"))




mod_file_dist = os.path.join(root_mod_dir, "Automatic City and State name changer.mod")
if os.path.exists(mod_file_dist):
    os.remove(mod_file_dist)
shutil.copyfile("descriptor.mod", mod_file_dist)

exp = 1  # the line where text need to be added or exp that calculates it for ex %2

with open(mod_file_dist, 'r') as f:
    lines = f.readlines()

with open(mod_file_dist, 'w', encoding='utf8') as f:
    for i, line in enumerate(lines):
        if i == exp:
            if deploy_as_zip:
                f.write('archive="{}.zip"\n'.format(mod_dest_name))
            else:
                f.write('path="{}"'.format(mod_dest_name))
        f.write(line)
