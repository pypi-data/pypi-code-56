import json
import html
import requests
import random


"""
This is a module that contains 9 functions, that produces questions when called. Each function has the same underlying 
principle, the only difference is in the number questions and difficulty of each function. The API is called into each
function. The API is then formatted in JSON and decoded using utf-8. Each API contains a number of questions and their 
respective answers. The answers are then accessed and stored un a variable. A dictionary containing correct and wrong,
each assigned a value. The value will increase as the user answers each question. If they got it right, correct
increases and if the got in wrong, wrong increases. The program then iterates over each questions. Correct answers and 
incorrect answers are placed in separated in place holders. The correct answers are then appended into the incorrect 
place holder. The length of the answers are then iterated and formatted. Then the user will be asked to input their 
answer, if the answer is correct, the user will be notified. If the answer is wrong, the user will be notified and the 
correct answer will be displayed. The user will also be asked if they want to continue, if the user answer yes, the 
program moves to the next question till the end of the question then a message will will appear letting the user know
how many question they got right and wrong out of a total number of question. If the user click no, the questions end
and a message will appear informing the user how many questions they got right and wrong out of a total number of 
questions. 
"""

"""
This function prints out ten questions with easy difficulty level for the user.
"""


def ten_easy_questions():
    res = requests.get('https://opentdb.com/api.php?amount=10&category=18&difficulty=easy')

    data = json.loads(res.content.decode('utf-8'))

    questions = data['results']
    score = {
        'correct': 0,
        'wrong': 0
    }
    option = ['a', 'b', 'c', 'd']

    for question in questions:
        var_question = question['question']

        print('-' * len(var_question))
        print(html.unescape(var_question))
        print('-' * len(var_question))
        print()

        choices = question['incorrect_answers']
        correct = question['correct_answer'].lower()
        choices.append(correct)
        random.shuffle(choices)

        for i in range(len(choices)):
            print(f'({option[i]})', html.unescape(choices[i]))

        answer = input('\nYour answer: ').lower()

        try:
            ans_index = option.index(answer)
            var_answer = choices[ans_index]

        except Exception:
            ans_index = -1
            var_answer = answer

        if var_answer == correct:
            print('\nYay! you got it right!')
            score['correct'] += 1

            next_question = input('\nNext question? y or n: ').upper()
            if next_question == 'N':
                break

        else:
            print(f'\nWrong! Sorry the answer is: {correct}')
            score['wrong'] += 1
            print()

            next_question = input('\nNext question? y or n: ').upper()
            if next_question == 'N':
                break

    msg = f"You got {score['correct']} correct answers and {score['wrong']} wrong answers out of " \
          f"{len(questions)} total questions"

    print()
    print('*' * len(msg))
    print(msg)
    return


"""
This function prints out ten questions with medium difficulty level for the user.
"""


def ten_medium_questions():
    res = requests.get('https://opentdb.com/api.php?amount=10&category=18&difficulty=medium')

    data = json.loads(res.content.decode('utf-8'))

    questions = data['results']
    score = {
        'correct': 0,
        'wrong': 0
    }
    option = ['a', 'b', 'c', 'd']

    for question in questions:
        var_question = question['question']

        print('-' * len(var_question))
        print(html.unescape(var_question))
        print('-' * len(var_question))
        print()

        choices = question['incorrect_answers']
        correct = question['correct_answer'].lower()
        choices.append(correct)
        random.shuffle(choices)

        for i in range(len(choices)):
            print(f'({option[i]})', html.unescape(choices[i]))

        answer = input('\nYour answer: ').lower()

        try:
            ans_index = option.index(answer)
            var_answer = choices[ans_index]

        except Exception:
            ans_index = -1
            var_answer = answer

        if var_answer == correct:
            print('\nYay! You got it right!')
            score['correct'] += 1

            next_question = input('\nNext question? Y or N: ').upper()

            if next_question == 'N':
                break

        else:
            print(f'\nWrong! Sorry the answer is: {correct}')
            score['wrong'] += 1
            print()

            next_question = input('\nNext question? y or n: ').upper()
            if next_question == 'N':
                break

    msg = f"You got {score['correct']} correct answers and {score['wrong']} wrong answers out of " \
          f"{len(questions)} total questions"

    print()
    print('*' * len(msg))
    print(msg)
    return


"""
This function prints out ten questions with hard difficulty level for the user.
"""


def ten_hard_questions():
    res = requests.get('https://opentdb.com/api.php?amount=10&category=18&difficulty=hard')

    data = json.loads(res.content.decode('utf-8'))

    questions = data['results']
    score = {
        'correct': 0,
        'wrong': 0
    }
    option = ['a', 'b', 'c', 'd']

    for question in questions:
        var_question = question['question']

        print('-' * len(var_question))
        print(html.unescape(var_question))
        print('-' * len(var_question))
        print()

        choices = question['incorrect_answers']
        correct = question['correct_answer'].lower()
        choices.append(correct)
        random.shuffle(choices)

        for i in range(len(choices)):
            print(f'({option[i]})', html.unescape(choices[i]))

        answer = input('\nYour answer: ').lower()

        try:
            ans_index = option.index(answer)
            var_answer = choices[ans_index]

        except Exception:
            ans_index = -1
            var_answer = answer

        if var_answer == correct:
            print('\nYay! You got it right!')
            score['correct'] += 1

            next_question = input('\nNext question? Y or N: ').upper()
            if next_question == 'N':
                break

        else:
            print(f'\nWrong! Sorry the answer is: {correct}')
            score['wrong'] += 1
            print()

            next_question = input('\nNext question? y or n: ').upper()
            if next_question == 'N':
                break

    msg = f"You got {score['correct']} correct answers and {score['wrong']} wrong answers out of " \
          f"{len(questions)} total questions"

    print()
    print('*' * len(msg))
    print(msg)
    return


"""
This function prints out twenty questions with easy difficulty level for the user.
"""


def twenty_easy_questions():
    res = requests.get('https://opentdb.com/api.php?amount=20&category=18&difficulty=easy')

    data = json.loads(res.content.decode('utf-8'))

    questions = data['results']
    score = {
        'correct': 0,
        'wrong': 0
    }
    option = ['a', 'b', 'c', 'd']

    for question in questions:
        var_question = question['question']

        print('-' * len(var_question))
        print(html.unescape(var_question))
        print('-' * len(var_question))
        print()

        choices = question['incorrect_answers']
        correct = question['correct_answer'].lower()
        choices.append(correct)
        random.shuffle(choices)

        for i in range(len(choices)):
            print(f'({option[i]})', html.unescape(choices[i]))

        answer = input('\nYour answer: ').lower()

        try:
            ans_index = option.index(answer)
            var_answer = choices[ans_index]

        except Exception:
            ans_index = -1
            var_answer = answer

        if var_answer == correct:
            print('\nYay! You got it right!')
            score['correct'] += 1

            next_question = input('\nNext question? Y or N: ').upper()
            if next_question == 'N':
                break

        else:
            print(f'\nWrong! Sorry the answer is: {correct}')
            score['wrong'] += 1
            print()

            next_question = input('\nNext question? y or n: ').upper()
            if next_question == 'N':
                break

    msg = f"You got {score['correct']} correct answers and {score['wrong']} wrong answers out of " \
          f"{len(questions)} total questions"

    print()
    print('*' * len(msg))
    print(msg)
    return


"""
This function prints out twenty questions with medium difficulty level for the user.
"""


def twenty_medium_questions():
    res = requests.get('https://opentdb.com/api.php?amount=20&category=18&difficulty=medium')

    data = json.loads(res.content.decode('utf-8'))

    questions = data['results']
    score = {
        'correct': 0,
        'wrong': 0
    }
    option = ['a', 'b', 'c', 'd']

    for question in questions:
        var_question = question['question']

        print('-' * len(var_question))
        print(html.unescape(var_question))
        print('-' * len(var_question))
        print()

        choices = question['incorrect_answers']
        correct = question['correct_answer'].lower()
        choices.append(correct)
        random.shuffle(choices)

        for i in range(len(choices)):
            print(f'({option[i]})', html.unescape(choices[i]))

        answer = input('\nYour answer: ').lower()

        try:
            ans_index = option.index(answer)
            var_answer = choices[ans_index]

        except Exception:
            ans_index = -1
            var_answer = answer

        if var_answer == correct:
            print('\nYay! You got it right!')
            score['correct'] += 1

            next_question = input('\nNext question? Y or N: ').upper()
            if next_question == 'N':
                break

        else:
            print(f'\nWrong! Sorry the answer is: {correct}')
            score['wrong'] += 1
            print()

            next_question = input('\nNext question? Y or N: ').upper()
            if next_question == 'N':
                break

    msg = f"You got {score['correct']} correct answers and {score['wrong']} wrong answers out of " \
          f"{len(questions)} total questions"

    print()
    print('*' * len(msg))
    print(msg)
    return


"""
This function prints out twenty questions with hard difficulty level for the user.
"""


def twenty_hard_questions():
    res = requests.get('https://opentdb.com/api.php?amount=20&category=18&difficulty=mhard')

    data = json.loads(res.content.decode('utf-8'))

    questions = data['results']
    score = {
        'correct': 0,
        'wrong': 0
    }
    option = ['a', 'b', 'c', 'd']

    for question in questions:
        var_question = question['question']

        print('-' * len(var_question))
        print(html.unescape(var_question))
        print('-' * len(var_question))
        print()

        choices = question['incorrect_answers']
        correct = question['correct_answer'].lower()
        choices.append(correct)
        random.shuffle(choices)

        for i in range(len(choices)):
            print(f'({option[i]})', html.unescape(choices[i]))

        answer = input('\nYour answer: ').lower()

        try:
            ans_index = option.index(answer)
            var_answer = choices[ans_index]

        except Exception:
            ans_index = -1
            var_answer = answer

        if var_answer == correct:
            print('\nYay! You got it right!')
            score['correct'] += 1

            next_question = input('\nNext question? Y or N: ').upper()
            if next_question == 'N':
                break

        else:
            print(f'\nWrong! Sorry the answer is: {correct}')
            score['wrong'] += 1
            print()

            next_question = input('\nNext question? Y or N: ').upper()
            if next_question == 'N':
                break

    msg = f"You got {score['correct']} correct answers and {score['wrong']} wrong answers out of " \
          f"{len(questions)} total questions"

    print()
    print('*' * len(msg))
    print(msg)
    return


"""
This function prints out thirty questions with easy difficulty level for the user.
"""


def thirty_easy_questions():
    res = requests.get('https://opentdb.com/api.php?amount=30&category=18&difficulty=easy')

    data = json.loads(res.content.decode('utf-8'))

    questions = data['results']
    score = {
        'correct': 0,
        'wrong': 0
    }
    option = ['a', 'b', 'c', 'd']

    for question in questions:
        var_question = question['question']

        print('-' * len(var_question))
        print(html.unescape(var_question))
        print('-' * len(var_question))
        print()

        choices = question['incorrect_answers']
        correct = question['correct_answer'].lower()
        choices.append(correct)
        random.shuffle(choices)

        for i in range(len(choices)):
            print(f'({option[i]})', html.unescape(choices[i]))

        answer = input('\nYour answer: ').lower()

        try:
            ans_index = option.index(answer)
            var_answer = choices[ans_index]

        except Exception:
            ans_index = -1
            var_answer = answer

        if var_answer == correct:
            print('\nYay! You got it right!')
            score['correct'] += 1

            next_question = input('\nNext question? Y or N: ').upper()
            if next_question == 'N':
                break

        else:
            print(f'\nWrong! Sorry the answer is: {correct}')
            score['wrong'] += 1
            print()

            next_question = input('\nNext question? Y or N: ').upper()
            if next_question == 'N':
                break

    msg = f"You got {score['correct']} correct answers and {score['wrong']} wrong answers out of " \
          f"{len(questions)} total questions"

    print()
    print('*' * len(msg))
    print(msg)
    return


"""
This function prints out thirty questions with medium difficulty level for the user.
"""


def thirty_medium_questions():
    res = requests.get('https://opentdb.com/api.php?amount=30&category=18&difficulty=medium')

    data = json.loads(res.content.decode('utf-8'))

    questions = data['results']
    score = {
        'correct': 0,
        'wrong': 0
    }
    option = ['a', 'b', 'c', 'd']

    for question in questions:
        var_question = question['question']

        print('-' * len(var_question))
        print(html.unescape(var_question))
        print('-' * len(var_question))
        print()

        choices = question['incorrect_answers']
        correct = question['correct_answer'].lower()
        choices.append(correct)
        random.shuffle(choices)

        for i in range(len(choices)):
            print(f'({option[i]})', html.unescape(choices[i]))

        answer = input('\nYour answer: ').lower()

        try:
            ans_index = option.index(answer)
            var_answer = choices[ans_index]

        except Exception:
            ans_index = -1
            var_answer = answer

        if var_answer == correct:
            print('\nYay! You got it right!')
            score['correct'] += 1

            next_question = input('\nNext question? Y or N: ').upper()
            if next_question == 'N':
                break

        else:
            print(f'\nWrong! Sorry the answer is: {correct}')
            score['wrong'] += 1
            print()

            next_question = input('\nNext question? Y or N: ')
            if next_question == 'N':
                break

    msg = f"You got {score['correct']} correct answers and {score['wrong']} wrong answers out of " \
          f"{len(questions)} total questions"

    print()
    print('*' * len(msg))
    print(msg)
    return


"""
This function prints out thirty questions with hard difficulty level for the user.
"""


def thirty_hard_questions():
    res = requests.get('https://opentdb.com/api.php?amount=30&category=18&difficulty=hard')

    data = json.loads(res.content.decode('utf-8'))

    questions = data['results']
    score = {
        'correct': 0,
        'wrong': 0
    }
    option = ['a', 'b', 'c', 'd']

    for question in questions:
        var_question = question['question']

        print('-' * len(var_question))
        print(html.unescape(var_question))
        print('-' * len(var_question))
        print()

        choices = question['incorrect_answers']
        correct = question['correct_answer'].lower()
        choices.append(correct)
        random.shuffle(choices)

        for i in range(len(choices)):
            print(f'({option[i]})', html.unescape(choices[i]))

        answer = input('\nYour answer: ').lower()

        try:
            ans_index = option.index(answer)
            var_answer = choices[ans_index]

        except Exception:
            ans_index = -1
            var_answer = answer

        if var_answer == correct:
            print('\nYay! You got it right!')
            score['correct'] += 1

            next_question = input('\nNext question? Y or N: ').upper()
            if next_question == 'N':
                break

        else:
            print(f'\nWrong! Sorry the answer is: {correct}')
            score['wrong'] += 1
            print()

            next_question = input('\nNext question? Y or N: ').upper()
            if next_question == 'N':
                break

    msg = f"You got {score['correct']} correct answers and {score['wrong']} wrong answers out of " \
          f"{len(questions)} total questions"

    print()
    print('*' * len(msg))
    print(msg)
    return

