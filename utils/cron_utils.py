import os
from crontab import CronTab
from .input_utils import get_sanitized_input, get_yn_input
from .time_utils import show_time_menu


class CronManager:

    def __init__(self):
        self.cron = CronTab(user=True)


    def _update_job_(self, attribute):
        new_attr = get_sanitized_input(prompt=f"\nEnter new {attribute}:\n", type_=str)
        while not get_yn_input(prompt=f"\n\n\nYour {attribute} to be entered is:\n{newCommand}\n\nAre you sure? [Y/n]: "):
            new_attr = get_sanitized_input(prompt=f"\nEnter new {attribute}:\n", type_=str)
        if attribute == "command":
            job.command = new_attr
        else:
            job.comment = new_attr



    def is_empty(self):
        return len(self.cron) == 0


    def setup_job(self):
        """
        Enables setting up a cron job. Allows user to enter script to execute, the time slice and the writes the job into cron
        """

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
        
        scheduleTime = show_time_menu(timeChoice)
        commandScript = f"/bin/sh {os.path.abspath(execFile)}"

        redirectBool = get_yn_input("Would you like the output of this cron job to be redirected? [Y/n]\n")
        if redirectBool:
            redirDest = get_sanitized_input("Please enter the destination that you prefer for cron job output redirection (path should be relative to the logs folder):\n", type_=str)
            commandScript += f" >> {os.path.abspath(os.path.join('./logs/', redirDest))} 2&>1"

        job = self.cron.new(command=commandScript, comment=f"Running {execFile}", precomment=True)
        job.setall(scheduleTime)
        self.cron.write()
        print("Cronjob added")


    def list_jobs(self, show_disabled=False):
        """
        Lists all the current cron jobs. If show_disabled is true, shows even the disabled jobs.
        """
        if self.is_empty():
            print("Oops! No cron jobs found! You can create one via the main menu")
            return
        print("Jobs existing in current enabled user crontab are: ")
        for i,job in enumerate(self.cron):
            if job.enabled or show_disabled:
                print(f"Job {i+1}. ", end=" ")
                if show_disabled:
                    print("Enabled " if job.enabled else "Disabled", end="\t")
                print(job.slices, job.command)


    def edit_job(self):
        """
        Allows editing the job. Provides a choice to edit timeslice, command or comment. And edits according to user input.
        """
        if self.is_empty():
            print("Oops! No cron jobs found! You can create one via the main menu")
            return
        self.list_jobs(show_disabled=True)
        print(f"Which Cron Job would you like to edit?")
        choice = get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=len(self.cron))
        job = self.cron[choice-1]
        print("\nCron Job to be edited:\n")
        print(f"Status: {'Enabled' if self.cron[choice-1].is_enabled else 'Disabled'}")
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
                
            scheduleTime = show_time_menu(timeChoice)

            job.setall(scheduleTime)
        else:
            attribute = "command" if choice == 2 else "comment"
            new_attr = get_sanitized_input(prompt=f"\nEnter new {attribute}:\n", type_=str)
            while not get_yn_input(prompt=f"\n\n\nYour {attribute} to be entered is:\n{newCommand}\n\nAre you sure? [Y/n]: "):
                new_attr = get_sanitized_input(prompt=f"\nEnter new {attribute}:\n", type_=str)
            if choice == 2:
                job.command = new_attr
            else:
                job.comment = new_attr

        print("\n\nCron Job successfully updated.\n")

        print("Updated Cron Job:\n")
        print(f"Status: {'Enabled' if job.is_enabled else 'Disabled'}")
        print(f"Timeslice: {job.slices}")
        print(f"Command: {job.command}")
        print(f"Comment: {job.comment}")


    def toggle_job(self, enable):
        """
        Toggles job between enable and disable. Shows list of cron jobs and asks which to enable/disable
        """
        if self.is_empty():
            print("Oops! No cron jobs found! You can create one via the main menu")
            return
        self.list_jobs(show_disabled=enableBool)
        print(f"Which Cron Job would you like to {'enable' if enableBool else 'disable'}?")
        choice = get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=len(self.cron))
        self.cron[choice-1].enable(enableBool)
        print(f"Cron Job {choice} has been successfully {'enabled' if enableBool else 'disabled'}")


    def delete_job(self):
        """
        Lists all jobs and deletes a cron job according to user preference
        """
        if self.is_empty():
            print("Oops! No cron jobs found! You can create one via the main menu")
            return
        self.list_jobs(show_disabled=True)
        print(f"Which Cron Job would you like to delete?")
        choice = get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=len(self.cron))
        self.cron.remove(self.cron[choice-1])
        print(f"Cron Job {choice} has been successfully deleted")


    def save(self):
        self.cron.write()