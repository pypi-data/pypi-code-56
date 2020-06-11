import requests
import json
import sys
import time

class CC:
	def __init__(self, api_token, id):
		self.api_token = api_token
		self.id = id
		
	def score(self, ids):
		url = 'https://corona-coins.ru/api/'
		response = requests.post(url,
		headers = {'Content-type': 'application/json'},
	
		                    
		json = {"token":self.api_token,
		             "method":"score",
		             "user_ids":ids
		}).json()
		return response
		
	def send(self,  to, summa):
		url = 'https://corona-coins.ru/api/'
		response = requests.post(url,
		headers = {'Content-type': 'application/json'},
		
			                    
		json = {"token":self.api_token,
		             "method":"transfer",
		             "to_id":to,
		             "amount":summa
			}).json()
		return response
			
		
		
	def getLink(id, summa, edit):
		if edit == False:
			return "vk.com/app7349811#merchant"+str(id)+"_"+str(summa)+"_1"
		elif edit == True:
			return "vk.com/app7349811#merchant"+str(id)+"_"+str(summa)
	
	def history(self, type=1):
		url = 'https://corona-coins.ru/api/'
		response = requests.post(url,
		headers = {'Content-type': 'application/json'},
		
			                    
		json = {"token":self.api_token,
		             "method":"history",
		             "type":type
			}).json()
		return response
			
	def run_longPoll(self, interval=0.05):
		longpoll_transaction = self.history(1)
		while True:
			time.sleep(interval)
			one_transaction = self.history(1)['response'][0]
			try:
				if longpoll_transaction['response'][0] != one_transaction:
					new_transaction = one_transaction
					if new_transaction['to_id'] == self.id:
						longpoll_transaction = one_transaction
						return new_transaction
						
			except IndexError:
				pass