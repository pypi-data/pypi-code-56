import random
import sys
import requests
from bs4 import BeautifulSoup


def register():	

	name = input('\nPlease input your full name: ')
	username = input('Input your preferred username: ')
	email = input('Please input your email: ')
		
	while True:
		password = str(input('Please input password(>6 characters): '))
		if len(password) >= 7:
			break
		else:
			print('Password should be >6 charaters\n')
			True
							
	file = open('user.txt','a')
	user_token = ''.join(map(str, random.sample(range(0,9),9)))						
	file.write (f'\nName: {name} \nUsername: {username} \nPassword: {password} \nToken: {user_token} \nEmail: {email}\n')		
	print(f'\nHere is your Token {user_token}, please keep safe.\n')
	file.close()	
	return	

def login():	
	while True:
		with open ('user.txt', 'r') as file:
			correct_details = 0
			username = input('\nUsername: ')
			password = input('Password: ')
			for line in file.readlines():
				y = line.split (':')
				if len(y) > 1:
					if y[0] == "Username" and y[1].strip() == username:
						correct_details += 1
					elif y[0] == "Password" and y[1].strip() == password:
						correct_details += 1
			if correct_details == 2:
				print ('\nLogin in successful')
				break	
			else:
				print('Wrong username or password please try again')
	else:
		True
		return	
		

def token():
	print('\nInput Token key before you can access GMAT Questions\n')
	while True:
		with open ('user.txt', 'r') as file:
			token = input('Token key: ')
			correct_details = 0
			for line in file.readlines():
				y = line.split (':')
				if len(y) > 1:
					if y[0] == "Token" and y[1].strip() == token:
						correct_details += 1
			if correct_details == 1:
				break
			else:
				print('Invalid token key, try again\n')
	else:
		True
		return
		

def main():	
	while True:
		try:
			print ('WELCOME TO GMATH PREPARATION\n')
			check = True
			while check:
				choice = int(input('1. Register \n2. Login \n3. Exit\n\n--> '))						
				if choice > 3:
					print ('\nPlease input valid number\n')
					check = True
				else:
					check = False
					break
					
			if choice == 1:
				register()
				True
			elif choice == 2:
				login()
				token()
				
				checks = True
				while checks:
					user_choice  = int(input('\n1. Quantitative Test \n2. Verbal Test \n3. Logout\n\n--> '))
					if choice > 3:
						print ('\nPlease input valid number\n')
						checks = True
					else:
						checks = False 
						break
					
				if user_choice == 1:
					for x in range (1,50,4):
						store = requests.get(f'https://projecteuler.net/problem={x}').text
						search = BeautifulSoup (store, 'html5lib')
						article = search.find('div', class_='problem_content')
							
						for article in  search.find_all('div', class_='problem_content'):
							question = article.text				
							print (question)
					
				elif user_choice == 2:
					
					store = requests.get(f'https://www.mba.com/exams/gmat/about-the-gmat-exam/gmat-exam-structure/verbal').text
	
					search = BeautifulSoup (store, 'html5lib')
					article = search.find('p', style='margin-left: 40px;')
			
					for article in  search.find_all('p', style='margin-left: 40px;'):
						question = article.text
						print(f'\n{question}')
					
				elif user_choice == 3:
					True
					
			else:
				sys.exit()
		except ValueError:
			print('input valid number')
	True
	return
			
if __name__ == '__main__':
	main ()