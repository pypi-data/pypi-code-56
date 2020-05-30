from . import question
import random
import string
import string_utils
import re
import sqlite3


conn = sqlite3.connect('user_credential.db')
conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    'First_Name' varchar(40) NOT NULL,
    'Last_Name' varchar(40) NOT NULL,
    'Email_Address' varchar(40) NOT NULL,
    'User_Name' varchar(40) NOT NULL,
    Password varchar(40) NOT NULL)
    """)

regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"


"""
This function automatically generates a password of 16 shuffled characters for the user.
"""


def gen_password():
    lower_case = string.ascii_lowercase
    upper_case = string.ascii_uppercase
    symbols = string.punctuation
    length = 4
    lower_case_pass = ''.join(random.choice(lower_case) for i in range(length))
    upper_case_pass = ''.join(random.choice(upper_case) for i in range(length))
    numbers = ''.join(map(str, random.sample(range(1, 9), length)))
    characters = ''.join(random.choice(symbols) for i in range(length))
    auto_password = lower_case_pass + upper_case_pass + numbers + characters
    password = string_utils.shuffle(auto_password)
    return password


"""
This function allows the user to decide whether they want the auto generated password or they want to type in
their own password. The user typed password must be between 7 to 20 characters.
"""


def user_gen_password():
    while True:
        user_passwords = input('\nPlease Enter your Password: \n')

        if 7 < len(user_passwords) < 20:
            pass
            break

        else:
            print('\nERROR!!! Password must be between 8 and 20 characters.')
    return user_passwords


"""
This function is for the signup page. The user is asked to input their first name and their last name. They will also
be asked for their email account, the email account would be checked to make sure it is in the right format. If the
email is not in the right format, it will throw up an error and the user will be asked to input their email again. 
Then the program will check if the email already exists in our database. If it does, an error message will appear and 
the user will be asked to input another email. The user will be asked to input their username, the program will check 
if the username is in our database. If it does, an error message will also appear and the user will be asked to type in
another username. The user will be asked if they want an auto generated password or they want to input their password. 
If they select auto generated password, the program automatically generates a random and shuffled 16 characters as the
password and if they select no, the program will ask them input their password and the password must be between 7 to 20 
characters.
"""


def signup():
    first_name = input('Enter First name: ')
    last_name = input('Enter Last name: ')

    while True:
        email = input('\nEnter the Account Email: ')

        if re.search(regex, email):
            cursor = conn.execute(f"SELECT * from users WHERE Email_Address= '{email}'").fetchone()

            if cursor:
                print('\nERROR! Email already in exists.')

            else:
                pass
                break

        else:
            print("\nInvalid Email. \nEnter your email again.")

    while True:
        username = input('Enter Username: ')
        cursor = conn.execute(f"SELECT * from users WHERE User_Name= '{username}'").fetchone()

        if cursor:
            print('\nERROR! Username taken.\n')

        else:
            pass
            break

    while True:
        user_option = input('Do you want an auto generated Password.\nYes or No: \n').upper()

        if user_option == 'YES':
            user_password = gen_password()
            print('PLEASE COPY IT DOWN!!!')
            print(f'Your AUTO GENERATED PASSWORD is: {user_password}')
            break

        elif user_option == 'NO':
            user_password = user_gen_password()
            break

        else:
            print('\nERROR!!! Wrong option! Option must be YES or No.\n')

    conn.execute(f"INSERT INTO users (First_Name, Last_Name, Email_Address, User_Name, Password) "
                 f"VALUES ('{first_name}', '{last_name}','{email}', '{username}', '{user_password}')")

    conn.commit()
    print('\nDatabase updated.')
    return username


"""
This function allows the user to login. The function asks the user to input their username and password and the function
checks if it is in our database. If either of the username and password or both are not in our database, the function
will display an error and the user will be asked to input their username and password again.
"""


def login():
    while True:
        user_name = input('Enter your username: ')
        password = input('Enter your password: ')
        cursors = conn.execute(f"SELECT User_Name AND Password from users WHERE User_Name='{user_name}' AND "
                               f"Password='{password}' ").fetchone()

        if cursors:
            print(f'\nCongratulations!!! You successfully logged in.\nWelcome {user_name}.')
            break

        else:
            print('\nERROR!!! Wrong username and password.\n')
    return user_name


while True:
    user_options = input("""
Please select an option to continue.
1 ===> Signup
2 ===> Login
3 ===> Exit App
Choose one: 
""")
    if user_options == '1':
        signup()

    elif user_options == '2':
        login()

        while True:
            user_login_option = input("""
Please select an option to continue.
1 ===> Select Number of Question
2 ===> Logout
Choose one:
""")

            if user_login_option == '1':

                while True:
                    user_number_question = input("""
Please select an option to continue.
1 ===> Select 10 Questions
2 ===> Select 20 Questions
3 ===> Select 30 Questions
4 ===> Go Back To The Previous Menu
Choose one:
""")

                    if user_number_question == '1':
                        print('\n10 questions selected!')

                        while True:
                            user_difficulty = input("""
Please select an option to continue.
1 ===> Easy
2 ===> Medium
3 ===> Hard
4 ===> Go Back To The Previous Menu
Choose one: 
""")

                            if user_difficulty == '1':
                                question.ten_easy_questions()

                            elif user_difficulty == '2':
                                question.ten_medium_questions()

                            elif user_difficulty == '3':
                                question.ten_hard_questions()

                            elif user_difficulty == '4':
                                print('Going back to the previous menu...')
                                break

                            else:
                                print('\nERROR!!! Wrong option!')

                    elif user_number_question == '2':
                        print('\n20 questions selected!')

                        while True:
                            user_difficulty = input("""
Please select an option to continue.
1 ===> Easy
2 ===> Medium
3 ===> Hard
4 ===> Go Back To The Previous Menu
Choose one: 
""")

                            if user_difficulty == '1':
                                question.twenty_easy_questions()

                            elif user_difficulty == '2':
                                question.twenty_medium_questions()

                            elif user_difficulty == '3':
                                question.twenty_hard_questions()

                            elif user_difficulty == '4':
                                print('Going back to the previous menu...')
                                break

                            else:
                                print('\nERROR!!! Wrong option!')

                    elif user_number_question == '3':
                        print('\n30 questions selected!')

                        while True:
                            user_difficulty = input("""
Please select an option to continue.
1 ===> Easy
2 ===> Medium
3 ===> Hard
4 ===> Go Back To The Previous Menu
Choose one: 
""")

                            if user_difficulty == '1':
                                question.thirty_easy_questions()

                            elif user_difficulty == '2':
                                question.thirty_medium_questions()

                            elif user_difficulty == '3':
                                question.thirty_hard_questions()

                            elif user_difficulty == '4':
                                print('Going back to the previous menu...')
                                break

                            else:
                                print('\nERROR!!! Wrong option!')

                    elif user_number_question == '4':
                        print('Going back to the previous menu...')
                        break

                    else:
                        print('\nError!!! Wrong option!')

            elif user_login_option == '2':
                print('Logging out....')
                print(f'See you next time.')
                break

            else:
                print('\nERROR!!! Wrong option!')

    elif user_options == '3':
        print('\nBye, see you next time.')
        break

    else:
        print('\nERROR!!! Wrong option!')
