[![Automatic-City-and-State-name-changer](https://github.com/kaboto1/Automatic-City-and-State-name-changer/actions/workflows/testing.yml/badge.svg?branch=master)](https://github.com/kaboto1/Automatic-City-and-State-name-changer/actions/workflows/testing.yml)

Welcome to the development repository of the Hearts of Iron 4 mod "Automatic City and State name changer"

The mod aims to create an immersive and realistic simulation of foregneir territorial occupation and integration by changing names and cities state in the language / culture or the owner.

Central part of this work is the *database* `provinces.yaml` and `states.yaml` where all the different name version are stored.

If you want to contribute to the mod only modifying these file would be of great help.

Next, there is `generate.py` that from the database creates the actualy hoi4 script that make the name change happening.

`wiki_translate.py` is used to make the base work using Wikipedia API to try to fetch the name in the different language, but often is a modern / incorrect version but still it helps a lot.

`deploy_local.py` to test the mod locally, it can create the zip or folder in the `mod` of you game installation.

Don't hesitate to create a pull_request if you want to contribute!
