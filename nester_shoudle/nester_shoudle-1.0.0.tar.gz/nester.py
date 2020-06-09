"""This is a beginer's moudle"""
def print_lol(the_list):
	"""this function visit and print a complexed list"""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)

