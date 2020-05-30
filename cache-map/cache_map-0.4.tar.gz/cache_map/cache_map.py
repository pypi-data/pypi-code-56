'''
Author : Rahul Sunil
Email  : rahulsunil2@gmail.com
Description : Cache Mapping
'''

class CacheMapping:

	def __init__(self, cache_size, mem_blocks):
		self.hit = 0 
		self.miss = 0
		self.cache_mem = {}
		self.cache_size = cache_size
		self.mem_blocks = list(map(int, mem_blocks.split(' ')))
		for i in range(self.cache_size):
			self.cache_mem[i] = list()
		self.page_history = []

	def updateHistory(self, p):
		if p in self.page_history:
			self.page_history.remove(p)
		self.page_history.append(p)

	def searchCache(self, p):
		for cache_i, mem_i in self.cache_mem.items():  
		    if p in mem_i:
		        return(cache_i)
		return -1

	def updateCacheMemory(self, p):
		for cache_i, mem_i in self.cache_mem.items():
			if len(mem_i) == 0:
				self.miss += 1
				self.cache_mem[cache_i].append(p)
				self.updateHistory(p)
				return
			elif mem_i[-1] == p:
				self.hit += 1
				self.updateHistory(p)
				return

		self.miss += 1
		key = self.searchCache(self.page_history.pop(0))
		self.cache_mem[key].append(p)
		self.updateHistory(p)

	def mapLRU(self):
		for page in self.mem_blocks:
			self.updateCacheMemory(page)

	def directMap(self):
		for i in self.mem_blocks:
			key = i % self.cache_size
			if(len(self.cache_mem[key]) > 0 and self.cache_mem[key][-1] == i):
				self.hit += 1
			else:
				self.miss += 1
				self.cache_mem[key].append(i)

	def display(self):
		print('Hit : ', self.hit)
		print('Miss : ', self.miss)
		print('Memory size : ', len(self.mem_blocks))

		for i in self.cache_mem.keys():
			print(self.cache_mem[i])


if __name__ == '__main__':

	c = int(input('Enter the cache memory size : '))
	m = input('Enter the memory blocks : ')

	print("1. Direct Map\n2. LRU Map")
	choice = int(input('Enter the choice : '))

	if choice == 1:
		# D I R E C T   M A P
		direct_map = CacheMapping(c, m)
		direct_map.directMap()
		direct_map.display()

	elif choice == 2:
		# L R U   M A P
		LRU_map = CacheMapping(c, m)
		LRU_map.mapLRU()
		LRU_map.display()

	else:
		print('Wrong Command')

