import os
from crontab import CronTab, CronSlices
from helper import *
from constant import *
from cronWrapper import CronWrapper


def mainMenu(cronWrapper):
	"""
	Displays the Main Menu (according to the MENU string array) and calls the mainMenuActioner which takes action based on choice entered.
	"""
	print("Select what you want to do: \n")
	for i, option in enumerate(MENU):
		print(f"{i+1}. {MENU[i]}")
	choice = input_util.get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=len(MENU))
	print("\n")
	mainMenuActioner(choice, cronWrapper)


def mainMenuActioner(choice, cronWrapper):
	"""
	Depending on the choice entered, calls different actions
	"""
	if choice == 1:
		setupJob(cronWrapper)
	elif choice == 2:
		cronWrapper.list()
	elif choice == 3:
		editJob(cronWrapper)
	elif choice == 4:
		cronWrapper.toggleEnable(enableBool=True)
	elif choice == 5:
		cronWrapper.toggleEnable(enableBool=False)
	elif choice == 6:
		cronWrapper.delete()
	elif choice == len(MENU):
		exit("Cron Job Exiting...\n")
	elif choice > len(MENU):
		raise ValueError(f"The choice can only have values upto {len(MENU)}")
	else:
		exit("Cron Job can't be idle because it has ADHD. Exiting...\n")
	return


def setupJob(cronWrapper):
	"""
	Enables setting up a cron job. Allows user to enter script to execute, the time slice and the writes the job into cron
	"""

	execFile = file_util.getScriptFile()
	scheduleTime = time_util.getTimeStr()
	commandScript = f"/bin/sh {os.path.abspath(execFile)}"
	comment = f"Running {execFile}"

	redirectBool = input_util.get_yn_inp("Would you like the output of this cron job to be redirected? [Y/n]\n")
	if redirectBool:
		redirDest = input_util.get_sanitized_input("Please enter the destination that you prefer for cron job output redirection (path should be relative to the logs folder):\n", type_=str)
		commandScript += f" >> {os.path.abspath(os.path.join('./logs/', redirDest))} 2&>1"

	cronWrapper.createJob(commandScript, scheduleTime, comment)
	print("Cronjob added")


def editJob(cronWrapper):
	"""
	Allows editing the job. Provides a choice to edit timeslice, command or comment. And edits according to user input.
	"""
	job = cronWrapper.selectJob(prompt = "Which job would you like to edit?")
	print("\nCron Job to be edited:\n")
	print(f"Status: {'Enabled' if job.is_enabled else 'Disabled'}")
	print(f"Timeslice: {job.slices}")
	print(f"Command: {job.command}")
	print(f"Comment: {job.comment}")
	print("Which of the following would you like to edit?")
	print("1. Timeslice")
	print("2. Command")
	print("3. Comment")
	choice = input_util.get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=3)
	cronWrapper.editJob(job, choice)

	print("\n\nCron Job successfully updated.\n")

	print("Updated Cron Job:\n")
	print(f"Status: {'Enabled' if job.is_enabled else 'Disabled'}")
	print(f"Timeslice: {job.slices}")
	print(f"Command: {job.command}")
	print(f"Comment: {job.comment}")


def backToMainMenu():
	"""
	Prompts user if they want to see the main menu after all actions of cronJobMaster have been completed.
	"""
	mainBool = input_util.get_yn_inp(prompt="\nThank you for using Cron Job Master.\nDo you want to go back to the Main Menu? [Y/n]\n")
	print("\n")
	return mainBool


if __name__ == "__main__":
	cronWrapper = CronWrapper.CronWrapper()
	mainMenu(cronWrapper)
	cronWrapper.write()
	while backToMainMenu():
		mainMenu(cronWrapper)
		cronWrapper.write()
	exit("Cron Job Exiting...")
