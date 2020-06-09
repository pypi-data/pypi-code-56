def print_lol(the_list, collapse=False, level=0):
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, collapse, level+1)
		else:
			if(collapse):
				for stop in range(level):
					print("\t", end="")
			print(each_item)
