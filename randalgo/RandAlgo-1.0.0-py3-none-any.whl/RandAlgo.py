import re
from bs4 import BeautifulSoup
import requests
import random


# fetching source code of the website
source = requests.get('https://java2blog.com/java-coding-interview-questions').text

# parsing into beautifulsoup
soup = BeautifulSoup(source, "lxml")

# Accessing the div tag with the info needed 
infomation = soup.find('div', class_='toc_light_blue no_bullets')

# searching within match to grab the text 
algorithmQuestions = infomation.ul.text

result = algorithmQuestions.replace("java", "python").split('Question')

#Choose Question
def chooseQuestion(number):
    easyQuestions = []
    mediumQuestions = []
    hardQuestions = []

    easyQuestions.extend([result[1],result[2],result[3],result[10],result[11],result[12],result[13],result[14],result[15],result[16],result[17],result[18],result[19],result[20]])

    mediumQuestions.extend([result[7],result[8],result[9],result[21],result[22],result[23],result[24],result[25],result[26],result[27],result[28],result[29],result[30],result[31],result[32],result[33],result[34],result[35],result[36],result[37],result[38],result[39],result[40]])

    hardQuestions.extend([result[41],result[42],result[43],result[44],result[45],result[46],result[47],result[48],result[49],result[50]])
    if number == "1":
        return easyQuestions
    elif number == "2":
        return mediumQuestions
    elif number == "3":
        return hardQuestions
    else:
        return []


# Validating email
def check_email(email):
    regex = "^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$"
    if (re.search(regex,email)):  
        print("Valid Email")
        return True         
    else:  
        print("Invalid Email, Fill-in valid email") 
        return False

# algorithm question selection
def level(option):            
    if option == "1":
        easyQuestion = random.choice(chooseQuestion(option))
        print(easyQuestion)
    if option == "2":
        mediumQuestion = random.choice(chooseQuestion(option))
        print(mediumQuestion)
    if option == "3":
        hardQuestion = random.choice(chooseQuestion(option))
        print(hardQuestion)


# Saving user details to the text file
def sign_up(text_to_append):
    """Append given text as a new line at the end of file"""
    # Opening the file in append & read mode ('a+')
    with open("UserDetails.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)


# verifying in login details
def log_in():
    usernameRequest = input("Enter username: ")
    passwordRequest = input("Enter password: ")
# Returning all lines in the file, as a list. Each line is an item
    loginSuccessful = []
    with open("UserDetails.txt", "r") as user:
        allUsers = user.readlines()
        for users in allUsers:
            singleUserArray = users.split(',')
            if usernameRequest == singleUserArray[1] and passwordRequest == singleUserArray[2].replace("\n",""):
                loginSuccessful.append(1)
                break
            else:
                loginSuccessful.clear()
    
    if(len(loginSuccessful) >= 1):
        print("Login Successful")
        while True:
            difficulty_level = input('''
Kindly choose the difficulty level:
Enter 1 for Easy
      2 for Medium
      3 for Hard
      >>>: ''')
            if difficulty_level == "1" or difficulty_level == "2" or difficulty_level == "3":
                break
                
            else:
                print("Wrong Entry!, Try again")
        while True:
            nextQuestion = 0
            close = 0
            
            level(difficulty_level)
            while True:
                # level(difficulty_level)
                selectNext =  input('''
    Answer the Question, to Continue
    Enter 1 for Yes
        2 for No
        >>>: ''')
                if(selectNext == "1"):
                    nextQuestion = 1
                    break
                elif (selectNext == "2"):
                    close = 1
                    print("Thanks for using RandAlgo")
                    break  
                else:
                    print("Wrong Entry")
                                           
            if nextQuestion == 1:
                continue
            if close == 1:
                break
    else:
        print("Wrong Username or Password")
        log_in()
              

# Requesting for User details 
def main():
    mail = True
    while mail:
        emailAddress = str(input("Enter Email Adress: "))
        if check_email(emailAddress):
            break
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    userInfo = emailAddress + "," + username + "," + password
    sign_up(userInfo)
    print("Sign up Successful, Kindly log in")
    log_in()


 # Greetings and choosing actions to take 
while True:
    print("Welcome to RandAlgo, Choose 1 for Sign up or 2 for Sign in")
    choice = input(">>>: ")

    if choice == "1":
        main()
    elif choice == "2":
        log_in()
    else:
        print("Wrong!, Choose 1 for Sign up or 2 for Sign in")
        

