class Employee:   #capitalize initial letter
	
	def __init__(self, first, last):
		self.first = first
		self.last = last


	def print_fullname(self):
		print ('{} {}'.format(self.first, self.last))
