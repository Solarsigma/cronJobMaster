import os
from crontab import CronTab, CronSlices
from utils.input_utils import get_sanitized_input, get_yn_input
from utils.cron_utils import CronManager


MENU = [
"Set up a Cron Job",
"List All Current Cron Jobs",
"Edit Cron Job",
"Enable Cron Job",
"Disable Cron Job",
"Delete Cron Job",
"Exit"
]


def mainMenu(cron_manager):
	"""
	Displays the Main Menu (according to the MENU string array) and calls the mainMenuActioner which takes action based on choice entered.
	"""
	print("Select what you want to do: \n")
    for i, option in enumerate(MENU, start=1):
        print(f"{i}. {option}")
	choice = get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=len(MENU))
	print("\n")
	main_menu_actioner(choice, cron_manager)


def main_menu_actioner(choice, cron_manager):
	"""
	Depending on the choice entered, calls different actions
	"""
    actions = {
        1: cron_manager.setup_job,
        2: lambda: cron_manager.list_jobs(show_disabled=get_yn_input(prompt="Do you want to see disabled jobs as well? [Y/n]\n")),
        3: cron_manager.edit_job,
        4: lambda: cron_manager.toggle_job(enableBool=True),
        5: lambda: cron_manager.toggle_job(enableBool=False),
        6: cron_manager.delete_job,
        7: exit,
    }
    action = actions.get(choice)
    if action is None:
        raise ValueError(f"Invalid choice: {choice}. Please select a valid option.")
    action()


if __name__ == "__main__":
	print("Welcome to the Cron Job Master tool! Here, YOU are the Cron Job Master!\n\n")
    main_menu(cron_manager)
    cron_manager.save()
    while True:
        if not get_yn_input(prompt="\nThank you for using Cron Job Master.\nDo you want to go back to the Main Menu? [Y/n]\n"):
            break
        main_menu(cron_manager)
        cron_manager.save()
	exit("Cron Job Exiting...")