import os
from crontab import CronTab, CronSlices
from helper import *
from constant import *
from cronWrapper import CronWrapper
from menuController import MenuController


if __name__ == "__main__":
	cronWrapper = CronWrapper.CronWrapper()
	# mainMenu(cronWrapper)
	MenuController.generate_menu(cronWrapper)
	cronWrapper.write()
	while MenuController.loop_menu():
		MenuController.generate_menu(cronWrapper)
		cronWrapper.write()
	exit("Cron Job Exiting...")
