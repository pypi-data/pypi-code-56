from utils import check, options


def runapp():
    print('\033[1;33m WELCOME to DevGossip. Catch up on the most entertaining gossip right here!')
    print('\nHow would you like to start?\nA. Sign Up \nB. Log in \nC. Post as anonymous \nD. Close App')
    user_choice = input('\n>> ').upper()

    while not check(user_choice):
        print('\033[1;91mInvalid action!')
        user_choice = input('>> ').upper()
        print()

    else:
        options(user_choice)


runapp()
