import sqlite3
from random import choice
from string import ascii_letters


connect=sqlite3.connect('appdb.sqlite')
cursor=connect.cursor()

def create_account():

    print('Kindly fill the details below to generate your gossip ID and password')

    #Get details from users
    name = input('Type in your fullname \n>> ')
    user_organisation = input('Type the organisation you work with\n>> ')
    user_email = input('Type your email address\n>>')

    if len(name) < 1 or len(user_email) < 1 or len(user_organisation) < 1:
        print('\nOne or more field is empty! Kindly fill in as appropriate\n')
        create_account()

    #Generate password
    user_password = name[0:2] + ''.join(choice(ascii_letters) for x in range(5))

    #Add user data to dtabase
    cursor.execute('INSERT OR IGNORE INTO Organisation (name) VALUES (?)', (user_organisation,))
    cursor.execute('SELECT id,name FROM Organisation WHERE name = ?', (user_organisation,))
    row_organisation=cursor.fetchone()[0]

    # check for duplicate mail
    try:
        cursor.execute('INSERT INTO Users (name,password,email,organisation_id) VALUES (?,?,?,?)',
                       (name, user_password, user_email, row_organisation))
    except:
        print()
        print('Email already exist in database!')
        print()
        welcome_page()

    #Commit in database
    connect.commit()
    cursor.execute('SELECT id FROM Users WHERE name=? and email= ?', (name, user_email,))
    fetch_id=cursor.fetchone()[0]

    print()
    print(f'Welcome {name}, your gossip ID is {fetch_id} and your password is {user_password}.'
          f'\nNote your gossip ID and password for login'
          f'\nYour account has been successfully created. Cheers!!! ')
    welcome_page()

def welcome_page():
    print()
    print('Welcome to your fav console gossip app')
    print('Select: \n1 To Open an new account\n2 To login into an existing account\n3 To close app\n')

    #Prompt users
    welcome_response=input('>>')

    #Take user to create account function
    if welcome_response is '1':
        create_account()
        welcome_page()

    #Take user to login function
    elif welcome_response is '2':
        login()
        #welcome_page()
    #Leave platform
    elif welcome_response is '3':
        quit()

    #Incase user enters wrong option
    else:
        print('Select appropriate number!\n')
        welcome_page()

def login():

    #Make variable accessible by other functions
    global input_id

    input_id = input('Input your gossip ID\n>> ')
    input_password = input('Input your password\n>> ')

    if len(input_id) <1 or len(input_password)<1:
        print()
        print('Type in your gossip ID and your password')
        print()
        login()
    # Prevent code from blowing up
    try:
        cursor.execute('SELECT password FROM Users WHERE id = ?', (input_id,))
        # Verify username and password
        fetched_password = cursor.fetchone()[0]


    except:
        print()
        print('Incorrect login details!')
        welcome_page()

    cursor.execute('SELECT name FROM Users WHERE id = ?', (input_id,))
    #Fetch for username
    fetched_name = cursor.fetchone()[0]

    if fetched_password == input_password:
        print()
        print(f'Successful login! Welcome back {fetched_name}')
        print()
        landing_page()

    else:
        print()
        print('Incorrect login details!')
        welcome_page()

def landing_page():
    print('Select:'
          '\n1 To check through latest gossip.'
          '\n2 To post new gossip'
          '\n3 To check profile'
          '\n4 To logout')

    user_response = input('\n>>')

    if user_response is '1':
        gossip_feed()
        return landing_page()

    elif user_response is'2':
        post_gossip()

    elif user_response is '3':
        check_profile()
        landing_page()

    elif user_response is '4':
        welcome_page()

    else:
        print()
        print('Select appropriate number!\n')
        landing_page()

def check_all_profile():
    print('This is the information about all users on this platform')
    print('-' * 80)
    cursor.execute('SELECT name, email,posts,organisation_id FROM Users')
    user_details = cursor.fetchall()

    for all_users in user_details:
        print('-' * 80)
        print('Name: ', all_users[0])
        print('email: ', all_users[1])
        print('No of post: ', all_users[2])
        cursor.execute('SELECT name FROM Organisation WHERE id=?', (all_users[3],))
        org_details = cursor.fetchone()
        print('Organisation', org_details[0])
        print()
    end_of_display = input('Press RETURN key to continue')

def check_profile_by_org():

    which_org = input('Type the organisation you want to fetch User details\n>>')
    try:
        cursor.execute('SELECT id FROM Organisation where name=?', (which_org,))
        org_id = cursor.fetchone()
        cursor.execute('SELECT name,email,posts FROM Users where organisation_id=?', (org_id[0],))
        user_by_org = cursor.fetchall()
        print('-' * 80)
        for users in user_by_org:
            print('Name: ', users[0])
            print('email: ', users[1])
            print('Number of post:', users[2])
    except:
        print('No User is from that Organisation on this platform'
              '\nTell them to join ASAP')
        landing_page()
    print()
    end_of_search = input('Press RETURN key to continue')

def check_profile_by_name():
    which_name = input('Type name of User you want to check details\n>>')
    try:
        cursor.execute('SELECT name,email,posts,organisation_id FROM Users where name=?', (which_name,))
        user_detail = cursor.fetchall()

        for user in user_detail:
            print('-' * 80)
            cursor.execute('SELECT name FROM Organisation where id=?', (user[3],))
            user_by_name = cursor.fetchone()
            print('Name: ', user[0])
            print('email: ', user[1])
            print('Number of post:', user[2])
            print('Organisation: ', user_by_name[0])
    except:
        print(f'{which_name} is not on this platform'
              '\nTell him/her to join ASAP')
        landing_page()
    print()
    end_of_search_by_user = input('Press RETURN key to continue')

def check_profile():
    print('Select: \n1 To check through profile of all Users on platform.'
          '\n2 To check through users from an organisation'
          '\n3 To search for a user\n')

    user_response=input('>>')
    if user_response is '1':
        check_all_profile()

    elif user_response is '2':
        check_profile_by_org()

    elif user_response is '3':
        check_profile_by_name()


    else:
        print('Select appropriate option!')
        check_profile()

def gossip_feed():

    #Select all gossips and soome other properties
    cursor.execute('SELECT id,story,user_id FROM Stories')
    gossip=cursor.fetchall()

    print()
    print('\t\t\tGossip feed')

    # Make all_stories variable accessible by other functions
    global all_stories
    for all_stories in gossip:

        print('-' * 80)
        print('-' * 80)
        print(all_stories[1])

        writer_name=all_stories[2]
        cursor.execute('SELECT name  FROM Users WHERE id=?',(writer_name,))  #
        print('-',cursor.fetchone()[0])

        #Fetch number of likes and unlikes for display
        cursor.execute('SELECT likes, unlikes FROM Stories WHERE id=?', (all_stories[0],))
        story_likes=cursor.fetchone()

        #Likes
        if story_likes[0] is None:
            print('Thumbs up: 0')

        else:
            print('Thumbs up:', story_likes[0])

        #Unlikes
        if story_likes[1] is None:
            print('Thumbs down: 0')

        else:
            print('Thumbs down:', story_likes[1])
        print()

        story_identity = all_stories[0]

        #Check through comments
        cursor.execute('SELECT comments,comment_poster FROM Comments WHERE story_id=?',(story_identity,))
        post_comments=cursor.fetchall()#

        if post_comments == []:
            print('No comment')

        else:
            print('Comments:')
            for comments in post_comments:
                print('\t',comments[0])
                cursor.execute('SELECT name FROM Users WHERE id=?', (comments[1],))
                comment_poster_name=cursor.fetchone()[0]
                print('\t\t-',comment_poster_name)
                print()


        print()
        #Function to comment on post
        comment_on_post()
        print()
        #To either like post or unlike post

        if like_on_post() is True or unlike_on_post() is True:
            print('You reacted to this post!')

        #To continue with feed or not
        if continue_with_feed() is True:
            break



    end_of_gossips=input('End of gossips. Press RETURN key to continue\n>>')

def continue_with_feed():
    global continue_with
    print()
    print('Select: \n1 To return to your dashboard.\n2 To continue reading gossips')
    return_to_dashboard = input('\n>>')

    if return_to_dashboard is '1':
        continue_with=True

    elif return_to_dashboard is '2':
        continue_with=False

    else:
        print('Select appropriate option!')
        continue_with_feed()

    return continue_with

def like_on_post(like=True):
    global dont_unlike
    dont_unlike=True
    while like:

        cursor.execute('SELECT story_id,user_id FROM Likes WHERE story_id=?', (all_stories[0],))

        check_likes = cursor.fetchall()

        for all_likes in check_likes:

            if int(input_id) == all_likes[1]:
                print('You already thumbs up this post prior to this time')
                like = False
                dont_unlike = True
                return True

        cursor.execute('SELECT story_id,user_id FROM Unlikes WHERE story_id=?', (all_stories[0],))

        check_unlikes = cursor.fetchall()

        for all_unlikes in check_unlikes:

            if int(input_id) == all_unlikes[1]:
                print('You already thumbs down this post prior to this time')
                like = False
                already_dislike = True
                return already_dislike

        else:
                user_like_post = input('Do you want to give this post a thumps up? \n1 For Yes \n2 For No\n>>')

                if user_like_post is '1':
                    cursor.execute('INSERT INTO Likes (story_id,user_id) VALUES ( ?,? )', (all_stories[0],input_id,))

                    cursor.execute('SELECT likes FROM Stories WHERE id=?', (all_stories[0],))
                    like_column = cursor.fetchone()[0]

                    if like_column is None:
                        cursor.execute('UPDATE Stories SET likes=1 WHERE id=?', (all_stories[0],))
                    else:
                        cursor.execute('UPDATE Stories SET likes=likes+1 WHERE id=?', (all_stories[0],))
                    connect.commit()
                    print()

                    like=False
                    dont_unlike=True
                    return True

                elif user_like_post is '2':
                    like=False
                    dont_unlike=False
                    return False
                else:
                    print('Select appropriate option!')

def unlike_on_post(unlike=True):
    global already_disliked

    while unlike:

        cursor.execute('SELECT story_id,user_id FROM Unlikes WHERE story_id=?', (all_stories[0],))

        check_unlikes = cursor.fetchall()

        for all_unlikes in check_unlikes:

            if int(input_id) == all_unlikes[1]:
                print('You already thumbs down this post prior to this time')
                unlike = False
                already_dislike=True
                return already_dislike



        user_unlike_post = input('Do you want to give this post a thumps down? \n1 For Yes \n2 for No\n>>')
        if user_unlike_post is '1':
            cursor.execute('INSERT INTO Unlikes (story_id,user_id) VALUES ( ?,? )', (all_stories[0], input_id,))

            cursor.execute('SELECT unlikes FROM Stories WHERE id=?', (all_stories[0],))
            unlike_column = cursor.fetchone()[0]

            if unlike_column is None:
                cursor.execute('UPDATE Stories SET unlikes=1 WHERE id=?', (all_stories[0],))
            else:
                cursor.execute('UPDATE Stories SET unlikes=unlikes+1 WHERE id=?', (all_stories[0],))
            connect.commit()
            print()

            unlike=False
            already_dislike=True
            return already_dislike
        elif user_unlike_post is '2':

            unlike=False
            already_dislike=False
            return already_dislike
        else:
            print('Select appropriate option!')

def comment_on_post(comment=True):

    while comment:

        make_comment = input('Do you want to make a comment on this post? \n1 For Yes \n2 For No\n>>')
        if make_comment is '1':
            your_comments = input('Type in your comments here\n>>')

            cursor.execute('INSERT INTO Comments (story_id, comments,comment_poster) VALUES (?,?,?)',
                           (all_stories[0], your_comments, input_id,))

            cursor.execute('SELECT posts FROM Users WHERE id=?', (input_id,))
            row = cursor.fetchone()[0]

            if row is None:
                cursor.execute('UPDATE Users SET posts=1 WHERE id=?', (input_id,))
            else:
                cursor.execute('UPDATE Users SET posts=posts+1 WHERE id=?', (input_id,))

            connect.commit()
            print('Your comment has been posted!')
            print('-' * 40)
            comment=False

        elif make_comment is '2':
            comment=False

        else:
            print()
            print('Select appropriate option!')
            print()

def post_gossip():

    user_post = input('Type your gossip here\n\n>>')
    if len(user_post)<1:
        print('Empty field not allowed!')
        post_gossip()
    cursor.execute('''INSERT INTO Stories (story,user_id) VALUES (?,?)''', (user_post,input_id,))

    cursor.execute('SELECT posts FROM Users WHERE id=?', (input_id,))

    row=cursor.fetchone()[0]

    if row is None:
        cursor.execute('UPDATE Users SET posts=1 WHERE id=?', (input_id,))
    else:
        cursor.execute('UPDATE Users SET posts=posts+1 WHERE id=?', (input_id,))

    connect.commit()
    print()
    print('Your gossip has been posted!')
    print()
    landing_page()

welcome_page()

