def get_yn_inp(prompt):
	"""
	Returns a boolean value after prompting the user to enter either Yes or No
	"""
	while True:
		inp = input(prompt)
		if inp in ['y', 'Y', 'Yes', 'yes', 'YES', 'True', 'true', 'TRUE']:
			return True
		if inp in ['n', 'N', 'No', 'no', 'NO', 'False', 'false', 'FALSE']:
			return False
		else:
			print(f"ERR: Please enter either Y or N")


def get_sanitized_input(prompt, type_=None, min_=None, max_=None, exception=None):
	"""
	Gets an  input from the user after showing them prompt. Type of input, minimum, maximum and exceptions are sanitized against.
	"""
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