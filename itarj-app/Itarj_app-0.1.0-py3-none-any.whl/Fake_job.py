# Defining a function that allows users either sign up or sign in
def choices():
    try:
        print('####### Welcome Fake job alert app ######')
        print("Please choose what you would like to do.")
        choice = int(input("Type 1 to sign up and 2 to sign in: "))
        if choice == 1:
            return getdetails()
        elif choice == 2:
            return checkdetails()
        else:
            print("not a valid digit")
            return choices()
    except (ValueError, TypeError,):
        print('Why are you like this, you can only enter a digit!!!')
        return choices()


# this function allows user input and submit their details

def getdetails():
    print("Please Provide")
    name = str(input("Full Name: "))
    password = str(input("Password: "))
    f = open("User_Data.txt", 'r')
    info = f.read()
    if name in info:
        print("Name Unavailable. Please Try Again")
        return getdetails()
    f.close()
    f = open("User_Data.txt", 'w')
    info = info + " " + name + " " + password
    f.write(info)


# log in function
def checkdetails():
    print("Please Provide")
    name = str(input("Name: "))
    password = str(input("Password: "))
    f = open("User_Data.txt", 'r')
    info = f.read()
    info = info.split()
    if name in info:
        index = info.index(name) + 1
        usr_password = info[index]
        if usr_password == password:
            return "Welcome Back, " + name
        else:
            print("Password entered is wrong")
            return checkdetails()
    else:
        print("Name not found. Please Sign Up.")
        return getdetails()


print(choices())

'''def welcome():
    print('####### Welcome Fake job alert app ######...')'''


def search_or_post():
    prompt = input('Enter \'post\' to post a job and \'search\' to search a job :: ').strip().lower()
    key = ['post', 'search']
    if prompt not in key:
        print('Invalid key! Enter \'Search\' or \'Post\' to proceed.')
        return search_or_post()
    return prompt


def post_job():
    company_name = input('Enter the Company name :: ')
    job_title = input('Enter the job_title :: ')
    month_posted = input('Enter the posted date :: ')

    with open('jobs.txt', 'a') as jobs:
        jobs.write(f'{company_name}, {job_title}, {month_posted}\n')
        print('thanks for posting')
        return sign_out()


def search_job():
    print("Enter company name, job title or month posted.")
    prompt = input('Make your search entry :: ').lower()
    with open('jobs.txt') as jobs_data:
        for line in jobs_data.readlines():
            if prompt in line.lower():
                print(line)
                return sign_out()
            else:
                print('No search found')
                return search_or_post()


def sign_out():
    try:

        prompt = int(input('Enter \'3\' to sign out : : '))
    except (ValueError, TypeError):
        print('invalid input, Enter 3 to sign out')
        return sign_out()
    else:
        key = [3]
        if prompt not in key:
            print('invalid key, enter 3 to sign out')
            return sign_out()
        else:
            if prompt == 3:
                print('See you next time')
                return choices()
            else:
                return search_or_post()


def main():
    user_input = search_or_post()
    if user_input == 'post':
        post_job()
    else:
        search_job()


main()
