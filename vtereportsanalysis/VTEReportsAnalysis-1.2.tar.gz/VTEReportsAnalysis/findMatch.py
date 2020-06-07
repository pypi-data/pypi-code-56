from collections import defaultdict

def shift_table(pattern):
	table = defaultdict(lambda: len(pattern))
	for index in range(0, len(pattern)-1):
		table[pattern[index]] = len(pattern) - 1 - index
	return table

def horspool_match(pattern, text):
	table = shift_table(pattern)
	index = len(pattern) - 1
	while index <= len(text) - 1:
		match_count = 0
		while match_count < len(pattern) and pattern[len(pattern)-1-match_count] == text[index-match_count]:
			match_count += 1
		if match_count == len(pattern):
			return index-match_count+1
		else:
			index += table[text[index]]
	return -1
'''
if __name__ == "__main__": 

	a = 'barber'
	b = 'jim_barbersaw_me_in_a_barbershopp'
	print(horspool_match(a, b))
	print(a[2:])
	print(b[horspool_match(a, b):])
'''