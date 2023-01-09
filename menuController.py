from helper import input_util
from utils import *

class MenuController:

    @staticmethod
    def do_1():
        """Set up a Cron Job"""
        setupJob(MenuController.cronWrapper)

    @staticmethod
    def do_2():
        """List All Current Cron Jobs"""
        MenuController.cronWrapper.list()

    @staticmethod
    def do_3():
        """Edit Cron Job"""
        editJob(MenuController.cronWrapper)

    @staticmethod
    def do_4():
        """Enable Cron Job"""
        MenuController.cronWrapper.toggleEnable(enableBool=True)

    @staticmethod
    def do_5():
        """Disable Cron Job"""
        MenuController.cronWrapper.toggleEnable(enableBool=False)

    @staticmethod
    def do_6():
        """Delete Cron Job"""
        MenuController.cronWrapper.delete()

    @staticmethod
    def do_7():
        """Exit"""
        exit("Cron Job Exiting...\n")

    @staticmethod
    def nothing():
        exit("Cron Job can't be idle because it has ADHD. Exiting...\n")

    @staticmethod
    def execute(user_input):
        controller_name = f"do_{user_input}"
        try:
            controller = getattr(MenuController, controller_name)
        except AttributeError:
            controller = getattr(MenuController, 'nothing')
        finally:
            controller()

    @staticmethod
    def generate_menu(cronWrapper):
        MenuController.cronWrapper = cronWrapper
        print("Select what you want to do: \n")
        do_methods = [m for m in dir(MenuController) if m.startswith('do_')]
        menu_string = "\n".join(
            [f"{method[-1]}. {getattr(MenuController, method).__doc__}"
                for method in do_methods])
        print(menu_string)
        choice = input_util.get_sanitized_input(prompt="Choice: ", type_=int, min_=1, max_=max([int(method[-1]) for method in do_methods]))
        print("\n")
        MenuController.execute(choice)

    @staticmethod
    def loop_menu():
    	mainBool = input_util.get_yn_inp(prompt="\nThank you for using Cron Job Master.\nDo you want to go back to the Main Menu?")
    	print("\n")
    	return mainBool
