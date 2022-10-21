from . import input_util

def get_basic_time():
	"""
	Prompts and takes in user input of time slices. Returns a string-formatted timeslice.
	"""
	print("Enter integers for the following fields:")
	minute = input_util.get_sanitized_input(prompt="Minute (0-59): ", type_=int, min_=0, max_=59, exception="*")
	hour = input_util.get_sanitized_input(prompt="Hour (0-23): ", type_=int, min_=0, max_=23, exception="*")
	dom = input_util.get_sanitized_input(prompt="Day of Month (1-31): ", type_=int, min_=1, max_=31, exception="*")
	mon = input_util.get_sanitized_input(prompt="Month (1-12): ", type_=int, min_=1, max_=12, exception="*")
	dow = input_util.get_sanitized_input(prompt="Day of Week (0-6, 0 corresponding to Sunday): ", type_=int, min_=0, max_=6, exception="*")
	return " ".join([minute, hour, dom, mon, dow])


def get_advanced_time():
	"""
	Returns a simple user-inputted string-formatted timeslice.
	"""
	time = input_util.get_sanitized_input(prompt="Enter the time string: ", type_=str)
	return time


def getChoiceFromMenu():
	timeChoice = input_util.get_sanitized_input(prompt="""
Choose the Time Input you'd like to provide:
1. Basic Time Input
2. Advanced Time Input (setup a custom time string)

Choice: """, type_=int, min_=1, max_=2)
	print("\n")
	return timeChoice


def getTimeStr():
	"""
	Displays the time Menu and returns the entered time.
	"""
	choice = getChoiceFromMenu()
	if choice not in [1,2]:
		raise ValueError("The choice can only be 1 or 2")
	while True:
		if choice == 1:
			print("BASIC TIME INPUT")
			time = get_basic_time()
		else:
			print("ADVANCED TIME INPUT")
			time = get_advanced_time()
		if CronSlices.is_valid(time):
			return time
		print("Sorry, your scheduling time is invalid. Please try again.")
