message4 = 'invalid response, respond with 1, 2, or 3'
message1 = 'login succesful'
message2 = 'login not successful please try again'
message5 = 'invalid response, enter a valid number, (e.g 10)'
message3 = 'invalid response, respond with 1, or 2'
message6 = 'please get an internet connection'
message7 = 'Welcome to RandAlgo console, looking for Algorithm questions? we got you'
message8 = 'Please login'


def message_log(message):
    '''
This functions prints all types of messages in our app ranging from error messages
to welcome meassages'''
    print(message)
    return message


def collect_user_details():
    '''
    this function collects and returns details of the user
    input:
        user response to first prompt when they install app
    output:
        user_registration file after details are been entered
    '''
    global first_name
    first_name = input('Firstname:\n')
    global last_name
    last_name = input('Lastname:\n')
    global e_mail
    e_mail = input('E-mail:\n')
    global username
    username = input('Username:\n')
    global password
    password = input('password:\n')
    return first_name, last_name, e_mail, username, password


def create_user_details_file(first_name, last_name, e_mail, username, password):
    '''This function creates a file in the local machine of the user, onceuser finishes registration
input:
    user details like name, username, and password
output:
    csv file containing user details
'''
    global file1
    with open('UserRegister.txt', 'w') as file1:
        '''the file UserRegister.txt is the csv file that will be created on users local machine to
        hold user details in case for login purposes'''
        file1.write(f'''fullname {first_name}
last {last_name}
e-mail {e_mail}
username {username}
password {password}
        ''')
    file1.close()
    return file1


def register_user():
    '''this file collaborates the above functions and register users successfully
'''
    collect_user_details()
    create_user_details_file(first_name, last_name, e_mail, username, password)
    return file1


def collect_user_details2():
    '''
    input:
        user details
    output:

    '''
    global username
    global password
    username = input('Username:\n')
    password = input('Password\n')
    return username, password


def user_reg_details(file):
    '''
    this functions is been called whenever an id confirmation is to take place e.g login checks
    input:
        the csv file to be read
    output:
        variable containing user details
    '''
    user_details1 = [line.strip() for line in open(file, 'r')]
    user_details2 = [m.split(' ') for m in user_details1]
    for i in user_details2:
        if len(i) == 3:
            user_details2.remove(i)
        elif i == ['']:
            user_details2.remove(i)
        else:
            continue
    user_details_dictionary = dict(user_details2)
    d = user_details_dictionary  # d is a variable used to store user details in a clean dictionary
    return d


def login_user():
    '''This feature collects user details and check if details are valid before proceeding further.
    input:
        username and password of user
    output:
        validation
    '''
    collect_user_details2()
    d = user_reg_details('UserRegister.txt')
    if (password == d['password']) and (username == d['username']):
        return True
    else:
        return False


def webcrawl_site(x):
    '''This function actually serves as the API since we could'nt get one
    input:
       integer value entered by the user
    output:
        Number of questions displayed as requested by the user
    '''
    from bs4 import BeautifulSoup
    import requests
    import csv
    from random import randint

    for x in range(1, x + 1):
        source = requests.get(f'https://projecteuler.net/problem={randint(1, 150)}').text
        soup = BeautifulSoup(source, 'lxml')
        content = soup.find('div', id='content').text
        print(content)
        print()
    return content


def fetch_algo_questions():
    '''This fuction allows user to input the amount of question they want and in turn returns algorithm
    questions
    input:
        integer value within a specified range
    output:
        algoruthm questions in the requested amount
    '''
    while True:
        try:
            number = int(input('How many questions do you want?\n'))
        except NameError:
            message_log(message5)
            break
        except ValueError:
            message_log(message5)
            break
        except SyntaxError:
            message_log(message5)
            break
        question = input('Are you sure connected to the internet?,(yes/no)\n')
        # question is used to put user on check if he has an internet connection
        if question == 'yes':
            question = True
        else:
            question = False

        if question == True:
            webcrawl_site(number)
            break
        else:
            message_log(message6)
            break


def give_user_question():
    '''
    This funtion comes to play when user wants to repeat action'''
    while True:
        try:
            user_action = eval(input('1 Get Question\n2 Logout\n'))
        except NameError:
            message_log(message3)
            continue
        except ValueError:
            message_log(message3)
            continue
        except SyntaxError:
            message_log(message3)
            continue
        if user_action == 1:
            fetch_algo_questions()
        elif user_action == 2:
            break
        else:
            continue


def main():
    '''This function calls and integrate everyother function in the CLI to enable users run them
    '''
    message_log(message7)
    while True:
        try:
            user_action = eval(
                input('1 Register\n2 Login\n3 Quit App\n'))  # user_action is the variable that collects the useraction
        except NameError:
            message_log(message4)
            continue
        except ValueError:
            message_log(message4)
            continue
        except SyntaxError:
            message_log(message4)
            continue
        if user_action == 1:
            register_user()
            message_log(message8)
            if login_user():
                message_log(message1)
                give_user_question()
            else:
                message_log(message2)
                continue
        elif user_action == 2:
            if login_user():
                message_log(message1)
                give_user_question()
            else:
                message_log(message2)
                continue
        elif user_action == 3:
            break
        else:
            message_log(message4)
            continue


if __name__=='__main__':
    main()
