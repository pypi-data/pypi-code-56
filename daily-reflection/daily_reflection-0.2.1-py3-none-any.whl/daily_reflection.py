#!/usr/bin/python3


# https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df

from __future__ import print_function, unicode_literals
from pprint import pprint
from tinydb import TinyDB, where, Query
import tinydb_encrypted_jsonstorage as tae
from reflect.actions import *
import sys
import os
import datetime
import uuid # creating unique id's for storage
from pathlib import Path # for finding user's home
# colorise output
from prompt_toolkit.shortcuts import prompt


from prompt_toolkit import prompt
from prompt_toolkit.filters import Condition

from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import prompt
import getpass

from reflect.style import *

from reflect.version import *

# get password
clear_screen()
print("Daily Reflection, v%s"%VERSION)

encryption_key = prompt( [('class:key','Password? ' )], is_password=True, style=style)
try:
    from os.path import join as join_path
    global db
    db = TinyDB(encryption_key=encryption_key, path=join_path(str(Path.home()),".reflect.db"), storage=tae.EncryptedJSONStorage)
except:
    print("Error loading DB, probably wrong encryption key",sys.exc_info()[0], sys.exc_info()[1])
    sys.exit(1)

def quit():
    return False

def reflection_menu():
    global db
    items = {
        "title":{"text":"What do you want to do?"},
        "r":{"text":"Do reflection", "handler": do_reflection},
        "--1":{},
        "a":{"text":"Add questions", "handler": add_questions },
        "m":{"text":"Modify questions", "handler": modify_questions },
        "o":{"text":"Change questions order", "handler": change_order },
        "d":{"text":"Delete questions", "handler": delete_questions },
        "--2":{},
        "p":{"text":"Change password", "handler": quit },
        "b":{"text":"Browse questions", "handler": quit },
        "e":{"text":"Export reflections", "handler": quit },
        "--3":{},
        "q":{"text":"Quit", "handler": quit }
    }
    clear_screen()
    while True:
        key = key_press_menu(menu_items=items)

        if key=="q" or key=="escape":
            break

        if key in ["r","a","m","o","d"]:
            clear_screen()
            time = time_menu()
            print("You chose: %s\n"%time)
            items[key]["handler"](time,db)

        if key == "e":
            clear_screen()
            export(db)
            continue
        if key == "b":
            clear_screen()
            browse( today(), db )
            continue
        if key == "p":
            clear_screen()
            change_password(db)
            continue
