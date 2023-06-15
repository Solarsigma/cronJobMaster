from .input_utils import get_sanitized_input, get_yn_input


def get_basic_time():
	"""
	Prompts and takes in user input of time slices. Returns a string-formatted timeslice.
	"""
	print("Enter integers for the following fields:")
	minute = get_sanitized_input(prompt="Minute (0-59): ", type_=int, min_=0, max_=59, exception="*")
	hour = get_sanitized_input(prompt="Hour (0-23): ", type_=int, min_=0, max_=23, exception="*")
	dom = get_sanitized_input(prompt="Day of Month (1-31): ", type_=int, min_=1, max_=31, exception="*")
	mon = get_sanitized_input(prompt="Month (1-12): ", type_=int, min_=1, max_=12, exception="*")
	dow = get_sanitized_input(prompt="Day of Week (0-6, 0 corresponding to Sunday): ", type_=int, min_=0, max_=6, exception="*")
	return " ".join([minute, hour, dom, mon, dow])


def get_advanced_time():
	"""
	Returns a simple user-inputted string-formatted timeslice.
	"""
	time = get_sanitized_input(prompt="Enter the time string: ", type_=str)
	return time


def show_time_menu(choice):
	"""
	Displays the time Menu and returns the entered time.
	"""
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