import os
from crontab import CronTab, CronSlices


MENU = [
"Set up a Cron Job",
"List All Current Cron Jobs",
"Edit Cron Job",
"Enable Cron Job",
"Disable Cron Job",
"Delete Cron Job",
"Exit"
]


def get_yn_inp(prompt):
	while True:
		inp = input(prompt)
		if inp in ['y', 'Y', 'Yes', 'yes', 'YES', 'True', 'true', 'TRUE']:
			return True
		if inp in ['n', 'N', 'No', 'no', 'NO', 'False', 'false', 'FALSE']:
			return False
		else:
			print(f"ERR: Please enter either Y or N")


def get_sanitized_input(prompt, type_=None, min_=None, max_=None, exception=None):
	if min_ is not None and max_ is not None and max_ < min_:
		raise ValueError("min_ must be less than or equal to max_")
	while True:
		inp = input(prompt)
		if exception:
			if inp == exception:
				return inp
		if type_:
			try:
				inp = type_(inp)
			except ValueError:
				print(f"ERR: Input type must be {type_}")
				continue
		if max_ is not None and inp > max_:
			print(f"ERR: Input value must be less than or equal to {max_}\n")
		elif min_ is not None and inp < min_:
			print(f"ERR: Input value must be more than or equal to {min_}\n")
		else:
			return inp


def get_basic_time():
	print("Enter integers for the following fields:")
	minute = get_sanitized_input(prompt="Minute (0-59): ", type_=int, min_=0, max_=59, exception="*")
	hour = get_sanitized_input(prompt="Hour (0-23): ", type_=int, min_=0, max_=23, exception="*")
	dom = get_sanitized_input(prompt="Day of Month (1-31): ", type_=int, min_=1, max_=31, exception="*")
	mon = get_sanitized_input(prompt="Month (1-12): ", type_=int, min_=1, max_=12, exception="*")
	dow = get_sanitized_input(prompt="Day of Week (0-6, 0 corresponding to Sunday): ", type_=int, min_=0, max_=6, exception="*")
	return " ".join([minute, hour, dom, mon, dow])

def get_advanced_time():
	time = get_sanitized_input(prompt="Enter the time string: ", type_=str)
	return time

def timeMenu(choice):
	if choice not in [1,2]:
		raise ValueError("The choice can only be 1 or 2")
	while True:
		if choice == 1:
			print("BASIC")
			time = get_basic_time()
		else:
			print("ADVANCED")
			time = get_advanced_time()
		if CronSlices.is_valid(time):
			return time
		print("Sorry, your scheduling time is invalid. Please try again.")


def mainMenu(cron):
	print("Select what you want to do: \n")
	for i, option in enumerate(MENU):
		print(f"{i+1}. {MENU[i]}")
	choice = get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=len(MENU))
	print("\n")
	mainMenuActioner(choice, cron)


def mainMenuActioner(choice, cron):
	if choice == 1:
		setupJob(cron)
	elif choice == 2:
		showDisabled = get_yn_inp(prompt="Do you want to see disabled jobs as well? [Y/n]\n")
		print("\n")
		listJobs(cron, showDisabled=showDisabled)
	elif choice == 3:
		editJob(cron)
	elif choice == 4:
		toggleJob(cron, enableBool=True)
	elif choice == 5:
		toggleJob(cron, enableBool=False)
	elif choice == 6:
		deleteJob(cron)
	elif choice == len(MENU):
		exit("Cron Job Exiting...\n")
	elif choice > len(MENU):
		raise ValueError(f"The choice can only have values upto {len(MENU)}")
	else:
		print("Nothing to do")
	return


def setupJob(cron):

	while True:
		execFile = os.path.join("./scripts/", input("Enter script file name: "))
		if os.path.exists(execFile):
			break
		print("File does not exist. Please try again.")
		print("List of files in 'scripts' folder:")
		for file in os.listdir("./scripts/"):
			if os.path.isfile(os.path.join("./scripts", file)):
				print("\t", file)
	os.chmod(execFile, 0o775)

	timeChoice = get_sanitized_input(prompt="""
Choose the Time Input you'd like to provide:
1. Basic Time Input
2. Advanced Time Input (setup a custom time string)

Choice: """, type_=int, min_=1, max_=2)
	print("\n")
	
	scheduleTime = timeMenu(timeChoice)
	commandScript = f"/bin/sh {os.path.abspath(execFile)}"

	redirectBool = get_yn_inp("Would you like the output of this cron job to be redirected? [Y/n]\n")
	if redirectBool:
		redirDest = get_sanitized_input("Please enter the destination that you prefer for cron job output redirection (path should be relative to the logs folder):\n", type_=str)
		commandScript += f" >> {os.path.abspath(os.path.join('./logs/', redirDest))} 2&>1"

	job = cron.new(command=commandScript, comment=f"Running {execFile}", precomment=True)
	job.setall(scheduleTime)
	cron.write()
	print("Cronjob added")


def listJobs(cron, showDisabled=False):
	print("Jobs existing in current enabled user crontab are: ")
	for i,job in enumerate(cron):
		if job.enabled or showDisabled:
			print(f"Job {i+1}. ", end=" ")
			if showDisabled:
				print("Enabled " if job.enabled else "Disabled", end="\t")
			print(job.slices, job.command)


def editJob(cron):
	listJobs(cron, showDisabled=True)
	print(f"Which Cron Job would you like to edit?")
	choice = get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=len(cron))
	job = cron[choice-1]
	print("\nCron Job to be edited:\n")
	print(f"Status: {'Enabled' if cron[choice-1].is_enabled else 'Disabled'}")
	print(f"Timeslice: {job.slices}")
	print(f"Command: {job.command}")
	print(f"Comment: {job.comment}")
	print("Which of the following would you like to edit?")
	print("1. Timeslice")
	print("2. Command")
	print("3. Comment")
	choice = get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=3)
	if choice == 1:
		timeChoice = get_sanitized_input(prompt="""
Choose the Time Input you'd like to provide:
1. Basic Time Input
2. Advanced Time Input (setup a custom time string)

Choice: """, type_=int, min_=1, max_=2)
		print("\n")
			
		scheduleTime = timeMenu(timeChoice)

		job.setall(scheduleTime)
	elif choice == 2:
		newCommand = get_sanitized_input(prompt="\nEnter new command:\n", type_=str)
		while not get_yn_inp(prompt=f"\n\n\nYour command to be entered is:\n{newCommand}\n\nAre you sure? [Y/n]: "):
			newCommand = get_sanitized_input(prompt="\nEnter new command:\n", type_=str)
		job.command = newCommand
	elif choice == 3:
		newComment = get_sanitized_input(prompt="\nEnter new comment:\n", type_=str)
		while not get_yn_inp(prompt=f"\n\n\nYour comment to be entered is:\n{newComment}\n\nAre you sure? [Y/n]: "):
			newComment = get_sanitized_input(prompt="\nEnter new comment:\n", type_=str)
		job.comment = newComment

	print("\n\nCron Job successfully updated.\n")

	print("Updated CRON Job:\n")
	print(f"Status: {'Enabled' if job.is_enabled else 'Disabled'}")
	print(f"Timeslice: {job.slices}")
	print(f"Command: {job.command}")
	print(f"Comment: {job.comment}")


def toggleJob(cron, enableBool):
	listJobs(cron, showDisabled=enableBool)
	print(f"Which Cron Job would you like to {'enable' if enableBool else 'disable'}?")
	choice = get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=len(cron))
	cron[choice-1].enable(enableBool)
	print(f"Cron Job {choice} has been successfully {'enabled' if enableBool else 'disabled'}")


def deleteJob(cron):
	listJobs(cron, showDisabled=True)
	print(f"Which Cron Job would you like to delete?")
	choice = get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=len(cron))
	cron.remove(cron[choice-1])
	print(f"Cron Job {choice} has been successfully deleted")


def showMain():
	mainBool = get_yn_inp(prompt="\nThank you for using Cron Job Master.\nDo you want to go back to the Main Menu? [Y/n]\n")
	print("\n")
	return mainBool


if __name__ == "__main__":
	cron = CronTab(user=True)
	mainMenu(cron)
	cron.write()
	while showMain():
		mainMenu(cron)
		cron.write()
	exit("Cron Job Exiting...")