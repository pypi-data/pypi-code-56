import getpass
from termcolor import colored
from colorama import init
init()
from pusher import Pusher
import pysher
import os
import json
import random
import string
import re


class welcome():
    def __init__(self):
        print("\n")
        print(colored("*********************************", "white"))     
        print(colored("*       ---- DevGossip ----     *", "white"))
        print(colored("*********************************", "white"))
        print(colored("<< 1. Signup                 >>", "green"))
        print(colored("<< 2. Login                  >>", "green"))
        print(colored("<< 3. close App              >>", "green"))
        
        selection = input("Please choose a number from the options above: ")


        if selection == str(1):
            sign_up()
        elif selection == str(2):
            log_in()
            while True:
                logged_in()
        elif selection == str(3):
            close_app()
        else:
            print("Please input '1' to signup; '2' to login or '3' to close the app")
            welcome()

            

    ''' This function handles signup to the system'''
class sign_up:
    def __init__(self):
        print("\n")
        print(colored("Please pres Ctrl+c at anytime to cancel signup and go back to Welcome page", "red"))
        try:
            while True:
                userName= input('Please choose a Username: ')
                if not userName.isalpha():
                    print("Your username must consist of letters only.")
                    continue
                else:
                    break
                
            while True:
                passWord= input('Please choose a password: ')
                break

            while True:
                email_add = input('Email Address: ')
                match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email_add)
                if match == None:
                    print('Invalid email address')
                    continue
                else:
                    break
                
            print("Your registration is complete. Please login")

            with open(f'userDetails.txt', 'a+') as users:
                for details in [userName, passWord, email_add]:
                    users.write(f"{details} ",)
                users.write('\n')
            welcome()
        
        except KeyboardInterrupt:
            print("Registration was cancelled.")
            welcome()


        

    ''' This function handles logon to the system'''
class log_in:
    users=()

    def __init__(self):
        print("\n")
        print(colored("Please pres Ctrl+c at anytime to cancel 'Login' and go back to Welcome page", "red"))
        try:
            file = open("userDetails.txt")
            users = file.read().strip().split()
            username = input("Please enter your username: ")
            password = getpass.getpass("Please enter %s's Password:" % username)
            #while True:
            if username in users:
                if password in users:
                    self.user = username
                else:
                    print(colored("Your password is incorrect", "red"))
                    log_in()
            else:
                print(colored("Your username is incorrect", "red"))
                log_in()

        except KeyboardInterrupt:
            print("Login was terminated")
            welcome()



    '''To close the app'''
class close_app:
    def __init__(self):
        exit()



class logged_in:
    pusher = None
    channel = None
    chatroom = None
    clientPusher = None
    user =()
    chatrooms = ["Python", "Java", "Php", "C", "Web", "Stacks", "General"]

    def __init__(self):
        print("\n")        
        print("You're logged in   ")
        print(colored("<< 1. Logout                        >>", "green"))
        print(colored("<< 2. Choose a room                 >>", "green"))
        print(colored("<< 3. Delete your account           >>", "green"))
        
        selection = input("Please choose a number from the options above: ")


        if selection == str(1):
            print("You are logged out")
            welcome()
        elif selection == str(2):
            self.selectChatroom()
            while True:
                self.getInput()
        elif selection == str(3):
            delete_User()
        else:
            print(colored("Please input '1' to Logout; '2' to Choose a room or '3' to delete your account", "red"))
            logged_in()


    ''' This function is used to select which chatroom you would like to connect to '''
    def selectChatroom(self):
        print("\n")
        try:
            print(colored("Please pres Ctrl+c at anytime to exit", "red"))        
            print(colored("Info! Available Rooms are %s" % str(self.chatrooms), "yellow"))
            chatroom = input("Please select a Room: ").capitalize()
            if chatroom in self.chatrooms:
                print("Please pres Ctrl+c at anytime to exit the Room")
                self.chatroom = chatroom
                self.initPusher()
            else:
                print(colored("No such Room in our list", "red"))
                self.selectChatroom()
        except KeyboardInterrupt:
            logged_in()

   
    ''' This function initialises both the Http server Pusher as well as the clientPusher'''
    def initPusher(self):
        self.pusher = Pusher(app_id=os.getenv('PUSHER_APP_ID', '1006082'), key=os.getenv('PUSHER_APP_KEY', 'e609aeea48c0c31e5fb1'), secret=os.getenv('PUSHER_APP_SECRET', '93b8e77f996839a42523'), cluster=os.getenv('PUSHER_APP_CLUSTER', 'eu'))
        self.clientPusher = pysher.Pusher(os.getenv('PUSHER_APP_KEY', 'e609aeea48c0c31e5fb1'), os.getenv('PUSHER_APP_CLUSTER', 'eu'))
        self.clientPusher.connection.bind('pusher:connection_established', self.connectHandler)
        self.clientPusher.connect()
        
    ''' This function is called once pusher has succesfully established a connection'''
    def connectHandler(self, data):
        self.channel = self.clientPusher.subscribe(self.chatroom)
        self.channel.bind('newmessage', self.pusherCallback)
    
    ''' This function is called once pusher recieves a new event '''
    def pusherCallback(self, message):
        message = json.loads(message)
        if message['user'] != self.user:
            print(colored("{}: {}".format(message['user'], message['message']), "blue"))
            print(colored("{}: ".format(self.user), "green"))
    
    ''' This function is used to get the user's current message '''
    def getInput(self):
        try:
            message = input(colored("{}: ".format(self.user), "green"))
            self.pusher.trigger(self.chatroom, u'newmessage', {"user": self.user, "message": message})
        except KeyboardInterrupt:
            self.selectChatroom()
    


class delete_User:
    def __init__(self):
        print("\n")
        print(colored("Please pres Ctrl+c to terminate this process", "red"))   
        try:
            yn = input("Are you sure? Y/N: ").lower()
            if yn =='y':
                del_user = input("Please input your username: ")
                with open("userDetails.txt", "r+") as f:
                    d = f.readlines()
                    f.seek(0)
                    for line in d:
                        if del_user not in line:
                            f.write(line)
                    f.truncate()
                print("Your account has been deleted")
                welcome()
            elif yn == 'n':
                logged_in()
        except KeyboardInterrupt:
            logged_in()
