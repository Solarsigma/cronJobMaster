from crontab import CronTab
from helper import *

class CronWrapper:

	def __init__(self):
		self.cron = CronTab(user=True)


	def list(self, showDisabled=None):
		"""
		Lists all the current cron jobs. If showDisabled is true, shows even the disabled jobs.
		"""
		if showDisabled is None:
			showDisabled = input_util.get_yn_inp(prompt="Do you want to see disabled jobs as well? [Y/n]\n")
			print("\n")
		print("Jobs existing in current enabled user crontab are: ")
		for i,job in enumerate(self.cron):
			if job.enabled or showDisabled:
				print(f"Job {i+1}. ", end=" ")
				if showDisabled:
					print("Enabled " if job.enabled else "Disabled", end="\t")
				print(job.slices, job.command)


	def toggleEnable(self, enableBool):
		"""
		Toggles job between enable and disable. Shows list of cron jobs and asks which to enable/disable
		"""
		job = self.selectJob(prompt = f"Which job would you like to {'enable' if enableBool else 'disable'}?")
		job.enable(enableBool)
		print(f"Selected Cron Job has been successfully {'enabled' if enableBool else 'disabled'}")


	def delete(self):
		"""
		Lists all jobs and deletes a cron job according to user preference
		"""
		job = self.selectJob(prompt = "Which job would you like to delete?")
		self.cron.remove(job)
		print(f"Cron Job has been successfully deleted")
		print("Deleted Cron Job:\n")
		print(f"Status: {'Enabled' if job.is_enabled else 'Disabled'}")
		print(f"Timeslice: {job.slices}")
		print(f"Command: {job.command}")
		print(f"Comment: {job.comment}")


	def createJob(self, command, scheduleTimeStr, comment):
		"""
		Sets up a cron job given the command script and the time string
		"""
		job = self.cron.new(command=commandScript, comment = comment, precomment = True)
		job.setall(timeStr)
		self.cron.write()


	def selectJob(self, prompt="Please select a job"):
		"""
		Allows user to select the job they want
		"""
		self.list(showDisabled=True)
		print(prompt)
		choice = input_util.get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=len(self.cron))
		return self.cron[choice-1]


	def editJob(self, job, choice):
		"""
		Allows user to edit a job in the cron. Choice corresponds to editing either 1. Timeslice, 2. Command or 3. Comment
		"""
		if choice == 1:
			scheduleTime = time_util.getTimeStr()
			job.setall(scheduleTime)
		elif choice == 2:
			newCommand = input_util.get_sanitized_input(prompt="\nEnter new command:\n", type_=str)
			while not input_util.get_yn_inp(prompt=f"\n\n\nYour command to be entered is:\n{newCommand}\n\nAre you sure? [Y/n]: "):
				newCommand = input_util.get_sanitized_input(prompt="\nEnter new command:\n", type_=str)
			job.command = newCommand
		elif choice == 3:
			newComment = input_util.get_sanitized_input(prompt="\nEnter new comment:\n", type_=str)
			while not input_util.get_yn_inp(prompt=f"\n\n\nYour comment to be entered is:\n{newComment}\n\nAre you sure? [Y/n]: "):
				newComment = input_util.get_sanitized_input(prompt="\nEnter new comment:\n", type_=str)
			job.comment = newComment


	def write(self):
		self.cron.write()
