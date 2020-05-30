# importing requests package,click, and os

import click
import requests
import os


def login():
    login_page = input('Hello, Welcome! Please enter 1 or 2 to continue. \n1. login \n2. Close App \n:')
    if login_page == "1":
        user_login()
    elif login_page == "2":
        exit()
    else:
        print("Invalid request")
        login()  # calling back the login page to show the options


def user_login():
    print("Hello there! I'm Tri_Vail, your general knowledge buddy "
          "for quiz and interview! You can always count on me")
    user_name = input(" What's your name?: ")
    print("It's nice meeting you", user_name, " I will give you a result shortly")
    print('-' * 100)
    
    
@click.command()
def get_started():
    """
    Worried? Here's some help!
    """
    login()
    session_details = open('user_session.txt', 'w')
    # opentdb api for the random trivia questions
    api_url = "https://opentdb.com/api.php?amount=50"
    response = requests.get(api_url)
    # fetching the data in json format using the click command
    click.echo(response.json())
    click.echo('\n')
    click.echo('-' * 100)
    session_details.close()
    os.remove('user_session.txt')
    # Handling endpoint errors
    try:
        response.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % exc)


if __name__ == '__main__':
    get_started()
