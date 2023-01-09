from helper import *

def setupJob(cronWrapper):
	"""
	Enables setting up a cron job. Allows user to enter script to execute, the time slice and the writes the job into cron
	"""

	execFile = file_util.getScriptFile()
	scheduleTime = time_util.getTimeStr()
	commandScript = f"/bin/sh {os.path.abspath(execFile)}"
	comment = f"Running {execFile}"

	redirectBool = input_util.get_yn_inp("Would you like the output of this cron job to be redirected?")
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
