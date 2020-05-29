import click
import pyfiglet
import mysql.connector
from mysql.connector import Error

#conecting to the database
@click.command()
def sql_connection():
    global cnx
    try:
        cnx = mysql.connector.connect(user='machoBeaver9@server248514724', password='7718e510-c19a-45ce-b1d5-0015d7ffe82f', host='server248514724.mysql.database.azure.com', port=3306, database='sampledb')

        if cnx.is_connected():
            global cursor
            db_Info = cnx.get_server_info()
            print("Connected to Itarj-console db Server Version ", db_Info)
            cursor = cnx.cursor()
            welcome()
    except Error as e:
        print("Couldn't connect check your internet connection and try again.")
        reconnect = click.confirm(click.style('Try again?', fg='yellow'))
        if reconnect:
            click.clear()
            sql_connection()
        else:
            exit(0)

@click.command()
def welcome():
    #welcome screen pyfiglet creates the itarj font
    greet = pyfiglet.figlet_format("I t a r j", font = "slant")
    click.secho(greet, fg='bright_yellow', bold=True)
    click.secho("\nThis is Itarj console. A console application that allows users to register reports of fake job alerts, news or adverts. \nUsers can also search for recorded fake job alerts using keywords.", fg='bright_green')
    global username
    username = click.prompt(click.style('\nTo use this application, please enter a username\n', fg='bright_white', bold=True) + click.style('Username',fg='bright_blue'))

    click.secho(f"\nWelcome, {username}!", color='bright_white', bold=True)
    menu()

@click.command()
def menu():
    #menu
    click.echo('Select an option from the menu')
    click.echo('1: Register fake job alert')
    click.echo('2: Search')
    click.echo('3: Exit application')
    menu_option = click.prompt(click.style('Enter option number', fg='bright_yellow'))
    if menu_option == '1':
        register_alert()
    elif menu_option == '2':
        search_alert()
    elif menu_option == '3':
        cursor.close()
        cnx.close()
        exit(0)
    else:
        click.echo('\n')
        menu()

@click.command()
def register_alert():
    # userscan register using Title, details, username and timestamp are added automatically
    title = click.prompt('Enter the' + click.style(' Title', fg='cyan') + ' of your post (Press "Enter" to submit)')
    post_details()
    upload_post_details = click.confirm("Do you want to upload post?")
    if upload_post_details:
        cursor.execute("CREATE TABLE IF NOT EXISTS job (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), title VARCHAR(255), details TEXT NOT NULL, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cursor.execute("""INSERT INTO job(username, title, details) VALUES (%s, %s, %s)""", (username, title, details))
        cnx.commit()
        click.secho("Post uploaded successfully!", fg="bright_green", bold=True)
        menu()
    else:
        menu()

def post_details():
    click.echo("\nEnter the details of your" + click.style(" Post", fg='blue') + " (links can also be included)")
    click.echo("An editor will be opened to input the post" + click.style(" (remember to save)", fg="red"))
    #opens editor for input
    continue_to_post = click.confirm("Do you want to continue?")
    if continue_to_post:
        global details
        details = click.edit()
        if details is None:
            click.secho("\nRemember to save and do not submit an empty file", fg='red', bold=True)
            post_details()
        elif details == "":
            click.secho("\nRemember to save and do not submit an empty file", fg='red', bold=True)
            post_details()
    else:
        menu()

@click.command()
def search_alert():
    #queries the database for a string or strings
    search_keyword = click.prompt(click.style("Enter search keyword", fg="bright_cyan"))
    if search_keyword == "":
        click.secho("Enter a search keyword and try again", fg='red')
        search_alert()
    weblink = "https://itarj-web.herokuapp.com/search/" + search_keyword
    click.launch(weblink)
    menu()

if __name__ == '__main__':

    details = ""
    username = ""
    cursor = ""
    cnx = ""
    #starts the application
    sql_connection()
    #closes cursor
    cursor.close()
    #closes connection to the database
    cnx.close()