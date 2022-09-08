# Cron Job Master
This CLI tool helps you setup cron jobs quickly and easily. It utilizes a script to be placed in the `cron_scripts` folder within the root repository (where the `main.py` file is placed). It can also publish debugging logs to a `logs` folder withing the root repository of the project.

To use, simply run `python main.py`

Currently, it is usable only for Linux users.

Currently, it supports the following functionality:
1. Listing all Cron Jobs present with the User
2. Adding a new cron job (Note: A pre-existing shell script which you want to run should be present in the `cron_scripts` folder. This tool does not support creating simple shell scripts yet)
3. Deleting/Disabling/Editing a cron job. You can delete/disable a cron job or edit which file it runs/when it runs.

The following updates are planned:
1. ~~Adding a README~~
2. Updating the Code so it is more extensible, developer friendly, and to follow SOLID principles.
3. Making a GUI
4. Creating simple scripts through the tool (For eg: Opening a URL in a browser etc). This will most likely be implemented only in the GUI.
5. Multiple-user support.
6. Other OS support.

I've explained my progress with the code and its steps [here](https://solarsigma.notion.site/Making-of-Python-Program-49f4e10cf65d4b6b843e98aed1075122).