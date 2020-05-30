from bs4 import BeautifulSoup
import requests
import random

def main():
    print('WELCOME TO RANDALGO; A RANDOM ALGORITHM QUESTIONS FETCHER!!!')

    option = int(input("To sign up if you haven't signed up before press 1 "
                       "and 2 to log in if you already have an account: "))
    user_detail = {}


    def login():
        first_name = input('Enter first name: ')
        last_name = input('Enter last name: ')
        password = input('Enter password: ')
        with open('user.txt', 'r') as user:
            for key in user:
                if first_name in key and last_name in key and password in key:
                    print('You logged in successfully')


    def question_fetcher():
        page = requests.get('https://www.toptal.com/algorithms/interview-questions')
        soup = BeautifulSoup(page.content, 'html.parser')
        questions = soup.find_all("div", class_="interview_question-content for-question content_body")
        data = []
        for question in questions:
            datum = {}
            algorithm_question = question.p.text
            datum['question'] = algorithm_question

            data.append(datum)
            if question == questions[-1]:
                for information in data:
                    pass

        que = input(
            'Do you want to enter the number of questions you would like the system to get for you? \nEnter yes '
            'to do so \nEnter no to make the system return a single question: ')
        while que == 'yes':
            print('\nNOTE: The system has only 19 algorithm questions')
            try:
                number_of_question = int(input('Enter the number of questions you want to search for: '))
                if number_of_question > 19:
                    print('The number of questions you are trying to get is greater than the number of questions in the system :(')
                    continue
                elif number_of_question > 1:
                    user_question = random.choices(data, k=number_of_question)
                    count = 0
                    for i in user_question:
                        count += 1
                        print(f"{count}: {i['question']} \n")
                    continue_or_not = int(input('Do you want to ask another question? press 1 to continue and 2 to stop: '))
                    if continue_or_not == 1:
                        continue
                    elif continue_or_not == 2:
                        break
                    else:
                        print('Invalid number')
                        continue

            except ValueError:
                continue
            break

        else:
            user_question = random.choice(data)
            count = 0
            for i in [1]:
                count += 1
                print(f"{count}: {user_question['question']}")

    if option == 1:
        def signup():
            first_name = input('Enter first name: ')
            last_name = input('Enter last name: ')
            password = input('Enter the password of your choice: ')
            confirm_password = input('Enter password again for confirmation: ')
            while True:
                user_detail['first_name'] = first_name
                user_detail['last_name'] = last_name
                user_detail['password'] = password
                user_detail['confirm_password'] = confirm_password
                if password == confirm_password:
                    with open('user.txt', 'a') as user_account:
                        user_account.write('\n' + str(user_detail) + ',')
                        break
                else:
                    print('Passwords do not match, please re enter passwords')
                    password = input('Enter the password of your choice: ')
                    confirm_password = input('Enter password again for confirmation: ')
                    continue
            options = input('Do you want to login? yes to login, no to close app: ')
            if options == 'yes':
                login()
                question_fetcher()

        signup()
    elif option == 2:
        login()
        question_fetcher()


if __name__ == "__main__":
    main()
